import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def init_django():
    if settings.configured:
        return
    
    settings.configure(
        INSTALLED_APPS=[
            'db',
        ],
        DATABASES={
            'default':{
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }
    )
    django.setup()

if __name__ =="__main__":
    init_django()
    execute_from_command_line()