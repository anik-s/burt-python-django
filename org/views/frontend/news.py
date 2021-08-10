from django.shortcuts import render
from django.views import View
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.contrib.auth.mixins import PermissionRequiredMixin
from org.models import News
from org.views.helper import get_formatted_date

page = 'news'


class NewsListView(PermissionRequiredMixin, View):
    permission_required = 'org.view_news'
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        return render(request, "frontend/news/news2.html", {'page': page})


class NewsListJson(PermissionRequiredMixin, BaseDatatableView):
    permission_required = 'org.view_news'
    login_url = '/login'
    model = News
    # define the columns that will be returned
    columns = ['id', 'title', 'publisher', 'date_year']
    order_columns = ['id', 'title', 'publisher']

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            json_data.append([
                escape("{0}".format(str(item.id))),
                escape("{0}".format(item.title)),
                escape("{0}".format(item.publisher)),
                escape(get_formatted_date(item.date_year, item.date_month, item.date_day)),
                # extra
                escape("{0}".format(item.url)),
            ])
        return json_data