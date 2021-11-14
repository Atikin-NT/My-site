from django.urls import path
from . import views
from django.contrib.auth import views as log

urlpatterns = [
    path('', views.index, name='index'),
    path('tags/', views.tagShow, name='tags'),
    path('tags/<str:curr_tag>/', views.tagPostShow, name='tags'),
    path('<int:article_id>/', views.detail, name='detail'),
    path('products/<int:product_id>/', views.detail, name='product_id'),
    path('articles/<int:user_id>/', views.articleById, name='user_id'),
    path('newarticle/', views.newArticle, name='newArticle'),
    path('register/', views.register, name='register'),
    path('login/', log.LoginView.as_view(), name='login'),
    path('logout/', log.LogoutView.as_view(), name='logout'),
    path('edit/', views.edit, name='edit'),
    path('password-change/', log.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', log.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', log.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', log.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', log.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', log.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]