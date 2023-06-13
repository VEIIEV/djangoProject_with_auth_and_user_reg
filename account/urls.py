from django.urls import path, include
from django.contrib.auth import views as auth_views

from account import views

urlpatterns = [

    # базовый метод входа
    # path('login/', views.user_login, name= 'login')

    # вызов шаблонов аутентификации

    # TODO: изменить каталоги регистрации что бы по путям находило верные штмл шаблоны

    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # # url-адреса смены пароля
    # path('password-change/',
    #      auth_views.PasswordChangeView.as_view(),
    #      name='password_change'),
    # path('password-change/done/',
    #      auth_views.PasswordChangeDoneView.as_view(),
    #      name='password_change_done'),
    #
    # # url-адреса сброса пароля
    # path('password-reset/',
    #      auth_views.PasswordResetView.as_view(),
    #      name='password_reset'),
    # path('password-reset/done/',
    #      auth_views.PasswordResetDoneView.as_view(),
    #      name='password_reset_done'),
    # path('password-reset/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(),
    #      name='password_reset_confirm'),
    # path('password-reset/complete/',
    #      auth_views.PasswordResetCompleteView.as_view(),
    #      name='password_reset_complete'),

    # средства джанго не работают, закоммиченный код работает, хз что не так
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),

]
