import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcms.settings')

if __name__ == '__main__' and __package__ is None:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print('BASE_DIR ', BASE_DIR)
    sys.path.append(BASE_DIR)

import django
django.setup()

print('ok')



