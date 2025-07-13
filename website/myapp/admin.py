from django.contrib import admin
from .models import School, Group, Student , Sport
from django.utils.html import format_html

admin.site.site_header = "Kaliganj Anchal Sports"
admin.site.site_title = "Kaliganj Anchal Sports Dashboard"
admin.site.index_title = "Welcome to Kaliganj Anchal Sports Admin Panel"

admin.site.register(School)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'id_number', 'school', 'group', 'gender', 'image_preview', 'created_at')
    list_filter = ('school', 'group', 'gender')
    search_fields = ('name', 'id_number', 'school__name')

    def image_preview(self, obj):  # 🔁 Must match the name in list_display
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "-"
    
    image_preview.short_description = 'Photo'
    
class SportInline(admin.TabularInline):  # or admin.StackedInline
    model = Sport
    extra = 1  # number of empty sport forms shown

class GroupAdmin(admin.ModelAdmin):
    inlines = [SportInline]  # 👈 allows adding sports inside group admin

admin.site.register(Group, GroupAdmin)
admin.site.register(Sport)  # optional: register separately if needed