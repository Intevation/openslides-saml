import os
from django.core.management.base import BaseCommand, CommandError
from openslides.utils.main import (
    get_default_settings_dir,
    get_local_settings_dir,
    is_local_installation,
)
from ...settings import create_saml_settings

class Command(BaseCommand):
    """
    Command to create the saml_settings.json file.
    """
    help = 'Create the saml_settings.json settings file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-d', '--dir',
            default=None,
            help='Directory for the saml_settings.json file.'
        )

    def handle(self, *args, **options):
        settings_dir = options.get('path')

        if settings_dir is None:
            if is_local_installation():
                settings_dir = get_local_settings_dir()
            else:
                settings_dir = get_default_settings_dir()

        settings_path = os.path.join(settings_dir, 'saml_settings.json')
        create_saml_settings(settings_path)
        print("Created SAML settings at: {}".format(settings_path))
