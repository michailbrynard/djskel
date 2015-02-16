# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.http import QueryDict
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from survey.models import Survey, VASProvider, Service, Reliable, Challenge, ChallengeDetail, Period
from survey.forms import ProfileForm, VASProviderForm, FinancialForm, ChallengeForm, ChallengeDetailForm, ProgressForm
from logging import getLogger


# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
logger = getLogger('django')


# VIEWS
# ---------------------------------------------------------------------------------------------------------------------#
def login_user(request, slug):
    logger.info('Slug is: {}, trying to log in...'.format(slug))

    request.session['survey_slug'] = slug
    request.session.save()
    survey_instance = None

    try:
        survey_instance = Survey.objects.get(slug=slug)

    except Survey.DoesNotExist:
        logger.info('Survey does not exist...')
        user = User(username=slug[30:])
        user.set_password(slug)
        user.email = ''
        user.save()
        logger.info('Saved new user... {}'.format(user))
        survey_instance = Survey(slug=slug, user=user)
        survey_instance.save()
        logger.info('Saved new survey... {}'.format(survey_instance))

        for rank in range(1, 4):
            ChallengeDetail.objects.create(respondent=survey_instance, rank=rank)
            logger.info('Added new ChallengeDetail with respondent = {} and rank = {}'.format(survey_instance, rank))

    else:
        logger.info('Found survey and use!:')

    finally:
        if request.user.is_staff:
            logger.info('Staff in the house!!')

        else:
            user = authenticate(username=survey_instance.user.username, password=slug)
            logger.info('Not staff, who is %s' % survey_instance.user.username)

            if user is not None:
                # If staff member is testing
                if user.is_active:
                    logger.info('User is active!')
                    login(request, user)
                    # Redirect to a success page
                else:
                    logger.warn('User not active')
                    pass
                    # Return a 'disabled account' error message
            else:
                logger.warn('Authentication Failed')
                pass
                # Return an 'invalid login' error message.

        # logger.info('Confirming that survey_slug is stored: {}'.format(request.session['survey_slug']))
        return HttpResponseRedirect(reverse('survey:about'))


def about(request):
    try:
        slug = request.session['survey_slug']
    except KeyError:
        logger.warning('Expired session, could not find "survey_slug"')
        return HttpResponseRedirect('/expired/')

    survey_instance = Survey.objects.get(slug=slug)
    progress_form = ProgressForm(instance=survey_instance)
    return render(request, "survey/welcome.html", {'form': progress_form})


def get_survey_context(survey_instance):
    progress_form = ProgressForm(instance=survey_instance)
    profile_form = ProfileForm(instance=survey_instance)
    providers = survey_instance.vasprovider_set.all()
    financial_form = FinancialForm(instance=survey_instance)
    challenge_form = ChallengeForm(instance=survey_instance)
    challenge_details = survey_instance.challengedetail_set.all()

    context = {
        'progress_form': progress_form,
        'profile_form': profile_form,
        'providers': providers,
        'financial_form': financial_form,
        'challenge_form': challenge_form,
        'challenge_details': challenge_details,
    }
    return context


def survey(request):
    try:
        slug = request.session['survey_slug']
    except KeyError:
        logger.warning('Expired session, could not find "survey_slug"')
        return HttpResponseRedirect('/expired/')

    survey_instance = Survey.objects.get(slug=slug)
    return render(request, "survey/survey.html", get_survey_context(survey_instance))


def update_profile(request):
    try:
        slug = request.session['survey_slug']
    except KeyError:
        logger.warning('Expired session, could not find "survey_slug"')
        return HttpResponseRedirect('/expired/')

    profile = Survey.objects.get(slug=slug)

    if request.method == 'POST':
        logger.info(request.POST)
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            user = profile.user
            user.username = slugify(form.cleaned_data.get('name').title())
            user.email = form.cleaned_data.get('email_address')
            logger.info(user.username)
            user.save()

        else:
            survey_instance = Survey.objects.get(slug=slug)
            context = get_survey_context(survey_instance)
            context.update({'profile_form': form})
            return render(request, "survey/survey.html", context)

    logger.info('The rent is too damn high!! %s' % request.GET.get('close', False))

    if request.GET.get('close', False):
        return HttpResponseRedirect(reverse('survey:goodbye'))
    else:
        return HttpResponseRedirect(reverse('survey:survey') + '?tab=0&modal=success')


def update_financial(request):
    try:
        slug = request.session['survey_slug']
    except KeyError:
        logger.warning('Expired session, could not find "survey_slug"')
        return HttpResponseRedirect('/expired/')

    profile = Survey.objects.get(slug=slug)

    if request.method == 'POST':
        logger.info(request.POST)
        form = FinancialForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()

        else:
            survey_instance = Survey.objects.get(slug=slug)
            context = get_survey_context(survey_instance)
            context.update({'financial_form': form})
            return render(request, "survey/survey.html", context)

    if request.GET.get('close', False):
        return HttpResponseRedirect(reverse('survey:goodbye'))
    else:
        return HttpResponseRedirect(reverse('survey:survey') + '?tab=2&modal=success')


