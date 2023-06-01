"""
Django settings for Social2023 project.
"""
# pip install social-auth-app-django автоизация
# pip install django-extensions
# pip install werkzeug
# pip install pyOpenSSL
# python manage.py runserver_plus --cert-file cert.crt

# pip install requests  # Когда пользователь добавляет изображение в закладки, нам нужно будет загрузить файл изображения по его URL-адресу.
# pip install easy-thumbnails
# pip install redis

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import social_core.backends.vk
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o92!oqnladlimdh*7!s0ohfl$h74)dyk0)$jq1munppu-4!)!3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['mysite.com', 'localhost', '127.0.0.1']

# user login #########################################33
LOGIN_REDIRECT_URL = 'dashboard'  # куда юзера при успешной авторизации
LOGIN_URL = 'login'  # куда юзера для входа в систему
LOGOUT_URL = 'logout'  # выхода

# для паролей , если хотим изменить алгоритм шифрования то тут копает
# PASSWORD_HASHERS = [
# 'django.contrib.auth.hashers.PBKDF2PasswordHasher',
# 'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
# 'django.contrib.auth.hashers.Argon2PasswordHasher',
# 'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
# 'django.contrib.auth.hashers.ScryptPasswordHasher',
# ]

# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account.apps.AccountConfig',  # должно быть обязательно что искало первым шаблоны регитрации
    'social_django',  # авторизация чеез соц сети
    'django_extensions',  # допы к авторизации ССЛ и т.п.
    'images',
    'easy_thumbnails', # для миниатюр
    'actions.apps.ActionsConfig',
]

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Social2023.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  # Добавил эту строку
            ],
        },
    },
]

WSGI_APPLICATION = 'Social2023.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # для реальной отправки почты

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'elskazi@yandex.ru'
EMAIL_HOST_PASSWORD = 'sgvmgfsvrvzobjev'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Вход по емайлу или по логину
AUTHENTICATION_BACKENDS = [
    "social_core.backends.vk.VKOAuth2",
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend',
]

# Надо ИД приложения сверху самое и ключ, сервисный не надо
# 51584390
# wNIAI05C4Wb1UjdvLOqN

SOCIAL_AUTH_VK_OAUTH2_KEY = '51584390'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'wNIAI05C4Wb1UjdvLOqN'
# SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email'] #ошибка надо попобывать с ХТППС

SOCIAL_AUTH_PIPELINE = [
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'account.authentication.create_profile',  # Функция из authentication
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
]

# if DEBUG:
#     import mimetypes
#     mimetypes.add_type('application/javascript', '.js', True)
#     mimetypes.add_type('text/css', '.css', True)

'''
Ссылка для добавления изображения так как JS не хочет работьа 
http://127.0.0.1:8002/images/create/?title=test&url=https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Zhang_zifeng.m.jpg/800px-Zhang_zifeng.m.jpg
'''

# Теперь мы можем вызвать метод
# get_absolute_url() для объекта User, чтобы получить его канонический адрес
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('user_detail', args=[u.username])
}

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0