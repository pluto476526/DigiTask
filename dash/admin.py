from django.contrib import admin
from dash.models import Nature, Category, Job_Listing , Feedback, Job_Proposal, Notification, Note_Type

# Register your models here.

admin.site.register(Nature)
admin.site.register(Category)
admin.site.register(Job_Listing)
admin.site.register(Feedback)
admin.site.register(Job_Proposal)
admin.site.register(Notification)
admin.site.register(Note_Type)
