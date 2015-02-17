# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
from django.core.management.base import BaseCommand
from survey.models import Service, Reliable, Challenge, Period
from logging import getLogger


# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
logger = getLogger('django')


# GLOBALS
# ---------------------------------------------------------------------------------------------------------------------#
CHALLENGES = [
    'Legal/regulatory objections',
    'ROI (return on investment) deemed too slow',
    'Predicted revenue generated deemed too low',
    'Lack of market research data',
    'Lack of documented business case',
    'Lack of relevant, local content',
    'Partnership with M4D service provider issues/breakdown',
    'Lack of local M4D service providers',
    'Technical requirements were too complex',
    'Lack of capacity on technical team',
    'Lack of marketing and communication support/bandwidth',
    'Lack of senior management team buy-in',
    'Lack of M4D service ideas',
]

SERVICES = [
    'News',
    'Sports',
    'Religion',
    'Voicemail',
    'Balance enquiries/top-ups',
    'Ringback tones',
    'Music',
    'Celebrities/Films',
    'Gaming',
    'Infotainment',
    'Comedy/Jokes',
    'Coupons/deals',
    'Contests/quizzes',
    'Astrology',
    'Healthcare',
    'Citizen/employee rights',
    'Agricultural productivity',
    'Women’s issues/Gender discrimination',
    'Response to natural disasters',
    'Access to the mobile internet',
    'Access to basic utilities (Water, Sanitation and Electricity)',
    'Education',
    'Jobs/employment',
    'Security/Personal safety',
]

RELIABLE_ATTRIBUTES = [
    'Reliable',
    'Proven track record of success',
    'Strong content',
    'Good communication during service development',
    'Strong business case',
    'Offer exclusivity',
    'Understand consumer needs/have consumer insights',
    'Exceptional marketing skills',
    'Excellent customer service (for MNO partner)',
    'Excellent customer service (for subscribers)',
    'Good value for money',
    'Strong market share',
    'Tech integration',
    'Existing partnerships with relevant organisations',
]

PERIOD = [
    '3 months',
    '6 months',
    '12 months',
]


# COMMANDS
# ---------------------------------------------------------------------------------------------------------------------#
class Command(BaseCommand):
    help = "Sync FactBook with external APIs!"

    def handle(self, *args, **options):
        logger.info('Erasing data...')
        # TODO: optionally clear all data...

        for challenge in CHALLENGES:
            instance, created = Challenge.objects.get_or_create(name=challenge, private=False)
            if created:
                instance.save()

        for service in SERVICES:
            instance, created = Service.objects.get_or_create(name=service, private=False)
            if created:
                instance.save()

        for reliable in RELIABLE_ATTRIBUTES:
            instance, created = Reliable.objects.get_or_create(name=reliable, private=False)
            if created:
                instance.save()

        for period in PERIOD:
            instance, created = Period.objects.get_or_create(name=period, private=False)
            if created:
                instance.save()

        logger.info('Done')
