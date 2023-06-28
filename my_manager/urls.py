"""
URL configuration for cdpc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .import views

urlpatterns = [
    path('login/',views.loginPage, name = "login"),
    path('logout/',views.logoutPage, name = "logout"),
    path('managers/',views.manager, name = "managers"),
    path('add_manager/',views.add_manager, name = "add_manager"),
    path('manager_detail/<str:pk_test3>/',views.manager_detail, name = "manager_detail"),
    path('manager_update/<str:pk_test3>/',views.manager_update, name = "manager_update"),
    path('manager_delete/<str:pk_test4>/',views.manager_delete, name = "manager_delete"),
    path('hpc/',views.hpcs, name = "hpc"),
    path('add_hpc/',views.add_hpc, name = "add_hpc"),
    path('update_hpc/<str:pk_test3>/',views.update_hpc, name = "hpc_update"),
    path('delete_hpc/<str:pk_test3>/',views.hpc_delete, name = "hpc_delete"),
    path('add_coordinator/',views.add_coordinator, name = "add_coordinator"),
    path('',views.home, name = "home"),
    path('user_page/',views.user_page, name = "user_page"),
    path('update_company_user/<str:pk_test2>/',views.update_company_user, name = "user_company_update"),
    path('coordinators/<str:pk>/',views.coordinators , name = "coordinator"),
    path('assign_company/<str:pk>/',views.assign_company , name = "assign_company"),
    path('assign_company_manager/<str:pk>/',views.assign_company_manager , name = "assign_company_manager"),
    path('companies/',views.companies , name = "companies"),
    path('company_detail/<str:pk>/',views.company_detail , name = "company_detail"),
    path('add_company/',views.add_company , name = "add_company"),
    path('update_company/<str:pk_test>/',views.update_company , name = "update_company"),
    path('delete_company/<str:pk_test1>/',views.delete_company , name = "delete_company"),
    path('update_coordinator/<str:pk_test2>/',views.update_coordinator , name = "update_coordinator"),
    path('delete_coordinator/<str:pk_test3>/',views.delete_coordinator , name = "delete_coordinator"),
    path('manager_user/',views.manager_user , name = "manager_user"),
]
