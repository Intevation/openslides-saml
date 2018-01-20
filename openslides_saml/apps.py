import os

from django.apps import AppConfig

from . import (
    __description__,
    __license__,
    __url__,
    __verbose_name__,
    __version__,
)
from .exceptions import SamlException


class SamlAppConfig(AppConfig):
    name = 'openslides_saml'
    verbose_name = __verbose_name__
    description = __description__
    version = __version__
    license = __license__
    url = __url__
    angular_site_module = True
    js_files = [
        'static/js/openslides_saml/base.js',
        'static/js/openslides_saml/site.js',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            import onelogin.saml2  # noqa
        except ImportError:
            raise SamlException("Could not import onelogin.saml2. Is python-saml3 installed?")

        try:
            import settings
        except ImportError:
            # When testing, we cannot import settings here..
            pass
        else:
            # Add the staticfiles dir to OpenSlides
            base_path = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
            # remove the app folder 'openslides_saml'
            base_path = os.path.dirname(base_path)
            settings.STATICFILES_DIRS.append(os.path.join(base_path, 'static'))

    def ready(self):
        # Import all required stuff.
        from openslides import args
        from openslides.utils.main import (
            get_default_settings_dir,
            get_local_settings_dir,
            is_local_installation,
        )
        from .urls import urlpatterns
        from .settings import SamlSettings

        settings_dir = None
        if args:
            settings_dir = args.settings_dir

        if settings_dir is None:
            if is_local_installation():
                settings_dir = get_local_settings_dir()
            else:
                settings_dir = get_default_settings_dir()

        # Instanciate the SamlSettings. Here, the class is loaded the first time
        # and by providing the settings_path the internal state is set to this
        # path.
        SamlSettings(settings_dir)

        # Make the urls available for openslides
        self.urlpatterns = urlpatterns
