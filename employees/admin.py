from django.contrib import admin
from django.utils.html import format_html

from .models import Employee


def delete_paid_salary(self, request, queryset):
    updated = queryset.update(total_paid=0)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_filter = ('position', 'level')
    list_display = ('full_name', 'position', 'manager_link', 'salary', 'total_paid')
    actions = [delete_paid_salary]

    def manager_link(self, obj):
        if obj.manager:
            url = f"/admin/employees/employee/{obj.manager.id}/change/"
            return format_html('<a href="{}">{}</a>', url, obj.manager.full_name)
        return "-"

    manager_link.short_description = 'Начальник'