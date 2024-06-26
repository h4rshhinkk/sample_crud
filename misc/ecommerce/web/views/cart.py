from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from django.urls import reverse
from web.forms.product import *
from web.helper import renderfile, is_ajax, LogUserActivity
from web.models import Category,Product,Cart
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import *
from web.constantvariables import PAGINATION_PERPAGE
from django.shortcuts import get_object_or_404,render,redirect
from django.db import transaction
from django.db.models import Q


class CartView(LoginRequiredMixin, View):
    template_name = "web/product/cart.html"
    def get(self, request):
        user = self.request.user
        cart_items = Cart.objects.filter(user=user)
        cart_total = float(sum(item.get_total_price() for item in Cart.objects.filter(user=user)))

        context = {
            "cart_items": cart_items,
            "cart_total": cart_total,
        }
        return render(request, self.template_name, context)



class AddToCartView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'User not authenticated'}, status=401)
        user = self.request.user
        quantity = request.GET.get('quantity', 1)
        is_cart=request.GET.get("update",'')
        print(is_cart,"==========")
        product_id = request.GET.get("product_id",'')
        product = get_object_or_404(ProductVariant, pk=product_id)

        cart_item, created = Cart.objects.get_or_create(
            user=user,
            product=product,
            defaults=({"quantity": quantity})
        )

        if not created:
            if is_cart:
                cart_item.quantity = int(quantity)
            else:
                cart_item.quantity += int(quantity)
            cart_item.save()
        return JsonResponse({
            'message': 'Product Quantity Added from cart successfully',
            'quantity':cart_item.quantity,
            'total_price':cart_item.get_total_price(),
            'cart_total':cart_item.cart_total(),
            'cart_count':Cart.objects.filter(user=request.user).count(),
        })