from django.urls import path

from .views import *

urlpatterns = [
    # Набор методов для услуг
    path("api/companies/search/", search_company),  # GET
    path("api/companies/<int:company_id>/", get_company_by_id),  # GET
    path("api/companies/<int:company_id>/update/", update_company),  # PUT
    path("api/companies/<int:company_id>/delete/", delete_company),  # DELETE
    path("api/companies/create/", create_company),  # POST
    path("api/companies/<int:company_id>/add_to_requisition/", add_company_to_requisition),  # POST
    path("api/companies/<int:company_id>/image/", get_company_image),  # GET
    path("api/companies/<int:company_id>/update_image/", update_company_image),  # PUT
    
    # Набор методов для заявок
    path("api/requisitions/search/", get_requisitions),  # GET
    path("api/requisitions/<int:requisition_id>/", get_requisition_by_id),  # GET
    path("api/requisitions/<int:requisition_id>/update/", update_requisition),  # PUT/PATCH
    path("api/requisitions/<int:requisition_id>/update_status_user/", update_status_user),  # PUT
    path("api/requisitions/<int:requisition_id>/update_status_admin/",update_status_admin,),  # PUT
    path("api/requisitions/<int:requisition_id>/delete/", delete_requisition),  # DELETE
    path("api/requisitions/<int:requisition_id>/delete_company/<int:company_id>/", delete_company_from_requisition,),  # DELETE
    path("api/requisitions/<int:requisition_id>/download_report/", download_requisition_report,),  # GET
    
    # Набор методов для аутентификации и авторизации
    path("api/register/", register),
    path("api/login/", login),
    path("api/logout/", logout),
    path("api/check/", check),
]
