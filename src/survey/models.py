# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
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
class Section(NaturalModel):
    started = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    owner = models.SlugField(max_length=50, null=True, blank=True)


class Service(NaturalModel):
    private = models.BooleanField(default=False)
    owner = models.SlugField(max_length=50, null=True, blank=True)


class Reliable(NaturalModel):
    private = models.BooleanField(default=False)
    owner = models.SlugField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'Attribute of Trusted VAS Vendors'
        verbose_name_plural = 'Attributes of Trusted VAS Vendors'


class Challenge(NaturalModel):
    private = models.BooleanField(default=False)
    owner = models.SlugField(max_length=50, null=True, blank=True)


class Period(NaturalModel):
    private = models.BooleanField(default=False)
    owner = models.SlugField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'Acceptable ROI Period'
        verbose_name_plural = 'Acceptable ROI Periods'


class Survey(models.Model):
    user = models.OneToOneField(User)
    slug = models.SlugField(max_length=50, unique=True)

    is_section_0_reviewed = models.BooleanField(default=False)
    is_section_1_reviewed = models.BooleanField(default=False)
    is_section_2_reviewed = models.BooleanField(default=False)
    is_section_3_reviewed = models.BooleanField(default=False)

    section_0_empty = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    section_1_empty = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    section_2_empty = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    section_3_empty = models.PositiveSmallIntegerField(default=0, null=True, blank=True)

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

    COUNTRY_CHOICES = (
        (None, 'Please select an option...'),
        (COUNTRY, 'Country'),
        (REGION, 'Region'),
    )
    country_or_region = models.CharField(
        max_length=3,
        choices=COUNTRY_CHOICES,
        help_text='Please select appropriate value',
        null=True,
        blank=True,
    )

    countries = models.ManyToManyField(
        to=Country,
        related_name='responsible_countries',
        help_text='Start typing or select country from dropdown.',
        null=True,
        blank=True,
    )

    # QUESTION 3
    # -----------------------------------------------------------------------------
    VAS_CHOICES = (
        (None, 'Please select an option...'),
        ('L1', '0'),
        ('L6', '40+'),
    )

    vas_parties = models.CharField(
        max_length=3,
        choices=VAS_CHOICES,
        # default=COUNTRY,
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
        ('L1', 'Option'),
        ('L6', 'All'),
    )

    service_pitches = models.CharField(
        max_length=3,
        choices=PITCH_CHOICES,
        # default='L1',
        null=True,
        blank=True,
    )

    # QUESTION 6
    # -----------------------------------------------------------------------------
    Q6_CHOICES = (
        (None, 'Please select an option...'),
        ('L1', 'First'),
    )
    investments = models.CharField(
        max_length=2,
        choices=Q6_CHOICES,
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
        help_text="(omit currency and separators when filling in total revenue, e.g. 132000)"
    )
    # TODO: sort out question text

    revenue_mar_14 = models.BigIntegerField( null=True, blank=True)
    revenue_jun_14 = models.BigIntegerField( null=True, blank=True)
    revenue_sep_14 = models.BigIntegerField( null=True, blank=True)
    revenue_dec_14 = models.BigIntegerField( null=True, blank=True)

    # QUESTION 8
    # -----------------------------------------------------------------------------
    # Q8. Where does most of your revenue in VAS come from?
    revenue_streams = models.ManyToManyField(
        to=Service,
        null=True,
        blank=True,
    )

    revenue_stream_1 = models.ForeignKey(
        to=Service,
        related_name='revenue_stream_1',
        null=True,
        blank=True,
    )
    revenue_stream_2 = models.ForeignKey(
        to=Service,
        related_name='revenue_stream_2',
        null=True,
        blank=True,
    )
    revenue_stream_3 = models.ForeignKey(
        to=Service,
        related_name='revenue_stream_3',
        null=True,
        blank=True,
    )

    # QUESTION 9
    # -----------------------------------------------------------------------------
    # Q9. What percentage of your company revenues does VAS represent?
    # [Obligatory free text answer]
    vas_revenue_share = models.PositiveSmallIntegerField(
        max_length=15,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
        help_text='(please give the percentage as an integer between 0 and 100)'
    )

    # QUESTION 10
    # -----------------------------------------------------------------------------
    # Q10. How long is acceptable to wait for return on investment (ROI) on a new VAS?
    Q10_CHOICES = (
        ('L1', 'Invested less than last year'),
    )
    acceptable_roi_wait = models.ForeignKey(
        to=Period,
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
    acceptable_roi_percentage = models.PositiveSmallIntegerField(
        max_length=25,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
        help_text='(please give the percentage as an integer between 0 and 100)'
    )

    # QUESTION 12
    # -----------------------------------------------------------------------------
    challenges = models.ManyToManyField(
        to=Challenge,
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
    challenge = models.ForeignKey(
        to=Challenge,
        null=True,
        blank=True,
        # help_text='(select from dropdown list)',
    )
    rank = models.PositiveSmallIntegerField(null=True, blank=True)

    # QUESTION 8
    # -----------------------------------------------------------------------------
    attempted_services = models.ManyToManyField(
        to=Service,
        help_text='(please tick all that apply)',
        null=True,
        blank=False,
    )

    IN_HOUSE = 'IN-HOUSE'
    PITCHED = 'PITCHED'

    CHOICES = (
        (None, 'Please select an option...'),
        (IN_HOUSE, 'In House'),
        (PITCHED, 'Pitched'),
    )
    pitch_source = models.CharField(
        max_length=8,
        choices=CHOICES,
        # default=IN_HOUSE,
        null=True,
        blank=False,
    )

    year = models.PositiveSmallIntegerField(
        max_length=4,
        validators=[MinValueValidator(1980), MaxValueValidator(2016)],
        null=True,
        blank=True,)

    challenge_details = models.TextField(
        null=True,
        blank=True,
    )

    solution_details = models.TextField(
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
        ordering = ['rank',]


class VASProvider(models.Model):
    # QUESTION 4
    # -----------------------------------------------------------------------------
    vas_company_name = models.CharField(max_length=150)

    active_countries = models.ManyToManyField(
        to=Country,
        related_name='active_countries',
        null=True,
        blank=True,
    )

    services_provided = models.ManyToManyField(
        to=Service,
        help_text='(please tick all that apply)',
        null=True,
        blank=True,
    )

    # TODO: Add this question
    strong_services = models.ManyToManyField(
        to=Service,
        help_text='(please tick all that apply)',
        related_name='strong_service_set',
        null=True,
        blank=True,
    )

    trust_attributes = models.ManyToManyField(
        to=Reliable,
        help_text='(please tick all that apply)',
        null=True,
        blank=True,
    )

    contact_name = models.CharField(max_length=150, null=True, blank=True)
    contact_email = models.EmailField(max_length=150, null=True, blank=True)
    respondent = models.ForeignKey(Survey, null=True, blank=True)

    def __str__(self):
        return self.vas_company_name

    class Meta:
        verbose_name = 'Trusted VAS Vendor'
        verbose_name_plural = 'Trusted VAS Vendors'