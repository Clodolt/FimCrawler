from django.contrib import admin
from .models import Profile
from .models import Journal

admin.site.register(Journal)
admin.site.register(Profile)

