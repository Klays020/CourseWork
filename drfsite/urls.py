"""drfsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth.views import LoginView
from testing_app.middleware import RedirectUnauthenticatedMiddleware
from django.urls import path, include, re_path
from django.contrib import admin
from django.urls import path, include

from testing_app.middleware import RedirectUnauthenticatedMiddleware
from testing_app.views import TestList, TestDetail, QuestionList, QuestionDetail, StudentTestList, StudentTestDetail, \
    SubmitStudentTestView, StudentTestDeleteView, UserDeleteView, CustomLogoutView, ListAllUrlsView, TestDetailView

urlpatterns = [
    path('', ListAllUrlsView.as_view(), name='list_all_urls'),
    #path('api/v1/drf-auth/login/', LoginView.as_view(), name='login'),

    path('admin/', admin.site.urls),
    path('api/tests/', TestList.as_view()),
    path('api/tests/<int:pk>/', TestDetail.as_view()),
    path('api/questions/', QuestionList.as_view()),
    path('api/questions/<int:pk>/', QuestionDetail.as_view()),
    path('api/tests/<int:pk>/', TestDetailView.as_view(), name='test-detail'),
    path('api/student-tests/', StudentTestList.as_view()),
    path('api/submit-test/<int:pk>/', SubmitStudentTestView.as_view(), name='submit_student_test'),
    path('api/student-tests/<int:pk>/', StudentTestDetail.as_view()),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),

    re_path(r'^auth/', include('djoser.urls.authtoken')),

    path('api/user/delete/<int:pk>/', UserDeleteView.as_view(), name='delete_user'),
    path('api/student-test/delete/<int:pk>/', StudentTestDeleteView.as_view(), name='delete_student_test'),
    path('api/logout/', CustomLogoutView.as_view(), name='custom_logout'),
]

