from django.urls import path
from . import views

app_name = 'firstapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<str:post_name>/', views.categoryShort, name='home'),
    path('adminpage/', views.adminpage, name='adminPage'),
    path('post/<int:post_id>/', views.postview, name='postDetail'),
    path('adminlogin/', views.login, name='adminlogin'),
    path('logout/', views.logout_view, name='logout'),
    path('delete_post/', views.delete_post, name='delete_post'),
path('add_category/', views.add_category, name='add_category'),
]
