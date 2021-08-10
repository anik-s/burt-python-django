from django.urls import path
from django.contrib.auth import views as auth_views

from .forms.user_login import UserLoginForm
from .views.frontend.acquisition import AcquisitionListJson, AcquisitionListView, AcquisitionDetailView
from .views.frontend.contact import ContactView
from .views.frontend.event import EventListJson, EventListView, EventDetailView
from .views.frontend.funding_round import FundingRoundListJson, FundingRoundListView, FundingRoundDetailView
from .views.frontend.home import HomeView, PublicLoginView
from .views.frontend.investor import InvestorOrganizationListJson, InvestorListView, InvestorPersonListJson
from .views.frontend.library import LibraryListJson, LibraryListView
from .views.frontend.news import NewsListView, NewsListJson
from .views.frontend.organization import OrganizationListJson, OrganizationListView, OrganizationDetailView
from .views.frontend.person import PersonListJson, PersonListView, PersonDetailView
from .views.frontend.platform import PlatformListJson, PlatformListView, PlatformDetailView
from .views.frontend.user import SignupView
from .views.not_found import not_found


urlpatterns = [

    # platform
    path('platforms/datatable-data', PlatformListJson.as_view(), name='platform_list_json'),
    path('platforms/<pk>', PlatformDetailView.as_view(), name='platform_detail'),
    path('platforms', PlatformListView.as_view(), name='platform_list'),

    # investor
    path('investor-organizations/datatable-data', InvestorOrganizationListJson.as_view(),
         name='investor_organization_list_json'),
    path('investor-persons/datatable-data', InvestorPersonListJson.as_view(), name='investor_person_list_json'),
    path('investors', InvestorListView.as_view(), name='investor_list'),

    # organization
    path('organizations/datatable-data', OrganizationListJson.as_view(), name='organization_list_json'),
    path('organizations/<pk>', OrganizationDetailView.as_view(), name='organization_detail'),
    path('organizations', OrganizationListView.as_view(), name='organization_list'),

    # person
    path('persons/datatable-data', PersonListJson.as_view(), name='person_list_json'),
    path('persons/<slug>', PersonDetailView.as_view(), name='person_detail'),
    path('persons', PersonListView.as_view(), name='person_list'),

    # acquisition
    path('acquisitions/datatable-data', AcquisitionListJson.as_view(), name='acquisition_list_json'),
    path('acquisitions/<slug>', AcquisitionDetailView.as_view(), name='acquisition_detail'),
    path('acquisitions', AcquisitionListView.as_view(), name='acquisition_list'),

    # event
    path('events/datatable-data', EventListJson.as_view(), name='event_list_json'),
    path('events/<slug>', EventDetailView.as_view(), name='event_detail'),
    path('events', EventListView.as_view(), name='event_list'),

    # funding_round
    path('funding_rounds/datatable-data', FundingRoundListJson.as_view(), name='funding_round_list_json'),
    path('funding_rounds/<slug>', FundingRoundDetailView.as_view(), name='funding_round_detail'),
    path('funding_rounds', FundingRoundListView.as_view(), name='funding_round_list'),

    # news
    path('news/datatable-data', NewsListJson.as_view(), name='news_list_json'),
    path('news', NewsListView.as_view(), name='news_list'),

    # library
    path('library/datatable-data', LibraryListJson.as_view(), name='library_list_json'),
    path('library', LibraryListView.as_view(), name='library_list'),

    # home
    path('', HomeView.as_view(), name='home'),

    # user
    path('signup', SignupView.as_view(), name='signup'),
    path('contact', ContactView.as_view(), name='contact'),
    path('login',
         auth_views.LoginView.as_view(template_name='frontend/home/login.html', extra_context={'operation': 'Login'},
                                      authentication_form=UserLoginForm)),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login')),

]
