import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create file 'secret_key' with the secret for your product
# SECURITY WARNING: keep the secret key used in production secret!
with open(os.path.join(BASE_DIR, 'photoclo/secret_key')) as file:
    SECRET_KEY = file.read()

# Create file 'debug' in this directory, to enable debug mode
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.path.exists(os.path.join(BASE_DIR, 'photoclo/debug'))

ALLOWED_HOSTS = [
    'photoclo.ru',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'app.web',
    'app.photo_load',
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

ROOT_URLCONF = 'photoclo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'photoclo.wsgi.application'


# File with database configuration, separated by new line
with open(os.path.join(BASE_DIR, 'photoclo/database.config')) as file:
    db_config = file.read().split()

DATABASES = {
    'default': {
        'ENGINE': db_config[0],
        'NAME': db_config[1],
        'USER': db_config[2],
        'PASSWORD': db_config[3] if db_config != 'NULL' else None,
        'HOST': db_config[4],
        'PORT': db_config[5],
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

MEDIA_ROOT = 'media/'
MEDIA_URL = '/media/'
