from django.shortcuts import render
from django.views import View
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

from org.models import Acquisition
from org.views.helper import get_formatted_date

page = 'acquisition'


class AcquisitionListView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "frontend/acquisition/acquisitions2.html", {'page': page})


class AcquisitionListJson(BaseDatatableView):
    model = Acquisition
    # define the columns that will be returned
    columns = ['slug', 'transaction_name', 'acquiring_organization', 'acquired_organization', 'announced_date_year']
    order_columns = ['slug', 'transaction_name']

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            json_data.append([
                escape("{0}".format(str(item.slug))),
                escape("{0}".format(item.transaction_name)),

                escape("{0}".format(item.acquired_organization.name)),
                escape("{0}".format(item.acquiring_organization.name)),

                escape(
                    get_formatted_date(item.announced_date_year, item.announced_date_month, item.announced_date_day)),

                # extra
                escape("{0}".format(item.acquired_organization.id)),
                escape("{0}".format(item.acquiring_organization.id))
            ])
        return json_data


class AcquisitionDetailView(View):

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        acquisition = Acquisition.objects.get(slug=slug)
        print(acquisition.acquisitionnews_set.all())
        context = {
            'page': page,
            'acquisition': acquisition,
            'announced_date': get_formatted_date(acquisition.announced_date_year, acquisition.announced_date_month,
                                                 acquisition.announced_date_day)
        }
        return render(request, "frontend/acquisition/acquisition_details2.html", context)
