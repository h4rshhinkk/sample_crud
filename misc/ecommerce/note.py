#https://stackoverflow.com/questions/63410160/how-do-i-toggle-boolean-field
#https://www.youtube.com/watch?v=QTP2UXgPi7U

#https://github.com/celikyuksell/Django-E-Commerce/blob/master/product/models.py
#https://github.com/SteinOveHelset/saulgadgets/blob/master/apps/store/models.py

#https://github.com/celikyuksell/Django-E-Commerce/blob/master/README.md


#https://stackoverflow.com/questions/59448563/django-fetch-related-child-with-parent-object?rq=3

#https://docs.djangoproject.com/en/3.0/ref/models/querysets/#prefetch-related


# class ProductView(View):
#     def get(self, request, *args, **kwargs):
#         context, response = {}, {}
#         page = int(request.GET.get('page', 1))
#         products = Product.objects.filter(is_active=True).select_related('productmedia')

#         # Get the default product media image for each product
#         default_media_images = []
#         for product in products:
#             default_media = product.productmedia_set.filter(is_default=True).first()
#             if default_media:
#                 default_media_images.append(default_media.image)

#https://www.redswitches.com/blog/drop-postgresql-database-examples/#HowToDropAPostgreSQLDatabase
#https://www.redswitches.com/blog/creating-users-in-postgresql/#Grant-User-Privileges
#https://docs.djangoproject.com/en/5.0/topics/auth/default/#topics-auth-creating-users

# GRANT privilege_name ON ecommerce TO postgres;
# grant all privileges on database ecommerce to harshin_user;