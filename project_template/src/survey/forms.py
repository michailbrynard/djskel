# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
from django import forms
from survey.models import Survey, VASProvider, ChallengeDetail
from logging import getLogger
from django.db.models import Q

# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
logger = getLogger('django')


# FORMS
# ---------------------------------------------------------------------------------------------------------------------#
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
    # def __init__(self, *args, **kwargs):
    # super(FinancialForm, self).__init__(*args, **kwargs)
    # if self.instance:
    # self.fields['revenue_streams'].queryset = Service.objects.filter(pk__in=[1, 5, 8, 9])

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

    class Meta:
        model = Survey

        # choices = [(0, '15-29'), (1, '30-44'), (2, '45-60'), (3, 'Other, please specify:')]
        # new = ChoiceWithOtherField(choices=choices)

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
            'slug': forms.HiddenInput(),
            'revenue_streams': forms.CheckboxSelectMultiple(),
            # 'acceptable_roi_wait': ChoiceWithOtherWidget(choices=(('1', '1'), ('2', '2'))),
        }


class VASProviderForm(forms.ModelForm):
    def __init__(self, slug, *args, **kwargs):
        super(VASProviderForm, self).__init__(*args, **kwargs)
        self.fields['services_provided'].help_text = ''
        self.fields['trust_attributes'].help_text = ''
        self.fields['countries'].help_text = ''
        self.fields['strong_services'].help_text = ''

        self.fields['services_provided'].queryset = self.fields['services_provided'].queryset.filter(
            Q(owner=None) | Q(owner=slug))
        self.fields['trust_attributes'].queryset = self.fields['trust_attributes'].queryset.filter(
            Q(owner=None) | Q(owner=slug))

    class Meta:
        model = VASProvider

        fields = [
            'id',
            'company_name',
            'countries',
            'services_provided',
            'strong_services',
            'trust_attributes',
            'contact_name',
            'contact_email',
            # 'respondent',
        ]

        widgets = {
            'id': forms.HiddenInput(),
            # 'respondent': forms.HiddenInput(),

            'countries': forms.SelectMultiple(attrs={'class': 'select2-field'}),
            'services_provided': forms.CheckboxSelectMultiple(),
            'strong_services': forms.CheckboxSelectMultiple(),
            'trust_attributes': forms.CheckboxSelectMultiple(),
        }


class ChallengeForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    # super(ChallengeForm, self).__init__(*args, **kwargs)
    # self.fields['services'].help_text = ''
    # self.fields['trust_attributes'].help_text = ''
    # self.fields['countries'].help_text = ''

    def __init__(self, *args, **kwargs):
        super(ChallengeForm, self).__init__(*args, **kwargs)
        self.fields['challenges'].queryset = self.fields['challenges'].queryset.filter(
            Q(owner=None) | Q(owner=self.instance.slug))
        # self.fields['biggest_challenge_1'].queryset = self.fields['biggest_challenge_1'].queryset.filter(owner=slug)
        # self.fields['biggest_challenge_2'].queryset = self.fields['biggest_challenge_2'].queryset.filter(owner=slug)
        # self.fields['biggest_challenge_3'].queryset = self.fields['biggest_challenge_3'].queryset.filter(owner=slug)

    class Meta:
        model = Survey

        fields = [
            'challenges',
            # 'biggest_challenge_1',
            # 'biggest_challenge_2',
            # 'biggest_challenge_3',
        ]

        widgets = {
            'challenges': forms.CheckboxSelectMultiple(),
        }


class ChallengeDetailForm(forms.ModelForm):
    # def __init__(self, slug, *args, **kwargs):
    def __init__(self, *args, **kwargs):
        super(ChallengeDetailForm, self).__init__(*args, **kwargs)
        # self.fields['challenge'].queryset = self.fields['challenge'].queryset.filter(owner=slug)
        self.fields['attempted_services'].help_text = ''
        self.fields['attempted_services'].queryset = self.fields['attempted_services'].queryset.filter(
            Q(owner=None) | Q(owner=self.instance.slug))

    # def __init__(self, *args, **kwargs):
    # super(ChallengeForm, self).__init__(*args, **kwargs)
    # self.fields['services'].help_text = ''
    # self.fields['trust_attributes'].help_text = ''
    # self.fields['countries'].help_text = ''

    class Meta:
        model = ChallengeDetail

        fields = [
            'challenge',
            'attempted_services',
            'country_or_region',
            'year',
            'challenge_details',
            'solution_details',
        ]

        widgets = {
            # 'challenge': forms.HiddenInput(),
            'attempted_services': forms.CheckboxSelectMultiple(),
        }


# import floppyforms.__future__ as forms
# FORMS
# ---------------------------------------------------------------------------------------------------------------------#
# class ProfileForm(forms.ModelForm):
# class Meta:
# model = Survey
# # fields = ('name', 'url')
