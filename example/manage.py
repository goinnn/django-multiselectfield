#!/usr/bin/env python
import os
import sys

from django.conf import ENVIRONMENT_VARIABLE

if __name__ == "__main__":
    os.environ.setdefault(ENVIRONMENT_VARIABLE, "example.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
