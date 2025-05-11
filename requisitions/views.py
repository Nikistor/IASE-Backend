import os
import requests
import mimetypes
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponse, FileResponse
from django.utils.dateparse import parse_datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from requisitions.jwt_helper import create_access_token
from requisitions.utils import identity_user
from requisitions.permissions import *
from requisitions.serializers import *
from requisitions.models import *

access_token_lifetime = settings.JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()


def get_draft_requisition_id(request):
    user = identity_user(request)

    if user is None:
        return None

    requisition = (
        Requisition.objects.filter(employer_id=user.pk).filter(status=1).first()
    )

    if requisition is None:
        return None

    return requisition


@api_view(["GET"])
def search_company(request):
    """
    Возвращает список компании
    """

    # Получим параметры запроса из URL
    name = request.GET.get("query")

    # Получение данные после запроса с БД (через ORM)
    company = Company.objects.filter(status=1)

    # Применим фильтры на основе параметров запроса, если они предоставлены
    if name:
        company = company.filter(name__icontains=name)

    serializer = CompanySerializer(company, many=True)

    draft_requisition = get_draft_requisition_id(request)

    resp = {
        "draft_requisition_id": draft_requisition.pk if draft_requisition else None,
        "companies": serializer.data,
    }

    return Response(resp)


