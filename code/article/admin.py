from django.contrib import admin
from .models import Article, ArticleStatisticAdmin, Profile, ProfileAdmin, TagsAdmin, TagsList, Products, ProductAdmin

admin.site.register(Article, ArticleStatisticAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(TagsList, TagsAdmin)
admin.site.register(Products, ProductAdmin)
