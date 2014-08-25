# LOGGING
# ------------------------------------------------------------------------------#
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


# IMPORTS
#------------------------------------------------------------------------------#

# shortcuts
from django.shortcuts import render

# views.generic
from django.views.generic import DetailView
from django.views.generic import ListView

# http
from django.http import HttpResponse
from django.http import StreamingHttpResponse

# contrib.auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group, Permission


# conf
from django.conf import settings

# core
from django.core.urlresolvers import reverse

# utils
from django.utils.translation import ugettext as _

# app1
from app1.models import *

# GENERIC VIEWS
#------------------------------------------------------------------------------#

class BasicModelView(DetailView):
    model = BasicModel


# CUSTOM VIEWS
#------------------------------------------------------------------------------#

@login_required
def custom_basic_view(request):
    # Context variables to pass on to template
    context = {
        'val1': 'Hello',
        'val2': 'World!'
    }

    # Render the template
    return render(request, 'app1/basic_template.html', context)


@login_required
def custom_basic_save_view(request, slug):
    bm = BasicModel.objects.get(slug=slug)

    if request.method == 'POST':
        # Form changes (TODO: clean data)
        form = ReportUpdateForm(request.POST, instance=bm)
        form.save()

        # Additional changes
        bm.version = bm.version + 1
        bm.save()

        # Redirect after successful save
        return HttpResponseRedirect(reverse('app1:basicmodel_detail', kwargs={'slug': bm.slug}))

    return render(request, 'app1/basic_template.html', context)

