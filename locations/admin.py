from django.contrib import admin

from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    actions = ('export_as_csv',)
    list_display = ('name', 'lat', 'long')
    list_per_page = 10
    search_fields = ('name',)

    @admin.action(description='Export selected locations as CSV')
    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="locations.csv"'
        writer = csv.writer(response)

        writer.writerow(['Name', 'Latitude', 'Longitude'])
        for location in queryset:
            writer.writerow([location.name, location.lat, location.long])

        return response
