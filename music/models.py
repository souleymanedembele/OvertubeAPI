from django.db import models

# Create your models here.
from Overtube import settings


class MusicCategory(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class Music(models.Model):
    owner = models.ForeignKey(
        'auth.User',
        related_name= 'musics',
        null=True, blank=True,
        on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, unique=True)
    music_category = models.ForeignKey(MusicCategory, related_name='musics', on_delete=models.CASCADE)
    release_date = models.DateTimeField()
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    video = models.FileField(upload_to='videos/%Y/%m/%d', null=True, verbose_name="")

    class Meta:
        ordering = ('-release_date',)

    def __str__(self):
        return self.name

class Artist(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'),)
    name = models.CharField(max_length=50, blank=False, default='')
    created = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default=MALE,)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class ArtistScore(models.Model):
    artist = models.ForeignKey(Artist, related_name='scores', on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    score = models.IntegerField()
    score_date = models.DateTimeField()

    class Meta:
        ordering = ('-score',)

class Profile(models.Model):
    user = models.ForeignKey('auth.User', related_name= 'profiles', on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)