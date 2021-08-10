from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from org.models import Event, EventPerson, EventOrganization
from org.views.helper import get_formatted_date

page = 'event'


# class EventListView(PermissionRequiredMixin, View):
class EventListView(View):
    # permission_required = 'org.view_event'
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        return render(request, "frontend/event/events2.html", {'page': page})


class EventListJson(BaseDatatableView):
    login_url = '/login'
    model = Event
    # define the columns that will be returned
    columns = ['slug', 'name', 'start_date_year', 'end_date_year', 'venue_city']
    order_columns = ['name', 'venue_city']

    max_display_length = 50

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            location = ""
            city = ""
            if item.venue_city is not None:
                city = item.venue_city.name
            country = ""
            if item.venue_country is not None:
                country = item.venue_country.name
            if country != "" and city != "":
                location = city + ", " + country

            json_data.append([
                escape("{0}".format(str(item.slug))),
                escape("{0}".format(item.name)),
                escape(get_formatted_date(item.start_date_year, item.start_date_month, item.start_date_day)),
                escape(get_formatted_date(item.end_date_year, item.end_date_month, item.end_date_day)),
                escape("{0}".format(location)),
            ])
        return json_data


# class EventDetailView(PermissionRequiredMixin, View):
class EventDetailView(View):
    # permission_required = 'org.view_event'
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        event = Event.objects.get(slug=slug)
        event_speakers = EventPerson.objects.filter(event=event, appearance_type__name='Speaker')
        event_organizers = EventPerson.objects.filter(event=event, appearance_type__name='Organizer')
        event_sponsors = EventPerson.objects.filter(event=event, appearance_type__name='Sponsor')
        event_exhibitors = EventPerson.objects.filter(event=event, appearance_type__name='Exhibitor')

        event_org_speakers = EventOrganization.objects.filter(event=event, appearance_type__name='Speaker')
        event_org_organizers = EventOrganization.objects.filter(event=event, appearance_type__name='Organizer')
        event_org_sponsors = EventOrganization.objects.filter(event=event, appearance_type__name='Sponsor')
        event_org_exhibitors = EventOrganization.objects.filter(event=event, appearance_type__name='Exhibitor')

        context = {
            'page': page,
            'event': event,
            'start_date': get_formatted_date(event.start_date_year, event.start_date_month,
                                             event.start_date_day),
            'end_date': get_formatted_date(event.end_date_year, event.end_date_month,
                                           event.end_date_day),

            'event_speakers': event_speakers,
            'event_organizers': event_organizers,
            'event_sponsors': event_sponsors,
            'event_exhibitors': event_exhibitors,

            'event_org_speakers': event_org_speakers,
            'event_org_organizers': event_org_organizers,
            'event_org_sponsors': event_org_sponsors,
            'event_org_exhibitors': event_org_exhibitors
        }
        return render(request, "frontend/event/event_details2.html", context)
