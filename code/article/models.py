import os
from django.db import models
from django.contrib import admin
from django.conf import settings
from markdownx.models import MarkdownxField
from markdownx.widgets import AdminMarkdownxWidget
from multiselectfield import MultiSelectField


def get_upload_path(instance, filename):
    name = str(instance.id)
    path = os.getcwd() + f"/media/images/{name}"
    print("start")
    if os.path.exists(path):
        os.chdir(path)
        for file in os.listdir():
            print(file)
            os.remove(file)
        print(os.listdir())
    return os.path.join(settings.MEDIA_ROOT, 'images', name, filename)


class TagsList(models.Model):
    tag = models.CharField('name', max_length=50, default="home")
    description = models.TextField('Description', default="")

    def __str__(self):
        return self.tag


choices = [(c.tag, c.tag) for c in TagsList.objects.all()]


class Article(models.Model):
    article_title = models.CharField('Название статьи', max_length=200)  # название статьи
    article_picture = models.ImageField('Основная картинка', upload_to=get_upload_path, default='default.jpg')  # картинка
    article_small_text = models.TextField('Краткое описание')  # краткое описание
    article_content_md = MarkdownxField(null=True)  # markdown editor
    pub_date = models.DateField('Дата публикации')  # дата публикации
    likes = models.IntegerField('Лайки', default=0)  # количество просмтров
    time_to_read = models.IntegerField('Время чтения', default=1)
    tagArticle = MultiSelectField(choices=choices, max_choices=5, null=True)
    author_id = models.IntegerField(default=25)

    def __str__(self):
        return self.article_title

    def save(self, *args, **kwargs):
        self.time_to_read = len(str(self.article_content_md)) // 1400
        if self.time_to_read == 0: self.time_to_read = 1
        super(Article, self).save(*args, **kwargs)


class Products(models.Model):
    product_title = models.CharField('Название статьи', max_length=200)  # название статьи
    product_picture = models.ImageField('Основная картинка', upload_to='images/')  # картинка
    product_small_text = models.TextField('Краткое описание')  # краткое описание
    article_content_md = MarkdownxField(null=True)  # markdown editor
    pub_date = models.DateField('Дата публикации')  # дата публикации
    likes = models.IntegerField('Лайки', default=0)  # количество просмтров
    downloads = models.IntegerField('Лайки', default=0)  # количество просмтров

    def __str__(self):
        return self.product_title

    def save(self, *args, **kwargs):
        super(Products, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField('Аватарка', upload_to='users/')
    description = models.TextField('Description', default='', null=False, blank=True)
    where_you_leave = models.TextField('Где вы живете?', default='Парадиз', blank=True, null=True)
    date_of_birth = models.DateField('Дата рождения (необязательно)', blank=True, null=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'date_of_birth', 'avatar')


class ArticleStatisticAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js',
        )
        css = {

        }

    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }
    list_display = ('__str__', 'likes')  # отображаемые поля в админке


class TagsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'description')  # отображаемые поля в админке


class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'product_title', 'likes')