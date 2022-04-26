from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    slug = models.SlugField(unique=True, db_index=True)
    messages_count = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    name = models.CharField(max_length=25, blank=True, verbose_name='Имя')
    surname = models.CharField(max_length=25, blank=True, verbose_name='Фамилия')
    biography = models.TextField(blank=True, verbose_name='О себе')
    photo = models.ImageField(upload_to="photos/", default="photos/default.jpg", verbose_name='Фото профиля')
    email = models.CharField(max_length=100, blank=True, verbose_name='Почта')
    github = models.CharField(max_length=100, blank=True, verbose_name='Гитхаб')
    telegram = models.CharField(max_length=100, blank=True, verbose_name='Телеграм')
    time_create = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True, verbose_name='Публичный профиль')
    verify_code = models.IntegerField(default=-1)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username_slug': self.slug})

    class Meta:
        verbose_name = 'Профили'
        verbose_name_plural = 'Профили'


class Section(models.Model):
    name = models.CharField(max_length=50)
    topics_count = models.IntegerField(default=0)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('section', kwargs={'section_id': self.pk})

    class Meta:
        verbose_name = 'Разделы'
        verbose_name_plural = 'Разделы'
        ordering = ['name', 'time_create']


class Topic(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    description = models.CharField(max_length=50, verbose_name='Краткое описание')
    posts_count = models.IntegerField(default=0)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    section = models.ForeignKey('Section', on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('topic', kwargs={'topic_id': self.pk, 'section_id': self.section.pk})

    class Meta:
        verbose_name = 'Темы'
        verbose_name_plural = 'Темы'
        ordering = ['posts_count', 'time_create', 'name']


class Post(models.Model):
    post = models.TextField(blank=False)
    start_post = models.BooleanField(default=False)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    reply_to = models.TextField(blank=True)
    reply_watched = models.BooleanField(default=False)
    topic = models.ForeignKey('Topic', on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.post

    class Meta:
        verbose_name = 'Посты'
        verbose_name_plural = 'Посты'
        ordering = ['time_create']