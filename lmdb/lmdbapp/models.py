from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name


class Person(models.Model):
    imdb_id = models.CharField(max_length=16)
    name = models.CharField(max_length=255)
    year_born = models.IntegerField(null=True)
    country_born = models.ForeignKey(Country, on_delete=models.RESTRICT, null=True)
    image_url = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Person: imdb_id={self.imdb_id} name={self.name}>'


class Genre(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name


class Work(models.Model):
    imdb_id = models.CharField(max_length=10)
    imdb_rating = models.FloatField(null=True)
    imdb_amount_ratings = models.IntegerField()
    work_type = models.CharField(max_length=16)
    title = models.CharField(max_length=255)
    directors = models.ManyToManyField(Person, related_name='directed_works')
    writers = models.ManyToManyField(Person, related_name='written_works')
    cast = models.ManyToManyField(Person, related_name='starred_in')
    countries = models.ManyToManyField(Country)
    genres = models.ManyToManyField(Genre)
    languages = models.ManyToManyField(Language)
    length = models.IntegerField(null=True)
    year = models.IntegerField()
    image_url = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'<Work: imdb_id={self.imdb_id} title={self.title}>'