def update_challenge(request):
    try:
        slug = request.session['survey_slug']
    except KeyError:
        logger.warning('Expired session, could not find "survey_slug"')
        return HttpResponseRedirect('/expired/')

    profile = Survey.objects.get(slug=slug)

    if request.method == 'POST':
        # logger.info(request.POST)
        form = ChallengeForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()

        else:
            return render(request, "survey/survey.html", {'challenge_form': form, })
            # do something.

    if request.GET.get('close', False):
        return HttpResponseRedirect(reverse('survey:goodbye'))
    else:
        return HttpResponseRedirect(reverse('survey:survey') + '?tab=3&modal=success')


def update_providers(request):
    # slug = request.session['survey_slug']
    # profile = Survey.objects.get(slug=slug)

    if request.GET.get('close', False):
        return HttpResponseRedirect(reverse('survey:goodbye'))
    else:
        return HttpResponseRedirect(reverse('survey:survey') + '?tab=1&modal=success')


def update_section_status(request):
    try:
        slug = request.session['survey_slug']
    except KeyError:
        logger.warning('Expired session, could not find "survey_slug"')
        return HttpResponseRedirect('/expired/')

    profile = Survey.objects.get(slug=slug)

    if request.method == 'POST':

        logger.info(request.POST.get('is_section_0_reviewed'))

        form = ProgressForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
        else:
            logger.info(form.errors)
            logger.warning('Progress form not valid...')

        response_data = {
            'message': 'Success!',
        }
        return JsonResponse(response_data)


def add_service(request):
    try:
        slug = request.session['survey_slug']
    except KeyError:
        logger.warning('Expired session, could not find "survey_slug"')
        return HttpResponseRedirect('/expired/')

    if request.method == 'POST':
        name = request.POST.get('name')
        service = Service(name=name, private=True, owner=slug)
        service.save()

        response_data = {
            'id': service.id,
            'name': service.name
        }
        return JsonResponse(response_data)


def add_challenge(request):
    try:
        slug = request.session['survey_slug']
    except KeyError:
        logger.warning('Expired session, could not find "survey_slug"')
        return HttpResponseRedirect('/expired/')

    if request.method == 'POST':
        name = request.POST.get('name')
        challenge = Challenge(name=name, private=True, owner=slug)
        challenge.save()

        response_data = {
            'id': challenge.id,
            'name': challenge.name
        }
        return JsonResponse(response_data)


def reorder_challenge(request):
    try:
        slug = request.session['survey_slug']
    except KeyError:
        logger.warning('Expired session, could not find "survey_slug"')
        return HttpResponseRedirect('/expired/')

    respondent = Survey.objects.get(slug=slug)

    if request.method == 'POST':

        data = request.POST
        logger.info(data)
        order = dict(data)['challenge-table[]']
        logger.info(order)

        challenges = []
        for k, v in enumerate(order):
            challenge = ChallengeDetail.objects.get(respondent=respondent, rank=k+1)
            logger.info('{0}\t-\tOld rank: {1}\tNew Rank: {2}'.format(challenge, k+1, int(v)))
            challenge.rank = int(v)
            challenges.append(challenge)

        for challenge in challenges:
            challenge.save()

        response_data = {}
        return JsonResponse(response_data)


def add_period(request):
    try:
        slug = request.session['survey_slug']
    except KeyError:
        logger.warning('Expired session, could not find "survey_slug"')
        return HttpResponseRedirect('/expired/')

    if request.method == 'POST':
        name = request.POST.get('name')
        roi_period = Period(name=name, private=True, owner=slug)
        roi_period.save()

        response_data = {
            'id': roi_period.id,
            'name': roi_period.name
        }
        return JsonResponse(response_data)


def add_reliable(request):
    try:
        slug = request.session['survey_slug']
    except KeyError:
        logger.warning('Expired session, could not find "survey_slug"')
        return HttpResponseRedirect('/expired/')

    if request.method == 'POST':
        name = request.POST.get('name')
        reliable = Reliable(name=name, private=True, owner=slug)
        reliable.save()

        response_data = {
            'id': reliable.id,
            'name': reliable.name
        }
        return JsonResponse(response_data)


