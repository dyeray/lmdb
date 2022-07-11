from enum import Enum, auto

from django.core.management.base import BaseCommand
from django.db.models import Count

from lmdbapp.management.utils import EnumAction
from lmdbapp.models import Person


class Command(BaseCommand):
    help = 'Reports'

    class Report(Enum):
        TOP_DIRECTORS = auto

    def add_arguments(self, parser):
        parser.add_argument('report', type=self.Report, action=EnumAction)

    def handle(self, *args, **options):
        report = options['report']
        match report:
            case self.Report.TOP_DIRECTORS:
                self.report_top_directors()

    def report_top_directors(self):
        directors = Person.objects\
            .annotate(num_films=Count('directed_works'))\
            .filter(num_films__gte=3)\
            .order_by('-num_films')\
            .values('name', 'num_films')
        for director in directors:
            print(f'{director["name"]}: {director["num_films"]}')
