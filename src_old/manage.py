#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    ENV = "config.settings.development"
    
    from socket import gethostname
    if gethostname() == 'ocean.wolkie.tk':
        ENV = "config.settings.production"
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", ENV)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
