from django.contrib import admin
from .models import SearchHistory


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['query_type', 'query_text', 'created_at']
    list_filter = ['query_type', 'created_at']
    search_fields = ['query_text', 'result']
    readonly_fields = ['created_at']
