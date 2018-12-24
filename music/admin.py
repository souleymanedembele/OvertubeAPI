from django.contrib import admin
from .models import *
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']

# Register your models here.
admin.site.register(Music)
admin.site.register(MusicCategory)
admin.site.register(Artist)
admin.site.register(ArtistScore)
admin.site.register(Profile, ProfileAdmin)
