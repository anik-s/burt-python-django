from django import forms
from django.forms import ModelChoiceField, formset_factory

from org.forms.common import year_choices, month_choices, day_choices, PersonSelect2Widget, OrganizationSelect2Widget, \
    PlatformSelect2Widget, FundingSelect2Widget, AcquisitionSelect2Widget, EventSelect2Widget, delete_choices
from org.models import LibraryContentType, LibraryContent, Person, Organization, FundingRound, Platform, Acquisition, \
    Event, PersonLibraryContent, OrganizationLibraryContent, FundingLibraryContent, PlatformLibraryContent, \
    AcquisitionLibraryContent, EventLibraryContent, LibraryContentPerson


class ContentTypeChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class LibraryContentForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_image = forms.ImageField(label="Image", required=False)
    short_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    url = forms.URLField(label="URL", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_year = forms.ChoiceField(label="Year", required=False, choices=year_choices,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    date_month = forms.ChoiceField(label="Month", required=False, choices=month_choices,
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    date_day = forms.ChoiceField(label="Day", required=False, choices=day_choices,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    content_type = ContentTypeChoiceField(queryset=LibraryContentType.objects.all(), required=True,
                                          empty_label="-- Select Content Type --",
                                          to_field_name="id", widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = LibraryContent
        fields = [
            'title',
            'profile_image',
            'short_description',
            'url',
            'date_year',
            'date_month',
            'date_day',
            'content_type'
        ]


mention_types = [('person', 'Person'), ('organization', 'Organization'), ('platform', 'Platform'),
                 ('funding_round', 'Funding'), ('acquisition', 'Acquisition'), ('event', 'Event')]


class LibraryContentMentionForm(forms.Form):
    mention_type = forms.ChoiceField(label="Choose Type", choices=mention_types,
                                     widget=forms.RadioSelect(attrs={'class': 'radio-mention-type'}))
    person = ModelChoiceField(label="Person", queryset=Person.objects.all(),
                              empty_label="Search Person", required=False,
                              widget=PersonSelect2Widget(attrs={'class': 'form-control'}))
    organization = ModelChoiceField(label="Organization", queryset=Organization.objects.all(),
                                    empty_label="Search Organization", required=False,
                                    widget=OrganizationSelect2Widget(attrs={'class': 'form-control'}))
    platform = ModelChoiceField(label="Platform", queryset=Platform.objects.all(),
                                empty_label="Search Platform", required=False,
                                widget=PlatformSelect2Widget(attrs={'class': 'form-control'}))
    funding = ModelChoiceField(label="Funding", queryset=FundingRound.objects.all(),
                               empty_label="Search Funding", required=False,
                               widget=FundingSelect2Widget(attrs={'class': 'form-control'}))
    acquisition = ModelChoiceField(label="Acquisition", queryset=Acquisition.objects.all(),
                                   empty_label="Search Acquisition", required=False,
                                   widget=AcquisitionSelect2Widget(attrs={'class': 'form-control'}))
    event = ModelChoiceField(label="Event", queryset=Event.objects.all(),
                             empty_label="Search Event", required=False,
                             widget=EventSelect2Widget(attrs={'class': 'form-control'}))
    deleted = forms.ChoiceField(label="Deleted", required=True, choices=delete_choices, initial='0',
                                widget=forms.Select(attrs={'class': 'form-control deleted'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        mention_type = cleaned_data.get("mention_type")
        person = cleaned_data.get("person")
        organization = cleaned_data.get("organization")
        funding = cleaned_data.get("funding")
        platform = cleaned_data.get("platform")
        acquisition = cleaned_data.get("acquisition")
        event = cleaned_data.get("event")
        deleted = cleaned_data.get("deleted")

        if deleted == '0':
            if mention_type == 'person' and person is None:
                msg = "This field is required"
                self.add_error('person', msg)
            elif mention_type == 'organization' and organization is None:
                msg = "This field is required"
                self.add_error('organization', msg)
            elif mention_type == 'funding_round' and funding is None:
                msg = "This field is required"
                self.add_error('funding', msg)
            elif mention_type == 'platform' and platform is None:
                msg = "This field is required"
                self.add_error('platform', msg)
            elif mention_type == 'acquisition' and acquisition is None:
                msg = "This field is required"
                self.add_error('acquisition', msg)
            elif mention_type == 'event' and event is None:
                msg = "This field is required"
                self.add_error('event', msg)

    def save(self, library_content):
        cleaned_data = self.cleaned_data
        print(cleaned_data)
        deleted = cleaned_data.get("deleted")
        if deleted == '0':
            if cleaned_data.get('mention_type') == 'person':
                person_news = PersonLibraryContent(person=cleaned_data.get("person"), library_content=library_content)
                person_news.save()
            elif cleaned_data.get('mention_type') == 'organization':
                o_news = OrganizationLibraryContent(organization=cleaned_data.get("organization"), library_content=library_content)
                o_news.save()
            elif cleaned_data.get('mention_type') == 'funding_round':
                f_news = FundingLibraryContent(funding=cleaned_data.get("funding"), library_content=library_content)
                f_news.save()
            elif cleaned_data.get('mention_type') == 'platform':
                p_news = PlatformLibraryContent(platform=cleaned_data.get("platform"), library_content=library_content)
                p_news.save()
            elif cleaned_data.get('mention_type') == 'acquisition':
                p_news = AcquisitionLibraryContent(acquisition=cleaned_data.get("acquisition"), library_content=library_content)
                p_news.save()
            elif cleaned_data.get('mention_type') == 'event':
                p_news = EventLibraryContent(event=cleaned_data.get("event"), library_content=library_content)
                p_news.save()


LibraryMentionFormSet = formset_factory(LibraryContentMentionForm, min_num=0, validate_min=True)


person_types = [('author', 'Author'), ('host', 'Host'), ('guest', 'Guest')]


class LibraryContentPersonForm(forms.Form):
    person_type = forms.ChoiceField(label="Choose Type", choices=person_types,
                                     widget=forms.Select(attrs={'class': 'form-control select-person-type'}))
    person = ModelChoiceField(label="Person", queryset=Person.objects.all(),
                                    empty_label="Search Person", required=False,
                                    widget=PersonSelect2Widget(attrs={'class': 'form-control'}))
    deleted = forms.ChoiceField(label="Deleted", required=True, choices=delete_choices, initial='0',
                                widget=forms.Select(attrs={'class': 'form-control deleted'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data = super().clean()
        person_type = cleaned_data.get("person_type")
        person = cleaned_data.get("person")
        deleted = cleaned_data.get("deleted")
        if deleted == '0':
            if person is None:
                self.add_error('person', 'This field is required')
            if person_type == "":
                self.add_error('person_type', 'This field is required')

    def save(self, library_content):
        cleaned_data = super().clean()
        person = cleaned_data.get("person")
        person_type = cleaned_data.get("person_type")
        deleted = cleaned_data.get("deleted")

        if deleted == '0':
            lcp = LibraryContentPerson(person=person, library_content=library_content, type=person_type)
            lcp.save()


LibraryContentPersonFormSet = formset_factory(LibraryContentPersonForm, min_num=0, validate_min=True)