import os
import sys

from django.conf import settings

from aviana.models import User
from config.settings import BASE_DIR


def demo():
    print(os.getcwd())
    print(sys.version)
    print(settings.DEBUG)
    print(BASE_DIR)
    print(User)
