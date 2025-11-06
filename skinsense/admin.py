from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Case, FollowUp

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'condition', 'risk_level', 'confidence', 'created_at')
    list_filter = ('risk_level', 'condition', 'created_at')
    search_fields = ('user__username', 'condition', 'risk_level')
    ordering = ('-created_at',)

@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = ('id', 'case', 'condition', 'confidence', 'risk_level', 'created_at')
    list_filter = ('risk_level', 'condition', 'created_at')
    search_fields = ('case__user__username', 'condition')
    ordering = ('-created_at',)
