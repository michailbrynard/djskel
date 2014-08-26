# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
import logging
logger = logging.getLogger('django')


# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
from django import forms
from .models import *


# FORMS
# ---------------------------------------------------------------------------------------------------------------------#
class AdvancedModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdvancedModelForm, self).__init__(*args, **kwargs)
        self.fields['fkbasic'].queryset = ChildModel.objects.filter(fkadvanced=self.instance)
