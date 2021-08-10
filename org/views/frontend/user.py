from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import Group


from org.forms.signup import SignupForm
from org.models import SiteAdmin

page = 'user'


class SignupView(View):

    def get(self, request, *args, **kwargs):
        form = SignupForm()
        context = {
            'page': page,
            'operation': "Signup",
            'form': form
        }
        return render(request, 'frontend/public/signup.html', context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = SignupForm(self.request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            site_admin = SiteAdmin.objects.create_user(username=email, email=email, password=password)
            user_group = Group.objects.get(name='User')
            user_group.user_set.add(site_admin)
            return redirect('/login')
        else:
            context = {
                'page': page,
                'operation': "Signup",
                'form': form
            }
            return render(request, 'frontend/public/signup.html', context)