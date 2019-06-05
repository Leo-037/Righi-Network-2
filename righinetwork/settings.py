import os

from . import private_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = private_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'righi-network.com', 'www.righi-network.com', '206.189.14.45']


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.flatpages',
	'django.contrib.messages',
	'django.contrib.staticfiles',

	'allauth',
	'allauth.account',
	'allauth.socialaccount',
	'allauth.socialaccount.providers.facebook',

	'django_summernote',
	'hijack',
	'compat',
	'hijack_admin',
	'markdown_deux',
	'silk',
	'taggit',

	'import_export',

	'accounts',
	'assemblee',
	'blog',
	'merchandising',
	'recuperi',
	'sondaggi',
	'tutoring',
]

MIDDLEWARE = [
	'silk.middleware.SilkyMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'righinetwork.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

LOGIN_EXEMPT_URLS = (
	r'^account/',
)

AUTHENTICATION_BACKENDS = (
	'allauth.account.auth_backends.AuthenticationBackend',
	'django.contrib.auth.backends.ModelBackend',
)

WSGI_APPLICATION = 'righinetwork.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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


LOGIN_URL = '/accounts/login/'

# impostazioni Allauth

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
# noinspection SpellCheckingInspection
SOCIALACCOUNT_QUERY_EMAIL = True
# noinspection SpellCheckingInspection,SpellCheckingInspection
SOCIALACCOUNT_PROVIDERS = {
	'facebook': {
		'METHOD': 'oauth2',
		'SCOPE': ['email', 'public_profile', 'user_friends'],
		'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
		'INIT_PARAMS': {'cookie': True},
		'FIELDS': [
			'id',
			'email',
			'name',
			'first_name',
			'last_name',
			'verified',
			'locale',
			'timezone',
			'link',
			'gender',
			'updated_time',
		],
		'EXCHANGE_TOKEN': True,
		'LOCALE_FUNC': lambda request: 'it',
		'VERIFIED_EMAIL': False,
		'VERSION': 'v2.5',
	}
}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "/"
ACCOUNT_SESSION_REMEMBER = False
ACCOUNT_PRESERVE_USERNAME_CASING = False

ACCOUNT_FORMS = {'login': 'accounts.forms.UserLoginForm'}

# noinspection SpellCheckingInspection
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
# noinspection SpellCheckingInspection,SpellCheckingInspection
EMAIL_HOST = 'authsmtp.securemail.pro'
EMAIL_HOST_USER = 'smtp@righi-network.com'
EMAIL_HOST_PASSWORD = private_settings.EMAIL_HOST_PASSWORD
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'smtp@righi-network.com'

# Impostazioni hijack

HIJACK_LOGIN_REDIRECT_URL = '/'
HIJACK_LOGOUT_REDIRECT_URL = '/gestione/'
HIJACK_USE_BOOTSTRAP = True
HIJACK_ALLOW_GET_REQUESTS = True

# Impostazioni Taggit

TAGGIT_CASE_INSENSITIVE = True

# Internationalization

LANGUAGE_CODE = 'it'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
