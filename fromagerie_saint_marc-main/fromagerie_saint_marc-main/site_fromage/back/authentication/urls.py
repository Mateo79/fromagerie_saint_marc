from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf import settings

from .views import ft_login, log_user, user_detail, signup, logout
from .views import edit_profile, get_user_by_id

from .views import item_detail, add_item, get_items, edit_item, delete_item

urlpatterns = [
    path('login/', log_user),
    path('signup/', signup),
    path('user_detail/', user_detail),
    path('get_user_by_id/<int:user_id>', get_user_by_id),
    path('logout/', logout),
    path('edit_profile/', edit_profile),
    path('add_item/', add_item),
    path('get_items/', get_items),
    path('edit_item/<int:item_id>/', edit_item),
    path('item_detail/<int:item_id>/', item_detail),
    path('delete_item/<int:item_id>/', delete_item),
]