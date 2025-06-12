from django.apps import AppConfig
from django import VERSION
from django.contrib.admin import utils
from django.contrib.admin.helpers import AdminReadonlyField
from django.contrib.admin.utils import display_for_field, lookup_field
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.related import (
    ForeignObjectRel,
    ManyToManyRel,
    OneToOneField,
)
from django.template.defaultfilters import linebreaksbr
from django.utils.hashable import make_hashable
from django.utils.html import conditional_escape

from multiselectfield.db.fields import MultiSelectField


class AppAppConfig(AppConfig):
    name = 'app'
    verbose_name = 'app'

    def ready(self):
        if not hasattr(utils, '_original_display_for_field'):
            utils._original_display_for_field = utils.display_for_field
            utils.display_for_field = patched_display_for_field
        if not hasattr(AdminReadonlyField, '_original_contents'):
            AdminReadonlyField._original_contents = AdminReadonlyField.contents
            AdminReadonlyField.contents = patched_contents


# Monkey patching for use multiselect field in list_display

def patched_display_for_field(value, field, empty_value_display, avoid_link=False):
    if isinstance(field, MultiSelectField) and getattr(field, "flatchoices", None):
        try:
            flatchoices = dict(field.flatchoices)
            return ', '.join([str(flatchoices.get(v, empty_value_display)) for v in value]) or empty_value_display
        except TypeError:
            # Allow list-like choices.
            flatchoices = dict(make_hashable(field.flatchoices))
            value = make_hashable(value)
            return ', '.join([str(flatchoices.get(v, empty_value_display)) for v in value]) or empty_value_display

    if VERSION < (5, 2):
        return utils._original_display_for_field(value, field, empty_value_display)
    return utils._original_display_for_field(value, field, empty_value_display, avoid_link=avoid_link)


# Monkey patching for use multiselect field like read-only fields

def patched_contents(self):
    from django.contrib.admin.templatetags.admin_list import _boolean_icon

    field, obj, model_admin = (
        self.field["field"],
        self.form.instance,
        self.model_admin,
    )
    try:
        f, attr, value = lookup_field(field, obj, model_admin)
    except (AttributeError, ValueError, ObjectDoesNotExist):
        result_repr = self.empty_value_display
    else:
        if field in self.form.fields:
            widget = self.form[field].field.widget
            # This isn't elegant but suffices for contrib.auth's
            # ReadOnlyPasswordHashWidget.
            if getattr(widget, "read_only", False):
                return widget.render(field, value)
        if f is None:
            if getattr(attr, "boolean", False):
                result_repr = _boolean_icon(value)
            else:
                if hasattr(value, "__html__"):
                    result_repr = value
                else:
                    result_repr = linebreaksbr(value)
        else:
            if isinstance(f.remote_field, ManyToManyRel) and value is not None:
                result_repr = ", ".join(map(str, value.all()))
            elif (
                isinstance(f.remote_field, (ForeignObjectRel, OneToOneField))
                and value is not None  # noqa
            ):
                result_repr = self.get_admin_url(f.remote_field, value)
            # Custom: start
            elif isinstance(f, MultiSelectField):
                if value in f.empty_values:
                    result_repr = self.empty_value_display
                else:
                    result_repr = getattr(obj, f'get_{f.name}_display')()
            # Custom: end
            else:
                result_repr = display_for_field(value, f, self.empty_value_display)
            result_repr = linebreaksbr(result_repr)
    return conditional_escape(result_repr)
