"""
Django settings for pac project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import settings as sets
import django.contrib.contenttypes

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nh_wdq=#w!f0#fumj5sxdxw72ux!r2gkj(6&7abfd3nx4kq%c)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = sets.IS_DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'users',
    'REST', 'rest_framework',
    'ALLSP',
    'TXSP',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  #
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pac.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 项目文件夹名称
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pac.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': sets.DATABASES_ENGINE,
        'NAME': sets.DATABASES_NAME,
        'USER': sets.DATABASES_USER,
        'PASSWORD': sets.DATABASES_PASSWORD,
        'HOST': sets.DATABASES_HOST,
        'PORT': sets.DATABASES_PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'z' \
                'h-hans'  # 语言

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'  # 时区

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = sets.STATIC_ROOT

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),  # 项目文件夹名称
)

AUTH_USER_MODEL = 'users.User'  # 自定义用户对象

LOGOUT_REDIRECT_URL = '/'  # 缺省的跳转路径 - 登出后
LOGIN_REDIRECT_URL = '/'  # 缺省的跳转路径 - 登录后

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # 模拟发送邮件，到终端

# 用户的凭据信息进行验证 - 登录
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'users.backends.EmailBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

