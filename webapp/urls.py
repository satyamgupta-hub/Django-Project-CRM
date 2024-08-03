from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="homepage"),
    path('register/',views.register,name="registerpage"),
    path('login/',views.login,name="loginpage"),
    path('logout/',views.logoutUser,name="logoutpage"),
    # cruds
    path('dashboard/',views.dashboardView,name="dashboardpage"),
    path('create-record/',views.create_record,name="createrecordpage"),
    path('update-record/<int:pk>',views.update_record,name="updaterecordpage"),
    path('views-record/<int:pk>',views.view_single_record,name="viewrecordpage"),
    path('delete-record/<int:pk>',views.delete_record,name="deleterecordpage"),
]
