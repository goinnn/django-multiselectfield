from django.apps import AppConfig
from django import VERSION
from django.contrib.admin import utils
from django.utils.hashable import make_hashable

from multiselectfield.db.fields import MultiSelectField


class AppAppConfig(AppConfig):
    name = 'app'
    verbose_name = 'app'

    def ready(self):
        if not hasattr(utils, '_original_display_for_field'):
            utils._original_display_for_field = utils.display_for_field
            utils.display_for_field = patched_display_for_field


# Monkey patching for use multiselect field in list_display

def patched_display_for_field(value, field, empty_value_display, avoid_link=False):
    if isinstance(field, MultiSelectField) and getattr(field, "flatchoices", None):
        try:
            flatchoices = dict(field.flatchoices)
            return ', '.join([flatchoices.get(v, empty_value_display) for v in value]) or empty_value_display
        except TypeError:
            # Allow list-like choices.
            flatchoices = dict(make_hashable(field.flatchoices))
            value = make_hashable(value)
            return ', '.join([flatchoices.get(v, empty_value_display) for v in value]) or empty_value_display

    if VERSION < (5, 2):
        return utils._original_display_for_field(value, field, empty_value_display)
    return utils._original_display_for_field(value, field, empty_value_display, avoid_link=avoid_link)
