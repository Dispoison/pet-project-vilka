from django.urls import path

from customer.views import *

urlpatterns = [
    path('sign-in', SignInView.as_view(), name='sign-in'),
    path('sign-out', sign_out, name='sign-out'),
    path('sign-up', SignUpView.as_view(), name='sign-up'),
]





