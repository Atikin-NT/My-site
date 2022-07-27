"""
Django settings for niktech project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
from datetime import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from pymdownx import arithmatex

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ROOT = os.path.dirname(__file__)

BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_ROOT, 'components')

LOGIN_REDIRECT_URL = '/'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cp4#8f-dd(9*675v3dm*la+@)939ua7tr)ljj_9^)xq7_tddy*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'article.apps.ArticleConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'multiselectfield',
    'markdownx',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'debug_toolbar',
    # 'captcha',
]

INTERNAL_IPS = [
    "127.0.0.1",
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'niktech.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'article/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'string_if_invalid': 'ζ༼Ɵ͆ل͜Ɵ͆༽ᶘ',
            'file_charset': 'utf-8',
            'debug': True,
        },
    },
]

WSGI_APPLICATION = 'niktech.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Markdownify
MARKDOWNX_MARKDOWNIFY_FUNCTION = 'markdownx.utils.markdownify'  # Default function that compiles markdown using defined extensions

# Markdown extensions
MARKDOWNX_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.footnotes',
    'pymdownx.emoji',  # исправить перенос на новую строку
    'markdown.extensions.footnotes',
    'markdown.extensions.attr_list',
    'markdown.extensions.def_list',
    'markdown.extensions.tables',
    'markdown.extensions.abbr',
    'markdown.extensions.md_in_html',
    'pymdownx.caret',  # ok
    'pymdownx.details',  # ! добавить css https://facelessuser.github.io/pymdown-extensions/extensions/details/
    'pymdownx.highlight',  # подсветка синтаксиса, проблема css
    'pymdownx.superfences',
    'pymdownx.keys',  # подсветка клавиш. На базовом уровне работает
    'pymdownx.mark',  # выделение текста
    'pymdownx.progressbar',  # прогрессбар
    'pymdownx.smartsymbols',  # спец знаки
    'pymdownx.tabbed',  # вкладки с контентом
    'pymdownx.tasklist',  # выполнил / не выполнил, доработать стили!
    'pymdownx.arithmatex',  # матан
    # 'mdx_math',
    # 'markdown_katex',
]
MARKDOWN_EXTENSIONS = ['extra']
MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS = {
    "pymdownx.tasklist": {
        "custom_checkbox": True,
    },
    "pymdownx.highlight": {
        'use_pygments': True,
        'guess_lang': True,
        'noclasses': False,
        'pygments_style': 'friendly',
    },
    "pymdownx.arithmatex": {
        'generic': True,
    }
}

# Markdown urls
MARKDOWNX_URLS_PATH = '/markdownx/markdownify/'  # Path that returns compiled markdown text. Change it to your custom app url which could i.e. enable you todo some additional work with compiled markdown text. More info at "Custom MARKDOWNX_URLS_PATH / Further markdownified text manipulations" below.
MARKDOWNX_UPLOAD_URLS_PATH = '/markdownx/upload/'  # Path that accepts file uploads, returns markdown notation of the image.

# Media path
# MARKDOWNX_MEDIA_PATH = 'markdownx/'  # Subdirectory, where images will be stored in MEDIA_ROOT folder
MARKDOWNX_MEDIA_PATH = datetime.now().strftime(
    'markdownx/%Y/%m/%d')  # Subdirectory, where images will be stored in MEDIA_ROOT folder

# Image
MARKDOWNX_UPLOAD_MAX_SIZE = 52428800  # 50MB # Maximum file size
MARKDOWNX_UPLOAD_CONTENT_TYPES = ['image/jpeg', 'image/png', 'image/gif']  # Acceptable file types
MARKDOWNX_IMAGE_MAX_SIZE = {'size': (1300, 1300),
                            'quality': 90, }  # Different options describing final image size, compression etc. after upload.

# Editor
MARKDOWNX_EDITOR_RESIZABLE = True  # Update editor's height to inner content height while typing

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#   --------------------------------------------login----------------------------------------------------------------
# LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
PASSWORD_RESET_TIMEOUT_DAYS = 1

# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
