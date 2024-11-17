from django.contrib import admin
from chats.models import Chat_Message, Company, Profile, My_Note, To_Do

# Register your models here.
admin.site.register(Chat_Message)
admin.site.register(Company)
admin.site.register(Profile)
admin.site.register(My_Note)
admin.site.register(To_Do)
