from django.contrib import admin
from .models import PDFHistory

@admin.register(PDFHistory)
class PDFHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "pdf_name", "uploaded_at")
    search_fields = ("user__username", "pdf_name")
    list_filter = ("uploaded_at",)
