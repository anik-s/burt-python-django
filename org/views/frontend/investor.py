from django.shortcuts import render
from django.views import View
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

from org.models import Organization, Person, FundingRoundInvestorOrganization, FundingRoundInvestor


class InvestorListView(View):
    page = 'investor'

    def get(self, request, *args, **kwargs):
        return render(request, "frontend/investor/investors2.html", {'page': self.page})


class InvestorOrganizationListJson(BaseDatatableView):
    model = Organization
    columns = ['id', 'name', 'description', 'description', 'city']
    order_columns = ['name', 'description']

    max_display_length = 50

    def get_initial_queryset(self):
        return Organization.objects.filter(organization_type='Investment Firm')

    def prepare_results(self, qs):
        json_data = []
        for item in qs:

            # location
            location = ""
            city = ""
            if item.city is not None:
                city = item.city.name
            country = ""
            if item.country is not None:
                country = item.country.name
            if country != "" and city != "":
                location = city + ", " + country
            # investments count
            investments_count = FundingRoundInvestorOrganization.objects.filter(investor_organization=item).count()
            # exits count
            exists_count = FundingRoundInvestorOrganization.objects.filter(investor_organization=item) \
                .exclude(funding_round__closed_date_year="").count()

            json_data.append([
                escape("{0}".format(str(item.id))),
                escape("{0}".format(item.name)),
                escape("{0}".format(investments_count)),
                escape("{0}".format(exists_count)),
                escape("{0}".format(location))
            ])
        return json_data


class InvestorPersonListJson(BaseDatatableView):
    model = Person
    columns = ['id', 'first_name', 'type', 'type', 'city']
    order_columns = ['name', 'first_name']

    max_display_length = 50

    def get_initial_queryset(self):
        return Person.objects.filter(type='Individual Investor')

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            # location
            location = ""
            city = ""
            if item.city is not None:
                city = item.city.name
            country = ""
            if item.country is not None:
                country = item.country.name
            if country != "" and city != "":
                location = city + ", " + country
            # investments count
            investments_count = FundingRoundInvestor.objects.filter(person=item).count()
            # exits count
            exists_count = FundingRoundInvestor.objects.filter(person=item)\
                .exclude(funding_round__closed_date_year="").count()
            json_data.append([
                escape("{0}".format(str(item.id))),
                escape("{0} {1}".format(item.first_name, item.last_name)),
                escape("{0}".format(investments_count)),
                escape("{0}".format(exists_count)),
                escape("{0}".format(location)),
            ])
        return json_data
