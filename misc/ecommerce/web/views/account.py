from django.views.generic import CreateView,View
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme
from web.models import User
from web.forms.account import SignInForm


class SignIn(CreateView):
    template_name = "web/account/index.html"
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect( reverse('web:home' ) )
        
        cache.set('next', request.GET.get('next', None))
        datas = { 'form' : SignInForm() }
        return render(request, self.template_name, datas)

    def post(self, request, *args, **kwargs):
        datas = {}
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
            if user is not None and user.is_active:
                login(self.request, user)
                next_url = cache.get('next')
                if next_url:
                    cache.delete('next')
                    if not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                        return HttpResponseRedirect(reverse('web:home'))
                    else:
                        return HttpResponseRedirect(next_url)
                else:
                    return HttpResponseRedirect(reverse('web:home'))
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect( reverse('web:signin') )
        else:
            email = request.POST.get('email')
            if User.objects.filter(email=email, is_active=False).exists():
                messages.error(request,"Your account is not active")
            else:
                if not request.POST.get('email'):
                    messages.error(request,"Email is required")
                elif not request.POST.get('password'):
                    messages.error(request,"Password is required")
                else:
                    messages.error(request,"Invalid Login Details")
        datas['form'] = form
        return render(request, self.template_name, datas)


class Home(LoginRequiredMixin,View):
    template_name = "web/account/home.html"
    def get(self, request, *args, **kwargs):
        # if self.request.user.is_authenticated:
        #     return HttpResponseRedirect( reverse('appswift:home' ) )
        cache.set('next', request.GET.get('next', None))
        
        datas = { 'form' : SignInForm(), 'userrr':self.request.user.email}
        return render(request, self.template_name, datas)
        
class SignOut(CreateView):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        request.session.flush()
        return HttpResponseRedirect( reverse('web:signin') )