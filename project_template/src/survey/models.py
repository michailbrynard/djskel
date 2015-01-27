# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from fact_book.models import Country, Currency
from logging import getLogger


# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
logger = getLogger('django')


# BASE MODELS
# ---------------------------------------------------------------------------------------------------------------------#
class NaturalManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class NaturalModel(models.Model):
    name = models.CharField(max_length=150, unique=False)

    def natural_key(self):
        return (self.name, )

    objects = NaturalManager()

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


# MODELS
# ---------------------------------------------------------------------------------------------------------------------#
class Service(NaturalModel):
    private = models.BooleanField(default=False)
    owner = models.SlugField(max_length=24, null=True, blank=True)


class Reliable(NaturalModel):
    private = models.BooleanField(default=False)
    owner = models.SlugField(max_length=24, null=True, blank=True)


class Challenge(NaturalModel):
    private = models.BooleanField(default=False)
    owner = models.SlugField(max_length=24, null=True, blank=True)


class Period(NaturalModel):
    private = models.BooleanField(default=False)
    owner = models.SlugField(max_length=24, null=True, blank=True)


class Survey(models.Model):
    user = models.OneToOneField(User)
    slug = models.SlugField(max_length=24, unique=True)
    name = models.CharField(max_length=150)

    # QUESTION 1
    # -----------------------------------------------------------------------------
    FEMALE = 'F'
    MALE = 'M'

    GENDER_CHOICES = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=MALE,
        verbose_name='Gender',
        null=False,
        blank=False,
    )

    company_name = models.CharField(max_length=150)
    job_title = models.CharField(max_length=150, blank=True, null=True)
    country_of_operation = models.ForeignKey(Country, null=True, blank=True)
    # country_of_operation = ChoiceField(Country)

    email_address = models.EmailField()
    phone_number = models.CharField(max_length=20, help_text='e.g.: +27 28 123 4444', blank=True, null=True)

    # QUESTION 2
    # -----------------------------------------------------------------------------
    COUNTRY = 'C'
    REGION = 'R'
    GLOBAL = 'G'

    COUNTRY_CHOICES = (
        (None, 'Please select an option...'),
        (COUNTRY, 'Country'),
        (REGION, 'Group (Region)'),
        (GLOBAL, 'Group (Global)'),

    )
    country_or_region = models.CharField(
        max_length=3,
        choices=COUNTRY_CHOICES,
        verbose_name='Is your position in the group or country level?',
        help_text='Please select appropriate value',
        null=True,
        blank=True,
    )

    countries = models.ManyToManyField(
        to=Country,
        related_name='responsible_countries',
        verbose_name='If you have responsibility for one or more countries, please list them here:',
        help_text='Start typing or select country from dropdown.',
        null=True,
        blank=True,
    )

    # QUESTION 3
    # -----------------------------------------------------------------------------
    VAS_CHOICES = (
        (None, 'Please select an option...'),
        ('L1', '0 - All in house'),
        ('L2', '1-10'),
        ('L3', '11-20'),
        ('L4', '21-30'),
        ('L5', '31-40'),
        ('L6', '40+'),
    )

    vas_parties = models.CharField(
        max_length=3,
        choices=VAS_CHOICES,
        # default=COUNTRY,
        verbose_name='In each country you cover in your personal remit, '
                     'approximately how many third party VAS suppliers, aggregators, '
                     'content providers etc does your company work with to offer '
                     'VAS to your customers?',
        null=True,
        blank=True,
    )

    def get_absolute_url(self):
        # return 'http://%s/s/%s' % (Site.objects.get_current().domain, self.slug)
        return reverse('survey:login', kwargs={'slug': self.slug, })

    # QUESTION 5
    # -----------------------------------------------------------------------------
    PITCH_CHOICES = (
        (None, 'Please select an option...'),
        ('L1', 'None'),
        ('L2', '1-25%'),
        ('L3', '26-50%'),
        ('L4', '51-75%'),
        ('L5', '76-99%'),
        ('L6', 'All'),
    )

    service_pitches = models.CharField(
        max_length=3,
        choices=PITCH_CHOICES,
        # default='L1',
        verbose_name='How many of your services are the result of pitches from external vendors?',
        null=True,
        blank=True,
    )

    # QUESTION 6
    # -----------------------------------------------------------------------------
    Q6_CHOICES = (
        (None, 'Please select an option...'),
        ('L1', 'Invested less than last year'),
        ('L2', 'Invested about the same as last year'),
        ('L3', 'Invested up to 20% more than last year'),
        ('L4', 'Invested up to 50% more than last year'),
        ('L5', 'Invested 50% or more than last year'),
    )
    investments = models.CharField(
        max_length=2,
        choices=Q6_CHOICES,
        verbose_name='Q1. How much did you invest in mobile VAS this year relative to last year?',
        null=True,
        blank=True,
    )

    # QUESTION 7
    # -----------------------------------------------------------------------------
    # Q7. What were the total revenues generated by mobile VAS during the following month:
    currency = models.ForeignKey(
        to=Currency,
        null=True,
        blank=True,
        verbose_name="Q2. What were the total revenues generated by mobile VAS during the following months "
                     "(select currency from dropdown):",

    )
    # TODO: sort out question text

    revenue_mar_14 = models.IntegerField(verbose_name='March 2014:', null=True, blank=True)
    revenue_jun_14 = models.IntegerField(verbose_name='June 2014:', null=True, blank=True)
    revenue_sep_14 = models.IntegerField(verbose_name='September 2014:', null=True, blank=True)
    revenue_dec_14 = models.IntegerField(verbose_name='December 2014:', null=True, blank=True)

    # QUESTION 8
    # -----------------------------------------------------------------------------
    # Q8. Where does most of your revenue in VAS come from?
    revenue_streams = models.ManyToManyField(
        to=Service,
        verbose_name='Q3. Which three VAS generate the highest revenues for your company?',
        null=True,
        blank=True,
    )

    revenue_stream_1 = models.ForeignKey(
        to=Service,
        related_name='revenue_stream_1',
        verbose_name='Highest revenue stream:',
        null=True,
        blank=True,
    )
    revenue_stream_2 = models.OneToOneField(
        to=Service,
        related_name='revenue_stream_2',
        verbose_name='Second highest revenue stream:',
        null=True,
        blank=True,
    )
    revenue_stream_3 = models.OneToOneField(
        to=Service,
        related_name='revenue_stream_3',
        verbose_name='Third highest revenue stream:',
        null=True,
        blank=True,
    )

    # QUESTION 9
    # -----------------------------------------------------------------------------
    # Q9. What percentage of your company revenues does VAS represent?
    # [Obligatory free text answer]
    vas_revenue_share = models.CharField(
        max_length=15,
        verbose_name='Q4. What percentage of your company revenues does VAS represent?',
        null=True,
        blank=True,
    )

    # QUESTION 10
    # -----------------------------------------------------------------------------
    # Q10. How long is acceptable to wait for return on investment (ROI) on a new VAS?
    Q10_CHOICES = (
        ('L1', 'Invested less than last year'),
        ('L2', 'Invested about the same as last year'),
        ('L3', 'Invested up to 20% more than last year'),
        ('L4', 'Invested up to 50% more than last year'),
        ('L5', 'Invested 50% or more than last year'),
    )
    acceptable_roi_wait = models.ForeignKey(
        to=Period,
        verbose_name='Q5. How long is acceptable to wait for return on investment (ROI) on a new VAS?',
        null=True,
        blank=True,
        help_text='Use the textbox below to add another option to the drop-down.'
    )
    # 3 months
    # 6 months
    # 12 months
    # Other:

    # TODO: Dropdown with freetext

    # QUESTION 11
    # -----------------------------------------------------------------------------
    # Q11. What is the minimum percentage of return on investment at the end of the acceptable period identified in Q10?
    acceptable_roi_percentage = models.CharField(
        max_length=25,
        verbose_name='Q6. What is the minimum percentage of return on investment at the'
                     ' end of the acceptable period identified in Q10?',
        null=True,
        blank=True,
    )

    # QUESTION 12
    # -----------------------------------------------------------------------------
    challenges = models.ManyToManyField(
        to=Challenge,
        verbose_name="Q1. What challenges have you met in trying to implement M4D VAS services in your company?",
        help_text='(please tick all that apply)',
        null=True,
        blank=True,
    )

    # QUESTION 13/14
    # -----------------------------------------------------------------------------
    # biggest_challenge_1 = models.OneToOneField(
    # to=ChallengeDetail,
    #     related_name='challenge_1',
    #     null=True,
    #     blank=True,
    # )
    # biggest_challenge_2 = models.OneToOneField(
    #     to=ChallengeDetail,
    #     related_name='challenge_2',
    #     null=True,
    #     blank=True,
    # )
    # biggest_challenge_3 = models.OneToOneField(
    #     to=ChallengeDetail,
    #     related_name='challenge_3',
    #     null=True,
    #     blank=True,
    # )

    def __str__(self):
        return self.name


