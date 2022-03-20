from django.contrib import admin

# Register your models here.
from .models import Category, User, UserProfile , lead , Agent

admin.site.register(User)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(lead)
admin.site.register(Agent)