import os
import json
from openslides.utils.main import get_default_settings_dir

from .exceptions import SamlException

from onelogin.saml2.settings import OneLogin_Saml2_Settings

README = """\
Take care of this folder that could contain private key. Be sure that this folder never is published.

OpenSlides SAML plugin expects that certs for the SP could be stored in this folder as:

 * sp.key     Private Key
 * sp.crt     Public cert
 * sp_new.crt Future Public cert

Also you can use other cert to sign the metadata of the SP using the:

 * metadata.key
 * metadata.crt"""

def create_saml_settings(settings_path: str, template: str=None, **context: str) -> None:
    """
    Creates the SAML settings file 'saml_settings.json'
    """
    settings_path = os.path.realpath(settings_path)
    if template is None:
        with open(os.path.join(os.path.dirname(__file__), 'saml_settings.json.tpl')) as template_file:
            template = template_file.read()

    content = template % context
    with open(settings_path, 'w') as settings_file:
        settings_file.write(content)

    # create cert folder and add thr README
    cert_dir = os.path.join(os.path.dirname(settings_path), 'certs')
    os.makedirs(cert_dir, exist_ok=True)

    # create README there
    readme_path = os.path.join(cert_dir, 'README')
    if not os.path.isfile(readme_path):
        with open(readme_path, 'w') as readme:
            readme.write(README)
        print("Written README into the certs folder: {}".format(cert_dir))
    print("Created SAML settings at: {}".format(settings_path))

    return settings_path


class SamlSettings():
    state = {}

    def __init__(self, settings_dir=None):
        """
        When provoding the settings_path, the settings are reloaded.
        """
        if settings_dir:
            self.state['settings_dir'] = settings_dir
            self.load_settings()

    def load_settings(self):
        settings_dir = self.state['settings_dir']
        settings_path = os.path.join(settings_dir, 'saml_settings.json')
        if not os.path.isfile(settings_path):
            create_saml_settings(settings_path)

        content = None
        try:
            with open(settings_path, 'r') as settings_file:
                content = json.load(settings_file)
        except IOError:
            raise SamlException(
                "Could not read settings file located at: {}".format(settings_path))
        except json.JSONDecodeError:
            raise SamlException(
                "The settings file located at {} could not be loaded.".format(settings_path))

        settings = OneLogin_Saml2_Settings(content, custom_base_path=settings_dir)
        self.state['settings'] = settings

    @classmethod
    def get(cls):
        return cls().state['settings']
