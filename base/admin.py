from django.contrib import admin

# Register your models here.

from .models import Performance, Athlete,Event, User, Meet

admin.site.register(User)
admin.site.register(Athlete)
admin.site.register(Event)
admin.site.register(Meet)
admin.site.register(Performance)

