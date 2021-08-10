import datetime
from django.shortcuts import render
from django.views import View

from org.models import News, Event, LibraryContent


class HomeView(View):

    def get(self, request, *args, **kwargs):
        featured_news = News.objects.filter(featured=True).order_by('-published_date')[:5]
        non_featured_news = News.objects.filter(featured=False).order_by('-published_date')[:4]
        events = Event.objects.filter(start_date__gte=datetime.datetime.now()).order_by('start_date')[:4]
        library_contents = LibraryContent.objects.filter().order_by('-date')[:4]
        context = {
            'featured_news': featured_news,
            'non_featured_news': non_featured_news,
            'events': events,
            'library_contents': library_contents,
            'operation': "Home"
        }
        return render(request, 'frontend/home/_content.html', context)


class PublicLoginView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'operation': "Login"
        }
        return render(request, 'frontend/home/login.html', context)
