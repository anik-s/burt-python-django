from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import formset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

from org.forms.library_content import LibraryContentForm, LibraryMentionFormSet, LibraryContentPersonForm, \
    LibraryContentPersonFormSet, LibraryContentMentionForm
from org.models import LibraryContent, PersonLibraryContent, OrganizationLibraryContent, FundingLibraryContent, \
    PlatformLibraryContent, AcquisitionLibraryContent, EventLibraryContent, LibraryContentPerson

page = 'library'


class LibraryCreateView(LoginRequiredMixin, View):
    model = LibraryContent
    success_url = '/admin/library'

    def get(self, request, *args, **kwargs):
        form = LibraryContentForm()
        mention_form_set = LibraryMentionFormSet(prefix="mention")
        library_content_person_form_set = LibraryContentPersonFormSet(prefix="person")
        context = {
            'page': page,
            'operation': 'Create',
            'form': form,
            'mention_form_set': mention_form_set,
            'library_content_person_form_set': library_content_person_form_set
        }
        return render(request, 'dashboard/library/library_add.html', context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = LibraryContentForm(self.request.POST, request.FILES)
        mention_form_set = LibraryMentionFormSet(self.request.POST, prefix='mention')
        person_form_set = LibraryContentPersonFormSet(self.request.POST, prefix='person')
        form_valid = form.is_valid() and mention_form_set.is_valid() and person_form_set.is_valid()
        if form_valid:
            library_content = form.save()
            for mention_form in mention_form_set:
                mention_form.save(library_content)
            for person_form in person_form_set:
                person_form.save(library_content)
            return redirect(self.success_url)
        else:
            context = {
                'page': page,
                'operation': 'Create',
                'form': form,
                'mention_form_set': mention_form_set,
                'library_content_person_form_set': person_form_set
            }
            return render(request, 'dashboard/library/library_add.html', context)


class LibraryUpdateView(LoginRequiredMixin, View):
    model = LibraryContent
    success_url = '/admin/library'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        library_content = LibraryContent.objects.get(pk=pk)
        form = LibraryContentForm(instance=library_content)

        mention_form = formset_factory(LibraryContentMentionForm, extra=0)
        mention_data = []

        person_library_contents = PersonLibraryContent.objects.filter(library_content=library_content)
        for plc in person_library_contents:
            mention_data.append({'mention_type': 'person', 'person': plc.person})

        organization_library_contents = OrganizationLibraryContent.objects.filter(library_content=library_content)
        for olc in organization_library_contents:
            mention_data.append({'mention_type': 'organization', 'organization': olc.organization})

        funding_library_contents = FundingLibraryContent.objects.filter(library_content=library_content)
        for flc in funding_library_contents:
            mention_data.append({'mention_type': 'funding_round', 'funding': flc.funding})

        platform_library_contents = PlatformLibraryContent.objects.filter(library_content=library_content)
        for plc in platform_library_contents:
            mention_data.append({'mention_type': 'platform', 'platform': plc.platform})

        acquisition_library_contents = AcquisitionLibraryContent.objects.filter(library_content=library_content)
        for alc in acquisition_library_contents:
            mention_data.append({'mention_type': 'acquisition', 'platform': alc.acquisition})

        event_library_contents = EventLibraryContent.objects.filter(library_content=library_content)
        for elc in event_library_contents:
            mention_data.append({'mention_type': 'event', 'platform': elc.event})

        person_form = formset_factory(LibraryContentPersonForm, extra=0)
        person_data = []
        library_content_persons = LibraryContentPerson.objects.filter(library_content=library_content)
        for lcp in library_content_persons:
            person_data.append({'person_type': lcp.type, 'person': lcp.person})

        context = {
            'page': page,
            'operation': 'Update',
            'form': form,
            'mention_form_set': mention_form(initial=mention_data, prefix="mention"),
            'library_content_person_form_set': person_form(initial=person_data, prefix="person"),
        }
        return render(request, 'dashboard/library/library_add.html', context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        library_content = LibraryContent.objects.get(pk=pk)
        form = LibraryContentForm(self.request.POST, request.FILES, instance=library_content)
        mention_form_set = LibraryMentionFormSet(self.request.POST, prefix='mention')
        person_form_set = LibraryContentPersonFormSet(self.request.POST, prefix='person')
        form_valid = form.is_valid() and mention_form_set.is_valid() and person_form_set.is_valid()
        if form_valid:
            library_content = form.save()
            # delete existing records
            PersonLibraryContent.objects.filter(library_content=library_content).delete()
            OrganizationLibraryContent.objects.filter(library_content=library_content).delete()
            FundingLibraryContent.objects.filter(library_content=library_content).delete()
            PlatformLibraryContent.objects.filter(library_content=library_content).delete()
            AcquisitionLibraryContent.objects.filter(library_content=library_content).delete()
            EventLibraryContent.objects.filter(library_content=library_content).delete()
            # entry new records
            for mention_form in mention_form_set:
                mention_form.save(library_content)

            # delete existing records
            LibraryContentPerson.objects.filter(library_content=library_content).delete()
            # entry new records
            for person_form in person_form_set:
                person_form.save(library_content)
            return redirect(self.success_url)
        else:
            context = {
                'page': page,
                'operation': 'Create',
                'form': form,
                'mention_form_set': mention_form_set,
                'library_content_person_form_set': person_form_set
            }
            return render(request, 'dashboard/library/library_add.html', context)


class LibraryListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/library/library_list.html", {'page': page})


class LibraryListJson(LoginRequiredMixin, BaseDatatableView):
    model = LibraryContent
    # define the columns that will be returned
    columns = ['id', 'title', 'content_type', 'id']
    order_columns = ['id', 'title', 'created_at']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 20

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            content_type = "N/A"
            if item.content_type is not None:
                content_type = item.content_type.name
            json_data.append([
                escape("{0}".format(str(item.id))),
                escape("{0}".format(item.title)),
                escape("{0}".format(content_type)),
                escape("{0}".format(str(item.id))),
            ])
        return json_data


class LibraryDeleteView(LoginRequiredMixin, DeleteView):

    model = LibraryContent

    def delete(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            payload = {'status': True}
            return JsonResponse(payload, status=200)
        except Exception as e:
            return JsonResponse({'status': False}, status=500)