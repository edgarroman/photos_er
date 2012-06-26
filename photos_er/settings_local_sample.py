# Django settings for edgar_project project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        # Local debugging sqlite
        'ENGINE': 'django.db.backends.sqlite3',  # use this for local debugging
        'NAME': 'C:/Users/username/code/photos_er/windows/sqlite3.db',
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Not used with sqlite3.
        'PORT': '',                      # Not used with sqlite3.
        # Live site settings
        #'ENGINE': 'django.db.backends.mysql',   # use this for live site
        #'NAME': 'photos_er_db',                      
        #'USER': 'username',
        #'PASSWORD': 'password',                  
        #'HOST': '',
        #'PORT': '',
    }
}

# if you want to use Google Analytics to track your site actvity
BRAND_GA_CODE = ''

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/user/site.com/photos_er/media/'

# Make this unique, and don't share it with anybody.
# generate this using: http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = ''

TEMP_DIRECTORY = '/home/user/site.com/photos_er/tmp/'

