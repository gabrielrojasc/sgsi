from __future__ import annotations

from django import forms
from django.forms import Form
from django.forms import HiddenInput
from django.forms import ModelForm

forms.fields.Field.is_checkbox = lambda self: isinstance(
    self.widget,
    forms.CheckboxInput,
)

forms.fields.Field.is_file_input = lambda self: isinstance(self.widget, forms.FileInput)


class BaseFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            attrs = field.widget.attrs
            if "class" not in attrs:
                attrs["class"] = ""

            match field.widget:
                case forms.widgets.DateInput():
                    attrs["class"] += " form-control"
                    field.widget.input_type = "date"
                    field.widget.format = "%Y-%m-%d"

                case forms.widgets.DateTimeInput():
                    attrs["class"] += " form-control"
                    field.widget.input_type = "datetime-local"
                    field.widget.format = "%Y-%m-%d %H:%M:%S"

                case forms.widgets.TimeInput():
                    attrs["class"] += " form-control"
                    field.widget.input_type = "time"
                    field.widget.format = "%H:%M:%S"

                case forms.widgets.FileInput():
                    attrs["class"] += " form-control is-invalid"

                case forms.widgets.CheckboxInput():
                    attrs["class"] += " form-check-input"
                    attrs["role"] = "switch"

                case _:
                    attrs["class"] += " form-control"

    def hide_field(self, field_name):
        self.fields[field_name].widget = HiddenInput()


class BaseForm(BaseFormMixin, Form):
    pass


class BaseModelForm(BaseFormMixin, ModelForm):
    pass
