from typing import Any

from django import forms
from django.utils.translation import gettext_lazy as _

from base.forms import BaseForm
from base.forms import BaseModelForm
from documents.models.control import Control
from documents.models.control_category import ControlCategory
from documents.models.document import Document
from documents.models.document_type import DocumentType
from documents.models.document_version import DocumentVersion


class DocumentForm(BaseModelForm):
    class Meta:
        model = Document
        fields = (
            "title",
            "code",
            "document_type",
            "description",
            "drive_folder",
            "documented_controls",
        )


class DocumentVersionForm(BaseModelForm):
    class Meta:
        model = DocumentVersion
        fields = ("author", "file", "file_url", "comment")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["author"].label_from_instance = lambda obj: obj.get_label()

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        self.check_only_one_file(cleaned_data)
        return cleaned_data

    def check_only_one_file(self, cleaned_data: dict[str, Any]) -> None:
        file = cleaned_data.get("file")
        file_url = cleaned_data.get("file_url")
        if bool(file) ^ bool(file_url):
            return
        msg = _("You must provide either a file or a URL.")
        self.add_error(None, msg)


class ControlForm(BaseModelForm):
    class Meta:
        model = Control
        fields = ("category", "title", "description")


class ControlCategoryForm(BaseModelForm):
    class Meta:
        model = ControlCategory
        fields = ("name",)


class EvidenceForm(BaseForm):
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
    evidence_text = forms.CharField(
        label=_("Evidence text"),
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text=_("Text as evidence of the activity completion."),
    )

    class Meta:
        fields = ("evidence_file", "evidence_url", "evidence_text")

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        self.check_only_one_evidence(cleaned_data)
        return cleaned_data

    def check_only_one_evidence(self, cleaned_data: dict[str, Any]) -> None:
        evidence_file = cleaned_data.get("evidence_file")
        evidence_url = cleaned_data.get("evidence_url")
        evidence_text = cleaned_data.get("evidence_text")
        if evidence_url and not evidence_file and not evidence_text:
            return
        if not evidence_url and evidence_file and not evidence_text:
            return
        if not evidence_url and not evidence_file and evidence_text:
            return
        msg = _("You must provide either a file, a URL or text as evidence.")
        self.add_error(None, msg)


class DocumentVersionApproveForm(EvidenceForm, BaseModelForm):
    class Meta:
        model = DocumentVersion
        fields = ("approved_by", "evidence_file", "evidence_url", "evidence_text")


class DocumentTypeForm(BaseModelForm):
    class Meta:
        model = DocumentType
        fields = ("name",)
