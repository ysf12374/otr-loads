"""
Django settings for conciergeek project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0s&x1@m4_s9-j9642ifu0o_k80k5ym3)r1c2(u$!y6y+#9y@c^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blogs.apps.BlogsConfig',
    'rest_framework',
    'sslserver',
    # 'django.contrib.gis',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',
    # 'csp.contrib.rate_limiting.RateLimitedCSPMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'conciergeek.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'csp.context_processors.nonce'
            ],
        },
    },
]

WSGI_APPLICATION = 'conciergeek.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'postgres',

        'USER': 'otr_just_maps',

        'PASSWORD': 'otrdev123321',

        'HOST': 'otr.ciwoso6g1uql.us-east-1.rds.amazonaws.com',

        'PORT': '5432',
    },
}
# DATABASES = {
#     "default": {
#         "ENGINE": os.environ.get("ENGINE", 'django.contrib.gis.db.backends.postgis'),
#         "NAME": os.environ.get("DB_NAME", os.path.join(BASE_DIR, "db.sqlite3")),
#         "USER": os.environ.get("POSTGRES_USER", "user"),
#         "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "password"),
#         "HOST": os.environ.get("DB_HOST", "localhost"),
#         "PORT": os.environ.get("DB_PORT", "5432"),
#     }
# }

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'conciergeek/static')
]

MEDIA_URL = 'media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

POSITIONSTACK_KEY="e4e66d21cb433f08d2e9c39dc3e1061f"

# # https://django-csp.readthedocs.io/en/latest/configuration.html
# CSP_DEFAULT_SRC = ["*"]
# # When DEBUG is on we don't require HTTPS on our resources because in a local environment
# # we generally don't have access to HTTPS. However, when DEBUG is off, such as in our
# # production environment, we want all our resources to load over HTTPS
# CSP_UPGRADE_INSECURE_REQUESTS = not DEBUG
# # For roughly 60% of the requests to our django server we should include the report URI.
# # This helps keep down the number of CSP reports sent from client web browsers
# CSP_REPORT_PERCENTAGE = 0.6
# CSP_FRAME_SRC = ["'self'","https://*.loadotr.com"]
# CSP_INCLUDE_NONCE_IN = ["script-src"]

# CSP_SCRIPT_SRC = ["*"
# ]

# CSP_STYLE_SRC = ["*"]

# CSP_IMG_SRC = ["*"
# ]

CSP_DEFAULT_SRC = ["'self'"]

# CSP_IMG_SRC = ["'*'","*","'self'","'unsafe-inline'",'data','data-uris','data:image/svg+xml','https://api.mapbox.com','https://unpkg.com','https://www.w3.org']
CSP_IMG_SRC = ["'self'",'data: image/svg+xml','https://api.mapbox.com','https://unpkg.com','https://www.w3.org',
                'https://d1nhio0ox7pgb.cloudfront.net']

CSP_FRAME_ANCESTORS = ["'self'", 'https://*.loadotr.com' ]

CSP_STYLE_SRC = ["'self'","'unsafe-inline'",
"'self'",'https://unpkg.com/leaflet@1.7.1/dist/leaflet.css',
'https://cdnjs.cloudflare.com',
'https://maxcdn.bootstrapcdn.com',
'https://fonts.googleapis.com',
'https://cdn.jsdelivr.net',
'https://ka-f.fontawesome.com']
CSP_FONT_SRC = ["'self'","'unsafe-inline'",'https://fonts.gstatic.com','https://ka-f.fontawesome.com']
CSP_CONNECT_SRC = ["'unsafe-inline'",
"'self'",'https://ka-f.fontawesome.com','https://maps.googleapis.com','https://router.hereapi.com']
CSP_SCRIPT_SRC = ["'self'","'unsafe-inline'",'https://dev.sc.loadotr.com',
     'https://test.sc.loadotr.com',
	 'https://unpkg.com',
	 'https://code.jquery.com',
	 'https://cdnjs.cloudflare.com',
	 'https://cdn.jsdelivr.net',
	 'https://maxcdn.bootstrapcdn.com',
	 'https://kit.fontawesome.com', 'googleanalytics.com','https://rawgit.com','https://d3js.org',
     'https://d3js.org','https://maps.googleapis.com','https://router.hereapi.com','https://cdn.amcharts.com']

X_FRAME_OPTIONS = 'ALLOW-FROM https://*.loadotr.com'

