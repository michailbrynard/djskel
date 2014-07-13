# LOGGING
import logging

log = logging.getLogger('django')
log.setLevel(logging.INFO)


def more_context(request):
    return {
        'var3': '!',
    }