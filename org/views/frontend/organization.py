from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views import View
from org.models import Organization, FundingRound
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from org.views.helper import get_formatted_date


class OrganizationListView(PermissionRequiredMixin, View):
    permission_required = 'org.view_organization'
    login_url = '/login'
    page = 'organization'

    def get(self, request, *args, **kwargs):
        return render(request, "frontend/organization/organizations2.html", {'page': self.page})


class OrganizationListJson(PermissionRequiredMixin, BaseDatatableView):
    permission_required = 'org.view_organization'
    login_url = '/login'

    model = Organization
    columns = ['id', 'name', 'description', 'description', 'city', 'founded_date_year']
    order_columns = ['name', 'description']

    max_display_length = 50

    def get_initial_queryset(self):
        return Organization.objects.filter(organization_type='Company')

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            o_cats = []
            for c in item.organizationhascategory_set.all():
                o_cats.append(c.category.name)
            city = ""
            if item.city is not None:
                city = item.city.name
            json_data.append([
                escape("{0}".format(str(item.id))),
                escape("{0}".format(item.name)),
                escape("{0}".format(item.description)),
                escape("{0}".format(', '.join(o_cats))),
                escape("{0}".format(city)),
                escape("{0}".format(get_formatted_date(item.founded_date_year, item.founded_date_month,
                                                       item.founded_date_day))),
            ])
        return json_data


class OrganizationDetailView(PermissionRequiredMixin, View):

    permission_required = 'org.view_organization'
    login_url = '/login'

    page = 'organization'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        organization = Organization.objects.get(pk=pk)
        # industry_categories = PlatformCategory.objects.filter(platform=platform)
        # existing = []
        # for ic in industry_categories:
        #     existing.append(str(ic.category_id))
        # form = PlatformForm(initial={'industry_categories': existing}, instance=platform)
        print(organization.acquiring_organization.all())
        exits_count = FundingRound.objects.filter(investee_organization=organization).exclude(closed_date_year='').count()
        context = {
            'page': self.page,
            'organization': organization,
            'founded_date': get_formatted_date(organization.founded_date_year, organization.founded_date_month,
                                               organization.founded_date_day),
            'closed_date': get_formatted_date(organization.closed_date_year, organization.closed_date_month,
                                              organization.closed_date_day),
            'ipo_date': get_formatted_date(organization.ipo_date_year, organization.ipo_date_month,
                                           organization.ipo_date_day),
            'exits_count': exits_count
        }
        return render(request, "frontend/organization/organization_details2.html", context)
