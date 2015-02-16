# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
import random
import string
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.utils import IntegrityError
from guardian.shortcuts import assign_perm
from survey.models import Survey, Challenge, ChallengeDetail
from fact_book.models import Country
from os import path
import pandas as pd
from logging import getLogger


# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
logger = getLogger('django')


# FUNCTIONS
# ---------------------------------------------------------------------------------------------------------------------#
def slug_generator(size=15, characters=string.ascii_letters + string.digits):
    """Return a random string of ascii characters and digits
    :param size:
    :param characters:
    :return:
    """
    # str(uuid.uuid4().hex[0:15])
    slug = ''.join(random.choice(characters) for _ in range(size))
    return slug


# COMMANDS
# ---------------------------------------------------------------------------------------------------------------------#
class Command(BaseCommand):
    help = "Sync FactBook with external APIs!"

    def handle(self, *args, **options):
        # TODO: Remove or improve before production...
        logger.info('Deleting all surveys...')

        User.objects.filter(is_staff=False).delete()
        Survey.objects.all().delete()
        ChallengeDetail.objects.all().delete()

        logger.info('Starting import...')
        df = pd.read_excel(path.join(settings.BASE_DIR, 'respondents.xlsx'), sheetname='Delegates')
        df.fillna('', inplace=True)

        for idx, survey in df.iterrows():
            data_raw = survey.to_dict()
            data = {k: str(v).strip() for k, v in data_raw.items()}

            try:
                country = Country.objects.get(name=data.get('country_of_operation'))
                data.update({'country_of_operation': country})

            except Country.DoesNotExist:
                logger.warning('Could not find country %s' % data.get('country_of_operation'))
                data.update({'country_of_operation': None})

            del data['countries']

            # Create and associate user
            username = slugify(data.get('name')).replace('-', '_')
            slug = '{0}_{1}'.format(data.get('slug')[2:] or slug_generator(), username)
            logger.info(slug)
            user = User.objects.create_user(username[:30], data.get('email', ''), slug)

            survey = Survey(**data)
            survey.slug = slug
            survey.user = user
            survey.save()
            assign_perm('change_survey', user, obj=survey)

            # Creating challenges
            # for challenge in Challenge.objects.all():
            #     ChallengeDetail.objects.create(owner=slug, challenge=challenge)

            for rank in range(1, 4):
                ChallengeDetail.objects.create(respondent=survey, rank=rank)

            # try:
            #     Survey(**data).save()
            # except IntegrityError:
            #     logger.excep('Integ exisits: %s ' % data)
            # except:
            #     logger.exception(data)
            # else:
            #     for challenge in Challenge.objects.all():
            #         ChallengeDetail.objects.create(slug, challenge)

        logger.info('Done')
