from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import Group

from org.forms.contact import ContactForm
from org.forms.signup import SignupForm
from org.models import SiteAdmin

page = 'contact'


class ContactView(View):

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'page': page,
            'operation': "Contact",
            'form': form
        }
        return render(request, 'frontend/public/contact.html', context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = ContactForm(self.request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            name = form.cleaned_data.get('name')
            send_mail(
                name,
                message,
                'projectburt@outlook.com',
                [email],
                fail_silently=False,
            )
        else:
            context = {
                'page': page,
                'operation': "Contact",
                'form': form
            }
            return render(request, 'frontend/public/signup.html', context)