class ChallengeDetail(models.Model):
    respondent = models.ForeignKey(Survey, null=True, blank=True)
    # owner = models.SlugField(max_length=24, unique=False)
    challenge = models.ForeignKey(to=Challenge, null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)

    # QUESTION 8
    # -----------------------------------------------------------------------------
    attempted_services = models.ManyToManyField(
        to=Service,
        verbose_name='Service(s) you were aiming to launch when you encountered the challenge:',
        help_text='(please tick all that apply)',
        null=True,
        blank=True,
    )

    IN_HOUSE = 'IN-HOUSE'
    PITCHED = 'PITCHED'

    CHOICES = (
        (None, 'Please select an option...'),
        (IN_HOUSE, 'In House'),
        (PITCHED, 'Pitched'),
    )
    country_or_region = models.CharField(
        max_length=8,
        choices=CHOICES,
        # default=IN_HOUSE,
        verbose_name='Was this pitched to you from an external provider or an in-house idea?',
        null=True,
        blank=True,
    )

    year = models.IntegerField(max_length=4, null=True, blank=True)

    challenge_details = models.TextField(
        verbose_name='More detail on specific problem(s) encountered when trying to implement:',
        null=True,
        blank=True,
    )

    solution_details = models.TextField(
        verbose_name='If a solution was found, what was it? '
                     'If a solution was not found, what would have helped the situation?',
        null=True,
        blank=True,
    )

    def get_name(self):
        if self.rank == 1:
            return "1st Biggest Challenge"
        elif self.rank == 2:
            return "2nd Biggest Challenge"
        elif self.rank == 3:
            return "3rd Biggest Challenge"
        else:
            return "-"

    def __str__(self):
        return "%s" % (self.challenge, )

    class Meta:
        unique_together = ('respondent', 'challenge')


