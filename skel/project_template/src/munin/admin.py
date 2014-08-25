from django.contrib import admin

from .skel.conf.project_template.src.munin.models import MuninView


@admin.register(MuninView) 
class MuninViewAdmin(admin.ModelAdmin):
    list_display = ('html_graph', )
    list_filter = ('info', 'period')
    list_display_links = None
    
    actions = None
    
    def html_graph(self, obj):
        return obj.graph()
    html_graph.allow_tags = True
    html_graph.short_description = "Graph"