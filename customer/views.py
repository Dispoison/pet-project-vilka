from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from customer.forms import SignUpForm, SignInForm
from shop.utils.mixins.view_data_mixin import ViewDataMixin


class SignUpView(ViewDataMixin, CreateView):
    form_class = SignUpForm
    template_name = 'customer/sign_up.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        mixin_context = self.get_mixin_context()
        return base_context | mixin_context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class SignInView(ViewDataMixin, LoginView):
    form_class = SignInForm
    template_name = 'customer/sign_in.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        mixin_context = self.get_mixin_context()
        return base_context | mixin_context


def sign_out(request):
    logout(request)
    return redirect('home')