class VASProvider(models.Model):
    # QUESTION 4
    # -----------------------------------------------------------------------------
    company_name = models.CharField(max_length=150, verbose_name="Q1. Company name")

    countries = models.ManyToManyField(
        to=Country,
        related_name='active_countries',
        verbose_name='Q2. Countries in which your company works with the supplier:',
        null=True,
        blank=True,
    )

    services_provided = models.ManyToManyField(
        to=Service,
        verbose_name="Q3. Services it provides:",
        help_text='(please tick all that apply)',
        null=True,
        blank=True,
    )

    # TODO: Add this question
    strong_services = models.ManyToManyField(
        to=Service,
        verbose_name="Of the above service areas are there any you feel this provider is particularly strong in? ",
        help_text='(please tick all that apply)',
        related_name='strong_service_set',
        null=True,
        blank=True,
    )

    trust_attributes = models.ManyToManyField(
        to=Reliable,
        verbose_name='Q4. What makes the company a trusted provider?',
        help_text='(please tick all that apply)',
        null=True,
        blank=True,
    )

    contact_name = models.CharField(max_length=150, null=True, blank=True, verbose_name="Q5. Vendor contact name")
    contact_email = models.EmailField(max_length=150, null=True, blank=True, verbose_name="Q6. Vendor contact email")

    respondent = models.ForeignKey(Survey, null=True, blank=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'Trusted VAS Vendor'
        verbose_name_plural = 'Trusted VAS Vendors'