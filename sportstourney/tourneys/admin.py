from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(userg)
admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Event)
admin.site.register(Bracket)
