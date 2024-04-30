from typing import Any

from django import forms
from django.utils.translation import gettext_lazy as _

from base.forms import BaseModelForm
from processes.models.process import Process
from processes.models.process_activity import ProcessActivity
from processes.models.process_activity_instance import ProcessActivityInstance
from processes.models.process_instance import ProcessInstance
from processes.models.process_version import ProcessVersion
from users.models import User


class ProcessForm(BaseModelForm):
    class Meta:
        model = Process
        fields = ("name",)


class ProcessVersionForm(BaseModelForm):
    class Meta:
        model = ProcessVersion
        fields = (
            "defined_in",
            "controls",
            "recurrency",
        )


class ProcessActivityForm(BaseModelForm):
    class Meta:
        model = ProcessActivity
        fields = ("description", "asignee_group")


class ProcessInstanceForm(BaseModelForm):
    process = forms.ModelChoiceField(
        label=_("Process"),
        queryset=Process.objects.all(),
        required=True,
    )

    class Meta:
        model = ProcessInstance
        fields = ("process",)

    def __init__(self, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["process"].queryset = user.get_instantiable_processes()
        self.user = user

    def save(self, commit: bool = True) -> ProcessInstance:
        self.instance.process_version = self.cleaned_data.get(
            "process"
        ).last_published_version
        return super().save(commit)


class ProcessActivityInstanceCompleteForm(BaseModelForm):
    evidence_file = forms.FileField(
        label=_("Evidence file"),
        required=False,
        help_text=_("File with the evidence of the activity completion."),
    )
    evidence_url = forms.URLField(
        label=_("Evidence URL"),
        required=False,
        help_text=_("URL to the evidence of the activity completion."),
    )

    class Meta:
        model = ProcessActivityInstance
        fields = ("evidence_file", "evidence_url")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        next_activity = self.instance.get_next_activity()
        if next_activity is not None:
            self.add_next_activity_fields(next_activity)

    def add_next_activity_fields(self, next_activity: ProcessActivity):
        users_qs = next_activity.asignee_group.user_set.all()
        self.fields["next_activity_asignee"] = forms.ModelChoiceField(
            label=_("Next activity asignee"),
            queryset=users_qs,
            required=True,
            help_text=_(
                "Next activity: {next_activity_description}, asignee group: "
                "{next_activity_asginee_group}."
            ).format(
                next_activity_description=next_activity.description,
                next_activity_asginee_group=next_activity.asignee_group,
            ),
        )
        if users_qs.count() == 1:
            self.fields["next_activity_asignee"].initial = users_qs.first()

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        self.evidence_file_xor_url(cleaned_data)
        return cleaned_data

    def evidence_file_xor_url(self, cleaned_data):
        evidence_file = cleaned_data.get("evidence_file")
        evidence_url = cleaned_data.get("evidence_url")
        if bool(evidence_file) ^ bool(evidence_url):
            return
        msg = _("You must provide either a file or a URL as evidence.")
        self.add_error(None, msg)
