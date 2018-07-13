# import os
# import logging.config


INSTALLED_APPS = [
    'src.entities'
]

SECRET_KEY = '8lu*6g0lg)9z!ba+a$ehk)xt)x%rxgb$i1&amp;022shmi1jcgihb*'
# LOGGING_CONFIG = None
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'console': {
#             # exact format is not important, this is the minimum information
#             'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#         },
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'console',
#         },
#     },
#     'loggers': {
#         # root logger
#         '': {
#             'level': 'WARNING',
#             'handlers': ['console'],
#         },
#     },
# }

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'blackpy',
    'USER': 'blackpy',
    'PASSWORD': '6X9IjDAGp69RHb',
    'HOST': 'mysql.blackpy.delvern.com',
    'PORT': '3306',
  }
}

