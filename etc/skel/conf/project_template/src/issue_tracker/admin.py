from django.contrib import admin
from issue_tracker.models import Ticket, Comment


class CommentInline(admin.StackedInline):
    model = Comment
    
    fieldsets = [
        (None, {'fields': [('submitted_by', 'submitted_on')]}),
        (None, {'fields': ['comment', ], 'classes': ['wide']})
    ]
    
    readonly_fields = ['submitted_by', 'submitted_on']
    
    can_delete = False
    extra = 0
    
    def save_model(self, request, obj, form, change): 
        if not obj.pk:
            obj.submitted_by = request.user

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'submitted_by',
        'submitted_on', 'modified_on')
    list_filter = ('priority', 'status', 'submitted_on')
    search_fields = ('title', 'description',)
    
    #readonly_fields = ('status',)
    
    inlines = [CommentInline, ]
    
    def save_model(self, request, obj, form, change): 
        if not obj.pk:
            obj.submitter = request.user
            obj.assigned_to  = request.user
        
        obj.save()
        

admin.site.register(Ticket, TicketAdmin)
