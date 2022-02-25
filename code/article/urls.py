from django.urls import path
from . import views
from django.contrib.auth import views as log
from django.contrib.sitemaps import GenericSitemap # new
from django.contrib.sitemaps.views import sitemap # new

urlpatterns = [
    path('', views.index, name='index'),
    path('tags/<str:curr_tag>/', views.tagPostShow, name='tags'),
    path('tags/', views.tagShow, name='tags'),
    path('<int:article_id>/', views.detail, name='detail'),
    # path('products/<int:product_id>/', views.detail, name='product_id'),
    # path('products/', views.product, name='product'),
    path('user/<int:user_id>/', views.articleById, name='user_id'),
    path('newarticle/', views.newArticle, name='newArticle'),
    path('editarticle/<int:article_id>', views.editArticle, name='editarticle'),
    path('deletearticle/<int:article_id>', views.deleteArticle, name='deletearticle'),
    path('register/', views.register, name='register'),
    path('login/', log.LoginView.as_view(), name='login'),
    path('logout/', log.LogoutView.as_view(), name='logout'),
    path('profilesettings/', views.edit, name='profilesettings'),
    path('password-change/', log.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', log.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', log.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', log.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', log.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', log.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]