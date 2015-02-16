# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
from django import forms
from survey.models import Survey, VASProvider, ChallengeDetail
from logging import getLogger
from django.db.models import Q

# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
logger = getLogger('django')


# GLOBALS
# ---------------------------------------------------------------------------------------------------------------------#
MULTI_SELECT_CHECKBOX_HELP_TEXT = '(please select all that apply or use the textbox below to add other options)'


# FORMS
# ---------------------------------------------------------------------------------------------------------------------#
class ProgressForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = [
            'is_section_0_reviewed',
            'is_section_1_reviewed',
            'is_section_2_reviewed',
            'is_section_3_reviewed',
            'section_0_empty',
            'section_1_empty',
            'section_2_empty',
            'section_3_empty',
        ]
        # widgets = {
        #     'is_section_0_reviewed': forms.HiddenInput(),
        #     'is_section_1_reviewed': forms.HiddenInput(),
        #     'is_section_2_reviewed': forms.HiddenInput(),
        #     'is_section_3_reviewed': forms.HiddenInput(),
        # }


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['countries'].help_text = ''

    class Meta:
        model = Survey
        fields = [
            'name',
            'company_name',
            'job_title',
            'country_of_operation',
            'email_address',
            'phone_number',
            'gender',
            'country_or_region',
            'countries',
            'vas_parties',
            'service_pitches',
        ]
        widgets = {
            'country_of_operation': forms.Select(attrs={'class': 'select2-field'}),
            'gender': forms.RadioSelect(),
            'countries': forms.SelectMultiple(attrs={'class': 'select2-field'}),
        }


class FinancialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FinancialForm, self).__init__(*args, **kwargs)
        self.fields['revenue_streams'].queryset = self.fields['revenue_streams'].queryset.filter(
            Q(owner=None) | Q(owner=self.instance.slug))
        self.fields['revenue_stream_1'].queryset = self.fields['revenue_streams'].queryset.filter(
            Q(owner=None) | Q(owner=self.instance.slug))
        self.fields['revenue_stream_2'].queryset = self.fields['revenue_streams'].queryset.filter(
            Q(owner=None) | Q(owner=self.instance.slug))
        self.fields['revenue_stream_3'].queryset = self.fields['revenue_streams'].queryset.filter(
            Q(owner=None) | Q(owner=self.instance.slug))
        self.fields['acceptable_roi_wait'].queryset = self.fields['acceptable_roi_wait'].queryset.filter(
            Q(owner=None) | Q(owner=self.instance.slug))

    class Meta:
        model = Survey
        fields = [
            'investments',
            'currency',
            'revenue_mar_14',
            'revenue_jun_14',
            'revenue_sep_14',
            'revenue_dec_14',
            'revenue_streams',
            'revenue_stream_1',
            'revenue_stream_2',
            'revenue_stream_3',
            'vas_revenue_share',
            'acceptable_roi_wait',
            'acceptable_roi_percentage',
        ]
        widgets = {
            'currency': forms.Select(attrs={'class': 'select2-field'}),

            'revenue_mar_14': forms.TextInput(
                attrs={'placeholder': 'e.g. 10900 (omit currency and separators)', 'type': 'number'}),
            'revenue_jun_14': forms.TextInput(
                attrs={'placeholder': 'e.g. 13000 (omit currency and separators)', 'type': 'number'}),
            'revenue_sep_14': forms.TextInput(
                attrs={'placeholder': 'e.g. 8500 (omit currency and separators)', 'type': 'number'}),
            'revenue_dec_14': forms.TextInput(
                attrs={'placeholder': 'e.g. 10000 (omit currency and separators)', 'type': 'number'}),

            'vas_revenue_share': forms.TextInput(
                attrs={'placeholder': 'please give the percentage as an integer between 0 and 100'}),
            'acceptable_roi_percentage': forms.TextInput(
                attrs={'placeholder': 'please give the percentage as an integer between 0 and 100'}),

            'revenue_streams': forms.CheckboxSelectMultiple(),
        }


class VASProviderForm(forms.ModelForm):
    def __init__(self, slug, *args, **kwargs):
        super(VASProviderForm, self).__init__(*args, **kwargs)
        self.fields['services_provided'].help_text = MULTI_SELECT_CHECKBOX_HELP_TEXT
        self.fields['trust_attributes'].help_text = MULTI_SELECT_CHECKBOX_HELP_TEXT
        self.fields['active_countries'].help_text = ''
        self.fields['strong_services'].help_text = '(please select all that apply)'

        self.fields['services_provided'].queryset = self.fields['services_provided'].queryset.filter(
            Q(owner=None) | Q(owner=slug))
        self.fields['trust_attributes'].queryset = self.fields['trust_attributes'].queryset.filter(
            Q(owner=None) | Q(owner=slug))

    class Meta:
        model = VASProvider
        fields = [
            'id',
            'vas_company_name',
            'active_countries',
            'services_provided',
            'strong_services',
            'trust_attributes',
            'contact_name',
            'contact_email',
        ]
        widgets = {
            'id': forms.HiddenInput(),
            'active_countries': forms.SelectMultiple(attrs={'class': 'select2-field'}),
            'services_provided': forms.CheckboxSelectMultiple(),
            'strong_services': forms.CheckboxSelectMultiple(),
            'trust_attributes': forms.CheckboxSelectMultiple(),
        }


class ChallengeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChallengeForm, self).__init__(*args, **kwargs)
        self.fields['challenges'].help_text = MULTI_SELECT_CHECKBOX_HELP_TEXT
        self.fields['challenges'].queryset = self.fields['challenges'].queryset.filter(
            Q(owner=None) | Q(owner=self.instance.slug))

    class Meta:
        model = Survey
        fields = [
            'challenges',
        ]
        widgets = {
            'challenges': forms.CheckboxSelectMultiple(),
        }


class ChallengeDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChallengeDetailForm, self).__init__(*args, **kwargs)
        self.fields['attempted_services'].help_text = MULTI_SELECT_CHECKBOX_HELP_TEXT
        self.fields['attempted_services'].queryset = self.fields['attempted_services'].queryset.filter(
            Q(owner=None) | Q(owner=self.instance.respondent.slug))

    class Meta:
        model = ChallengeDetail
        fields = [
            'challenge',
            'attempted_services',
            'pitch_source',
            'year',
            'challenge_details',
            'solution_details',
        ]
        widgets = {
            'attempted_services': forms.CheckboxSelectMultiple(),
        }