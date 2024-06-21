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
    path('product/create/',ProductCreate.as_view(),name='create_product')

]