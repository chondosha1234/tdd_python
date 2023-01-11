from django.urls import path
from . import views

#app_name = 'lists'

urlpatterns = [
    path('<list_id>/', views.view_list, name='view_list'),
    path('<list_id>/add_item', views.add_item, name='add_item'),
    path('new', views.new_list, name='new_list')
]
