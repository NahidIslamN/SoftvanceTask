from django.urls import path
from .views import *

urlpatterns = [
    path('auth/signup/', SignUp.as_view(), name="signup" ),
    path('auth/login/', SignIn.as_view(), name="login" ),
    path('auth/profile/', MyProfile.as_view(), name='profile'),
    path('employers/', EmployerView.as_view(), name='employees'),
    path('employers/<pk>/',EmployerDetails.as_view(), name='employee' ),
    path('auth/logout/', LogOut.as_view(), name='logout')


]
