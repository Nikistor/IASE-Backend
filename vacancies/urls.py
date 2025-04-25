from django.urls import path

from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/companies/search/', search_company),  # GET
    path('api/companies/<int:company_id>/', get_company_by_id),  # GET
    path('api/companies/<int:company_id>/update/', update_company),  # PUT
    path('api/companies/<int:company_id>/delete/', delete_company),  # DELETE
    path('api/companies/create/', create_company),  # POST
    path('api/companies/<int:company_id>/add_to_vacancy/', add_company_to_vacancy),  # POST
    path('api/companies/<int:company_id>/image/', get_company_image),  # GET
    path('api/companies/<int:company_id>/update_image/', update_company_image),  # PUT

    # Набор методов для заявок
    path('api/vacancies/search/', get_vacancies),  # GET
    path('api/vacancies/<int:vacancy_id>/', get_vacancy_by_id),  # GET
    path('api/vacancies/<int:vacancy_id>/update/', update_vacancy),  # PUT/PATCH
    path('api/vacancies/<int:vacancy_id>/update_bankrupt/', update_vacancy_bankrupt),  # POST
    path('api/vacancies/<int:vacancy_id>/update_status_user/', update_status_user),  # PUT
    path('api/vacancies/<int:vacancy_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/vacancies/<int:vacancy_id>/delete/', delete_vacancy),  # DELETE
    path('api/vacancies/<int:vacancy_id>/delete_company/<int:company_id>/', delete_company_from_vacancy),  # DELETE

    # Набор методов для аутентификации и авторизации
    path("api/register/", register),
    path("api/login/", login),
    path("api/logout/", logout)
]