import json
from enum import Enum

from django.core.management.base import BaseCommand

from lmdbapp.management.utils import EnumAction
from lmdbapp.models import Person, Work, Country, Genre, Language


def get_valid_entries(rows, entry_type):
    for row in rows:
        entry = json.loads(row)
        if entry['imdb_id'].startswith(entry_type.value):
            yield entry


class Command(BaseCommand):
    help = 'Import films from json'

    class DatabaseEntryType(Enum):
        PERSON = 'nm'
        WORK = 'tt'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str)
        parser.add_argument('type', type=self.DatabaseEntryType, action=EnumAction)

    def handle(self, *args, **options):
        filepath = options['filepath']
        entry_type = options['type']
        with open(filepath) as file:
            rows = get_valid_entries(file, entry_type)
            if entry_type == self.DatabaseEntryType.PERSON:
                self.insert_people(rows)
            else:
                self.insert_works(rows)

    def insert_works(self, works):
        for work in works:
            countries = [Country(code=country['code'], name=country['name']) for country in work['countries']]
            Country.objects.bulk_create(countries, ignore_conflicts=True)

            Genre.objects.bulk_create([Genre(name=genre) for genre in work['genres']], ignore_conflicts=True)

            languages = [Language(code=language['code'], name=language['name']) for language in work['languages']]
            Language.objects.bulk_create(languages, ignore_conflicts=True)

            work_instance = Work.objects.create(
                imdb_id=work['imdb_id'],
                imdb_rating=work['imdb_rating'],
                imdb_amount_ratings=work['imdb_votes'],
                work_type=work['work_type'],
                title=work['title'],
                length=work['length'],
                year=work['year'],
                image_url=work['image']
            )
            work_instance.directors.add(*Person.objects.filter(imdb_id__in=work['director_ids']))
            work_instance.writers.add(*Person.objects.filter(imdb_id__in=work['writer_ids']))
            work_instance.cast.add(*Person.objects.filter(imdb_id__in=work['cast_ids']))
            work_instance.countries.add(*Country.objects.filter(code__in=[country.code for country in countries]))
            work_instance.genres.add(*Genre.objects.filter(name__in=work['genres']))
            work_instance.languages.add(*Language.objects.filter(code__in=[language.code for language in languages]))

    def insert_people(self, people):
        for person in people:
            birth_date = (person['birth_date'] or '').split('-')[0] or None
            Person.objects.create(imdb_id=person['imdb_id'], name=person['name'], year_born=birth_date, image_url=person['image'])
