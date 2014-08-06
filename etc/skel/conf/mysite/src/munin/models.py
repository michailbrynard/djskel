from django.db import models
import base64

class MuninView(models.Model):
    BASE_URI = 'http://127.0.0.1/munin/localdomain/localhost.localdomain/'
    AUTH = ('admin', '1q2w3e4r')
    
    INFO_CHOICES = (
        ('memory', 'Memory'), 
        ('cpu', 'CPU Usage'), 
        ('if_eth0', 'Network Traffic'),  
        ('df', 'Disk Usage')
    )
    info = models.CharField(max_length=10, choices=INFO_CHOICES)
    
    PERIOD_CHOICES = (
        ('day', 'Day'), 
        ('week', 'Week'), 
        ('month', 'Month'),  
        ('year', 'Year'),
    )
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)

    
    def graph(self):
        import requests
        r = requests.get(
             self.BASE_URI + '%s-%s.png' % (self.info, self.period), 
             auth=self.AUTH,
        )
        
        png64 = base64.b64encode(r.content).decode('UTF-8')
        html_img = '<div style="width: 100%%; text-align: center;"><img src="data:image/png;base64,%s" />' % png64
        
        r.close()
        return html_img
    
    def __str__(self):
        return '%s - %s' % (self.info, self.period)
    
    class Meta:
        unique_together = ('info', 'period')
        verbose_name='Graph'
        verbose_name_plural='Graphs'
