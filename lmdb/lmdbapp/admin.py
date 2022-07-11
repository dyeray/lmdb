from django.contrib import admin
from lmdbapp.models import Work, Person


class DirectedInline(admin.TabularInline):
    model = Work.directors.through


class PersonAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    inlines = (DirectedInline,)


admin.site.register(Work)
admin.site.register(Person, PersonAdmin)
