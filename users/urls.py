from django.urls import path

from .views import (MyTokenObtainPairView, RegisterUser, UserProfile,
                    UsersDetail, UsersList)

urlpatterns = [
    path('users/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/register', RegisterUser.as_view(), name='register'),
    path('users/profile/', UserProfile.as_view(), name='user_profile'),
    path('users/list/', UsersList.as_view(), name = 'users-list'),
    path('users/list/<int:pk>/', UsersDetail.as_view(), name = 'users-datail'),
]
