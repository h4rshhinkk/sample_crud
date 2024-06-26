from django.urls import path
from web.views.account import *
from web.views.category import *
from web.views.product import *
app_name = "web"

# views
urlpatterns = [
    # Landing Page
    path("", Home.as_view(), name="home"),

    #Category
    path('category/', CategoryView.as_view(), name='category'),
    path('category/create/', CategoryCreate.as_view(), name='create_category'),
    path('category/<int:pk>/update/', CategoryUpdate.as_view(), name='update_category'),
    path('category/<int:pk>/delete/', CategoryDelete.as_view(), name='delete_category'),
    path('category/<int:pk>/view/', CategoryDetail.as_view(), name='view_category'),
    
    #category disable enable fun()
    path('changestatus/', change_status, name="change_status"),
    
    #Product
    path('product/', ProductView.as_view(), name='product'),
    path('product/create/',ProductCreate.as_view(),name='create_product'),
    path('product/<int:pk>/update/', ProductUpdate.as_view(), name='update_product'),
    path('product/<int:pk>/delete/', ProductDelete.as_view(), name='delete_product'),

    #list
    path('product_image/', ProductImageView.as_view(), name='product_image'),


    #search
    path('search/',search,name="search"),

    #variant
    path('product/varaint/',ProductVariantView.as_view(), name='product_variant'),
    path('product/variant/create/',ProductVariantCreate.as_view(),name='product_variant_create')
    
]