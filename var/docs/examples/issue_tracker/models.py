from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


STATUS_CODES = (
    (1, _('Open')),
    (2, _('Working')),
    (3, _('Closed')),
)

PRIORITY_CODES = (
    (1, _('Now')),
    (2, _('Soon')),
    (3, _('Someday')),
)

apps = [('general', 'General'), ('reports', 'SLA Reporting'), ('graphs', 'IRIS Graphs'), ('munin', 'Server Graphs'), ('laf', 'Look & Feel'), ('security', 'Security')]

#[app for app in settings.INSTALLED_APPS if not (app.startswith('django.') or app.startswith('libs.'))]

class Ticket(models.Model):
    """Trouble tickets"""
    title = models.CharField(_('title'), max_length=100)
    project = models.CharField(_('project'), blank=True, max_length=100, choices=apps)
    
    submitted_on = models.DateField(_('date submitted'), auto_now_add=True)
    modified_on = models.DateField(_('date modified'), auto_now=True)
    
    submitted_by = models.ForeignKey(User, verbose_name=_('submitter'), editable=False)
    assigned_to = models.ForeignKey(User, verbose_name=_('assigned to'), related_name='assignee', blank=True, editable=False)
    description = models.TextField(_('description'), blank=True)
    status = models.IntegerField(_('status'), default=1, choices=STATUS_CODES)
    priority = models.IntegerField(_('priority'), default=1, choices=PRIORITY_CODES)

    class Meta:
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')
        ordering = ('status', 'priority', 'submitted_on', 'title')

    def __unicode__(self):
        return self.title
    
class Comment(models.Model):  
    ticket = models.ForeignKey(Ticket)
    comment = models.TextField()
    
    submitted_by = models.ForeignKey(User, verbose_name=_('submitter'), editable=False)
    submitted_on = models.DateField(_('date submitted'), auto_now_add=True)
    
    modified_on = models.DateField(_('date modified'), auto_now=True)
      
