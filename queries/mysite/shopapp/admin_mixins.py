import csv
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from django.db.models.options import Options


class ExportAsCSVMixin:
    def export_csv(self, request: HttpRequest, queryset: QuerySet):
        meta: Options = self.model._meta
        field_name = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={meta}-export.csv"
        csv_writer = csv.writer(response)
        csv_writer.writerow(field_name)

        for obj in queryset:
            csv_writer.writerow([getattr(obj, field) for field in field_name])
        return response
    export_csv.short_description = "Export as CSV"