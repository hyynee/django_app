from django.urls import path
from . import views

urlpatterns = [
    path('products',views.products, name='products'),
    path('product/<id>',views.product_detail, name='product'),
    path('view_cart', views.view_cart, name='view_cart'), 
    path('add_item', views.add_product_to_cart, name='add_item'),
    path('update_item', views.update_cart_item_quantity, name='update_item'),
    path('delete_item', views.delete_item, name='delete_item'),
]