@api_view(["GET"])
def get_company_by_id(request, company_id):
    """
    Возвращает информацию о конкретном компании
    """
    if not Company.objects.filter(pk=company_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Получение данные после запроса с БД (через ORM)
    company = Company.objects.get(pk=company_id)

    serializer = CompanySerializer(company, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_company(request, company_id):
    """
    Обновляет информацию о компании
    """

    if not Company.objects.filter(pk=company_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    company = Company.objects.get(pk=company_id)
    serializer = CompanySerializer(company, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_company(request):
    """
    Добавляет новую компанию
    """
    company = Company.objects.create()

    serializer = CompanySerializer(company)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsModerator])
def delete_company(request, company_id):
    """
    Удаляет компанию
    """
    if not Company.objects.filter(pk=company_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    company = Company.objects.get(pk=company_id)
    company.status = 2
    company.save()

    companies = Company.objects.filter(status=1)
    serializer = CompanySerializer(companies, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_company_to_requisition(request, company_id):
    """
    Добавляет компанию в заявку
    """
    token = get_access_token(request)
    payload = get_jwt_payload(token)
    user_id = payload["user_id"]

    if not Company.objects.filter(pk=company_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    company = Company.objects.get(pk=company_id)

    requisition = Requisition.objects.filter(status=1).last()

    if requisition is None:
        requisition = Requisition.objects.create(
            date_created=timezone.now(), date_formation=None, date_complete=None
        )

    requisition.name = "Заявка №" + str(requisition.pk)
    requisition.employer = CustomUser.objects.get(pk=user_id)
    requisition.companies.add(company)
    requisition.save()

    serializer = RequisitionSerializer(requisition)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_company_image(request, company_id):
    """
    Возвращает фото компании
    """
    if not Company.objects.filter(pk=company_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    company = Company.objects.get(pk=company_id)

    return HttpResponse(company.image, content_type="image/jpg")


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_company_image(request, company_id):
    """
    Обновляет фото компании
    """
    if not Company.objects.filter(pk=company_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    company = Company.objects.get(pk=company_id)
    serializer = CompanySerializer(company, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_requisitions(request):
    token = get_access_token(request)
    payload = get_jwt_payload(token)
    user = CustomUser.objects.get(pk=payload["user_id"])

    status = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")

    requisitions = Requisition.objects.exclude(status__in=[1, 5])

    if not user.is_moderator:
        requisitions = requisitions.filter(employer_id=user.pk)

    if status > 0:
        requisitions = requisitions.filter(status=status)

    if date_start:
        # requisitions = requisitions.filter(date_formation__gte=datetime.strptime(date_start, "%Y-%m-%d").date())
        requisitions = requisitions.filter(
            date_formation__gte=parse_datetime(date_start)
        )

    if date_end:
        # requisitions = requisitions.filter(date_formation__lte=datetime.strptime(date_end, "%Y-%m-%d").date())
        requisitions = requisitions.filter(date_formation__lte=parse_datetime(date_end))

    serializer = RequisitionSerializer(
        requisitions, many=True, context={"request": request}
    )
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_requisition_by_id(request, requisition_id):
    """
    Возвращает информацию о конкретной заявки
    """
    if not Requisition.objects.filter(pk=requisition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    requisition = Requisition.objects.get(pk=requisition_id)
    serializer = RequisitionSerializer(requisition, context={"request": request})

    return Response(serializer.data)


@api_view(["PUT", "PATCH"])  # Разрешаем оба метода
@permission_classes([IsAuthenticated])
def update_requisition(request, requisition_id):
    try:
        requisition = Requisition.objects.get(pk=requisition_id)
    except Requisition.DoesNotExist:
        return Response(
            {"detail": "Заявка не найдена."}, status=status.HTTP_404_NOT_FOUND
        )

    # Для PATCH используем partial=True, для PUT — нет
    serializer = RequisitionSerializer(
        requisition, data=request.data, partial=(request.method == "PATCH")
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsRemoteService])
def update_requisition_bankrupt(request, requisition_id):
    if not Requisition.objects.filter(pk=requisition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    requisition = Requisition.objects.get(pk=requisition_id)
    serializer = RequisitionSerializer(
        requisition, data=request.data, many=False, partial=True
    )

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


def calculate_requisition_bankrupt(requisition_id):
    data = {"requisition_id": requisition_id}

    requests.post("http://127.0.0.1:8080/calc_bankrupt/", json=data, timeout=3)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, requisition_id):
    """
    Пользователь обновляет информацию о заявки
    """
    if not Requisition.objects.filter(pk=requisition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    requisition = Requisition.objects.get(pk=requisition_id)

    if requisition.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        requisition.status = 2
        requisition.save()
        if requisition.status == 2:
            requisition.date_formation = datetime.now()
            requisition.save()

    calculate_requisition_bankrupt(requisition_id)

    serializer = RequisitionSerializer(requisition)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, requisition_id):
    """
    Аналитик обновляет информацию о заявке
    """
    token = get_access_token(request)
    payload = get_jwt_payload(token)
    user_id = payload["user_id"]

    if not Requisition.objects.filter(pk=requisition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])
    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    requisition = Requisition.objects.get(pk=requisition_id)

    if requisition.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # requisition.status = request_status
    # requisition.date_complete = datetime.now()
    # requisition.moderator = CustomUser.objects.get(pk=user_id)
    # requisition.save()

    if request_status == 4:
        requisition.date_complete = None
    else:
        requisition.date_complete = datetime.now()

    requisition.status = request_status
    requisition.moderator = CustomUser.objects.get(pk=user_id)
    requisition.save()

    serializer = RequisitionSerializer(requisition, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_requisition(request, requisition_id):
    """
    Удаляет заявку
    """
    if not Requisition.objects.filter(pk=requisition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    requisition = Requisition.objects.get(pk=requisition_id)

    if requisition.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    requisition.status = 5
    requisition.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_company_from_requisition(request, requisition_id, company_id):
    """
    Удаляет компанию из заявки
    """
    if not Requisition.objects.filter(pk=requisition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Company.objects.filter(pk=company_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    requisition = Requisition.objects.get(pk=requisition_id)
    requisition.companies.remove(Company.objects.get(pk=company_id))
    requisition.save()

    return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(method="post", request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        message = {"message": "invalid credentials"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token,
    }

    response = Response(user_data, status=status.HTTP_201_CREATED)

    response.set_cookie(
        "access_token", access_token, httponly=False, expires=access_token_lifetime
    )

    return response


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    message = {
        "message": "User registered successfully",
        "user_id": user.id,
        "access_token": access_token,
    }

    response = Response(message, status=status.HTTP_201_CREATED)

    response.set_cookie(
        "access_token", access_token, httponly=False, expires=access_token_lifetime
    )

    return response


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if access_token not in cache:
        cache.set(access_token, access_token_lifetime)

    message = {"message": "Вы успешно вышли из аккаунта"}
    response = Response(message, status=status.HTTP_200_OK)

    response.delete_cookie("access_token")

    return response


@api_view(["GET"])
@permission_classes([])
def download_requisition_report(request, requisition_id):
    """
    Возвращает отчет в виде файла
    """
    if not Requisition.objects.filter(pk=requisition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    requisition = Requisition.objects.get(pk=requisition_id)

    if not requisition.report:
        return Response({"error": "Отчет не найден"}, status=status.HTTP_404_NOT_FOUND)

    file_path = os.path.join(settings.MEDIA_ROOT, requisition.report.name)

    if not os.path.isfile(file_path):
        return Response(
            {"error": "Файл отчета не существует"}, status=status.HTTP_404_NOT_FOUND
        )

    file_mime, _ = mimetypes.guess_type(file_path)
    file_mime = file_mime or "application/octet-stream"

    return FileResponse(
        open(file_path, "rb"),
        content_type=file_mime,
        as_attachment=True,
        filename=os.path.basename(file_path),
    )
