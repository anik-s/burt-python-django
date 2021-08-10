from django.shortcuts import render
from django.views import View
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from org.models import FundingRound
from org.views.helper import get_formatted_date

page = 'funding_round'


class FundingRoundListView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "frontend/funding_round/funding_rounds2.html", {'page': page})


class FundingRoundListJson(BaseDatatableView):
    model = FundingRound
    columns = ['slug', 'transaction_name', 'investee_organization', 'funding_type', 'money_raised', 'announced_date_year']
    order_columns = ['transaction_name', 'investee_organization']

    max_display_length = 50

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            c = item.money_raised_currency.name if item.money_raised_currency is not None else ""
            m = item.money_raised if item.money_raised is not None else ""
            mr = c + " " + str(m)
            json_data.append([
                escape("{0}".format(str(item.slug))),
                escape("{0}".format(item.transaction_name)),
                escape("{0}".format(item.investee_organization.name)),
                escape("{0}".format(item.funding_type.name)),
                escape("{0}".format(mr)),
                escape("{0}".format(get_formatted_date(item.announced_date_year, item.announced_date_month,
                                                       item.announced_date_day))),

                # extra
                escape("{0}".format(item.investee_organization.id)),
            ])
        return json_data


class FundingRoundDetailView(View):

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        funding_round = FundingRound.objects.get(slug=slug)
        org_investors_count = funding_round.fundingroundinvestororganization_set.all().count()
        individual_investors_count = funding_round.fundingroundinvestor_set.all().count()

        org_partner_investors_count = funding_round.fundingroundinvestororganization_set.filter(lead_investor=False).count()
        individual_partner_investors_count = funding_round.fundingroundinvestor_set.filter(lead_investor=False).count()

        total_investors = org_investors_count + individual_investors_count
        total_partner_investors = org_partner_investors_count + individual_partner_investors_count

        has_investors = False
        if total_investors > 0:
            has_investors = True

        context = {
            'page': page,
            'funding_round': funding_round,
            'announced_date': get_formatted_date(funding_round.announced_date_year, funding_round.announced_date_month,
                                               funding_round.announced_date_day),
            'closed_date': get_formatted_date(funding_round.closed_date_year, funding_round.closed_date_month,
                                              funding_round.closed_date_day),
            'total_investors': total_investors,
            'total_partner_investors': total_partner_investors,
            'has_investors': has_investors
        }
        return render(request, "frontend/funding_round/funding_details2.html", context)