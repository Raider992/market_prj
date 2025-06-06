from django.db import models

class ListOfCountries(models.Model):
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def  __str__(self):
        return self.name


class Regions(models.Model):
    country = models.ForeignKey(ListOfCountries, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return self.name

class Accommodation(models.Model):
    country = models.ForeignKey(ListOfCountries, on_delete=models.CASCADE)
    region = models.ForeignKey(Regions, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='название отеля', max_length=128, unique=True)
    image = models.ImageField(upload_to='media/', blank=True)
    short_desc = models.TextField(verbose_name='краткое описание отеля', max_length=60, blank=True)
    description = models.TextField(verbose_name='подробное описание отеля', blank=True)
    availability = models.PositiveIntegerField(verbose_name='количество свободных номеров')
    price = models.DecimalField(verbose_name='цена номера', max_digits=8, decimal_places=2, default=0)
    room_desc = models.TextField(verbose_name='краткое описание номера', max_length=60, blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    @staticmethod
    def get_items():
        return Accommodation.objects.filter(is_active=True).order_by('country', 'regions', 'name')

    def __str__(self):
        return self.name