def create_provider(request):
    try:
        slug = request.session['survey_slug']
    except KeyError:
        logger.warning('Expired session, could not find "survey_slug"')
        return HttpResponseRedirect('/expired/')

    if request.method == 'POST':

        logger.info(request.POST)
        form = VASProviderForm(request.POST)

        if form.is_valid():
            logger.info('Form is valid!')
            response_data = {}

            vas = form.save()
            if not vas.respondent:
                survey_instance = Survey.objects.get(slug=slug)
                vas.respondent = survey_instance
                vas.save()

            response_data['id'] = vas.id
            response_data['companyName'] = vas.company_name
            response_data['contactName'] = vas.contact_name or '-'
            response_data['contactEmail'] = vas.contact_email or '-'

            return JsonResponse(response_data)

        else:
            logger.info(form.errors)

    return JsonResponse({'Error': 'Can only handle POST requests...'})


def get_provider(request, pk):
    try:
        slug = request.session['survey_slug']
    except KeyError:
        logger.warning('Expired session, could not find "survey_slug"')
        return HttpResponseRedirect('/expired/')
    vas = VASProvider.objects.get(slug=slug, pk=pk)
    form = VASProviderForm(request.POST, instance=vas)

    return render(request, "survey/survey.html", {'provider_form': form, })


def update_provider(request, pk):
    try:
        slug = request.session['survey_slug']
    except KeyError:
        logger.warning('Expired session, could not find "survey_slug"')
        return HttpResponseRedirect('/expired/')

    if request.method == 'POST':

        if pk is not None:
            vas = VASProvider.objects.get(pk=pk)
            form = VASProviderForm(request.POST, instance=vas)
        else:
            form = VASProviderForm(request.POST)

        if form.is_valid():
            response_data = {}

            vas = form.save()
            if not vas.respondent:
                survey_instance = Survey.objects.get(slug=slug)
                vas.respondent = survey_instance
                vas.save()

            response_data['id'] = vas.id
            response_data['companyName'] = vas.company_name
            response_data['contactName'] = vas.contact_name or '-'
            response_data['contactEmail'] = vas.contact_email or '-'

            return JsonResponse(response_data, status=200)

        else:
            return JsonResponse({'errors': form.errors, 'data': form}, status=400)

    return JsonResponse({'Error': 'Can only handle POST requests...'}, status=403)


def delete_provider(request):
    if request.method == 'DELETE':
        provider_instance = VASProvider.objects.get(pk=int(QueryDict(request.body).get('pk')))
        provider_instance.delete()
        response_data = {'msg': 'Post was deleted.'}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'Error': 'Can only handle DELETE requests...'})


class ProviderView(View):
    form_class = VASProviderForm

    template_name = 'provider_template.html'

    def get(self, request, pk, *args, **kwargs):
        try:
            slug = self.request.session['survey_slug']
        except KeyError:
            logger.warning('Expired session, could not find "survey_slug"')
            return HttpResponseRedirect('/expired/')
        vas = VASProvider.objects.get(slug=slug, pk=pk)
        form = self.form_class(instance=vas, slug=slug)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})


class ProviderCreate(CreateView):
    model = VASProvider
    form_class = VASProviderForm

    def get_success_url(self):
        return reverse('survey:survey') + '?tab=1'

    def get_form_kwargs(self):
        kwargs = super(ProviderCreate, self).get_form_kwargs()
        kwargs.update({'slug': self.request.session['survey_slug']})
        return kwargs

    def form_valid(self, form):
        slug = self.request.session['survey_slug']
        form.instance.respondent = Survey.objects.get(slug=slug)
        return super(ProviderCreate, self).form_valid(form)


class ProviderUpdate(UpdateView):
    model = VASProvider
    form_class = VASProviderForm

    def get_success_url(self):
        return reverse('survey:survey') + '?tab=1'

    def get_form_kwargs(self):
        kwargs = super(ProviderUpdate, self).get_form_kwargs()
        kwargs.update({'slug': self.request.session['survey_slug']})
        return kwargs


class ProviderDelete(DeleteView):
    model = VASProvider
    success_url = reverse_lazy('survey:survey')  # + '?tab=2'


class ChallengeDetailCreate(CreateView):
    model = ChallengeDetail
    form_class = ChallengeDetailForm
    success_url = reverse_lazy('survey:survey')  # + '?tab=3&modal=exampleModal'

    def get_success_url(self):
        return reverse('survey:survey') + '?tab=3'

    def form_valid(self, form):
        slug = self.request.session['survey_slug']
        form.instance.rank = self.kwargs['rank']
        survey_instance = Survey.objects.get(slug=slug)
        form.instance.respondent = survey_instance
        return super(ChallengeDetailCreate, self).form_valid(form)


class ChallengeDetailUpdate(UpdateView):
    model = ChallengeDetail
    form_class = ChallengeDetailForm

    def get_object(self, model=ChallengeDetail):
        slug = self.request.session['survey_slug']
        survey_instance = Survey.objects.get(slug=slug)
        logger.info(slug)
        logger.info(self.kwargs['rank'])
        obj = ChallengeDetail.objects.get(respondent=survey_instance, rank=self.kwargs['rank'])
        return obj

    def get_success_url(self):
        return reverse('survey:survey') + '?tab=3'