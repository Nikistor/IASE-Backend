from rest_framework import serializers
from .models import *


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Company
        # Поля, которые мы сериализуем (Все поля)
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'is_moderator')


class VacancySerializer(serializers.ModelSerializer):
    companies = CompanySerializer(read_only=True, many=True)
    employer = UserSerializer(read_only=True, many=False)
    moderator = UserSerializer(read_only=True, many=False)
    report_url = serializers.SerializerMethodField()

    class Meta:
        model = Vacancy
        fields = [
            'id',
            'name',
            'status',
            'date_created',
            'date_formation',
            'date_complete',
            'bankrupt',
            'employer',
            'moderator',
            'companies',
            'report',
            'report_url',
        ]
        read_only_fields = ['id', 'date_created']

    def get_report_url(self, obj):
        if obj.report:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.report.url)
            # Если request отсутствует, вернуть относительный URL
            return obj.report.url
        return None

class VacanciesSerializer(serializers.ModelSerializer):
    employer = UserSerializer(read_only=True, many=False)
    moderator = UserSerializer(read_only=True, many=False)

    class Meta:
        # Модель, которую мы сериализуем
        model = Vacancy
        # Поля, которые мы сериализуем (Все поля)
        fields = '__all__'


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

