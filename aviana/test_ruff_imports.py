import os
import sys

from django.conf import settings

from aviana.models import User


def demo():
    print(os.getcwd())
    print(sys.version)
    print(settings.DEBUG)
    print(User)
