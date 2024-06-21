from django.views.generic import CreateView,View
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render




class Home(View):
    template_name = "web/account/home.html"
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect( reverse('web:home' ) )
        return render(request, self.template_name)