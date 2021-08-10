from django.shortcuts import render
from django.views import View
from org.models import LibraryContent, LibraryContentType
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

from org.views.helper import get_formatted_date

page = 'library'


class LibraryListView(View):

    def get(self, request, *args, **kwargs):
        types = LibraryContentType.objects.all().order_by('name')
        return render(request, "frontend/library/library_list.html", {'types': types, 'page': page})


class LibraryListJson(BaseDatatableView):

    columns = ['slug', 'title', 'short_description', 'short_description', 'short_description', 'short_description']
    order_columns = ['title', 'slug']

    max_display_length = 50

    def get_initial_queryset(self):
        l_type = self.request.GET.get('type')
        return LibraryContent.objects.filter(content_type__name=l_type)

    def prepare_results(self, qs):

        json_data = []
        for item in qs:
            ps = []
            ps2 = []
            for c in item.librarycontentperson_set.all():
                if c.type == "author" or c.type == "host":
                    ps.append({'name': c.person.first_name + " " + c.person.last_name, 'slug': c.person.slug})
                elif c.type == "guest":
                    ps2.append({'name': c.person.first_name + " " + c.person.last_name, 'slug': c.person.slug})
            json_data.append([
                escape("{0}".format(str(item.slug))),
                escape("{0}".format(item.title)),
                escape("{0}".format(item.short_description)),
                escape(get_formatted_date(item.date_year, item.date_month, item.date_day)),
                ps,
                ps2,
                # extra
                escape("{0}".format(item.url)),
            ])
        return json_data