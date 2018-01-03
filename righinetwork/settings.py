import os

from . import private_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = private_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',

	'allauth',
	'allauth.account',
	'allauth.socialaccount',

	'allauth.socialaccount.providers.facebook',
	# 'allauth.socialaccount.providers.google',
	# 'allauth.socialaccount.providers.instagram',

	'django_summernote',
	'hijack',
	'compat',
	'hijack_admin',
	'markdown_deux',
	'silk',
	"taggit",

	'accounts',
	'assemblee',
	'blog',
	'sondaggi',
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

LOGIN_EXEMPT_URLS = (
	r'^account/',
)

ROOT_URLCONF = 'righinetwork.urls'

TEMPLATES = [
	{
		"BACKEND": "django.template.backends.django.DjangoTemplates",
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
		"APP_DIRS": True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			]
		}
	}
]

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
	'allauth.account.auth_backends.AuthenticationBackend',
)

WSGI_APPLICATION = 'righinetwork.wsgi.application'

# Database

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'RighinetworkDB'),
	}
}

# Password validation

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
SOCIALACCOUNT_QUERY_EMAIL = True
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
		'VERSION': 'v2.9',
	}
}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "/"

ACCOUNT_FORMS = {'login': 'accounts.forms.UserLoginForm'}

EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_HOST_USER = 'noreply@righi-network.com'
EMAIL_HOST_PASSWORD = private_settings.EMAIL_HOST_PASSWORD
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'noreply@righi-network.com'

# Impostazioni hijack

HIJACK_LOGIN_REDIRECT_URL = '/'
HIJACK_LOGOUT_REDIRECT_URL = '/admin/auth/user/'
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

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "static"),
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_cdn")
