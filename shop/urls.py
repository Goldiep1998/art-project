from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('gallery', views.gallery, name='gallery'),
    path('image-info/<int:id>', views.image_info, name='image-info'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('buy/<int:id>', views.buy, name='buy'),
    path('about', views.about, name='about'),
    path('cart', views.cart, name='cart'),
    path('addtocart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('order/<int:id>', views.order, name='order'),
    path('order_list', views.order_list, name='order_list'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('removeitem/<int:id>', views.remove_item, name='remove_item'),
    path('admin_flag/<int:id>', views.admin_flag, name='admin_flag'),
    path('flagged_images', views.flagged_images, name='flagged_images'),
    path('remove-flag/<int:id>', views.remove_flag, name='remove_flag'),

]