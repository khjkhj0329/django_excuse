from django.contrib import admin
from .models import Excuse

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Excuse, QuestionAdmin)

# Register your models here.
