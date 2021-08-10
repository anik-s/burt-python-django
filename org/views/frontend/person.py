from django.shortcuts import render
from django.views import View
from org.models import Organization, Person, PersonJob
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from org.views.helper import get_formatted_date

page = 'person'


class PersonListView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "frontend/person/persons2.html", {'page': page})


class PersonListJson(BaseDatatableView):
    model = Person
    columns = ['slug', 'first_name', 'type', 'type', 'city']
    order_columns = ['name', 'first_name']

    max_display_length = 50

    def get_initial_queryset(self):
        return Person.objects.filter(type='Person')

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            location = ""
            city = ""
            if item.city is not None:
                city = item.city.name
            country = ""
            if item.country is not None:
                country = item.country.name
            if country != "" and city != "":
                location = city + ", " + country
            p_jobs = PersonJob.objects.filter(person=item).order_by('-start_date')[:1]
            p_job_title = "-"
            p_job_org = "-"
            if (len(p_jobs)) > 0:
                p_job_title = p_jobs[0].title
                p_job_org = p_jobs[0].organization.name
            json_data.append([
                escape("{0}".format(str(item.slug))),
                escape("{0} {1}".format(item.first_name, item.last_name)),
                escape("{0}".format(p_job_title)),
                escape("{0}".format(p_job_org)),
                escape("{0}".format(location)),
            ])
        return json_data


class PersonDetailView(View):

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        person = Person.objects.get(slug=slug)
        current_jobs_count = PersonJob.objects.filter(has_end_date=False).count()
        past_jobs_count = PersonJob.objects.filter(has_end_date=True).count()
        context = {
            'page': page,
            'person': person,
            'current_jobs_count': current_jobs_count,
            'past_jobs_count': past_jobs_count
        }
        return render(request, "frontend/person/person_details2.html", context)