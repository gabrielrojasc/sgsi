import uuid

from contextlib import nullcontext as does_not_raise
from datetime import datetime
from datetime import time
from datetime import timedelta
from decimal import Decimal
from unittest.mock import MagicMock
from unittest.mock import patch

from django.core.files.uploadedfile import UploadedFile
from django.db.models.fields.files import FieldFile
from django.utils.functional import Promise

import pytest

from base.models import BaseModel
from base.serializers import ModelEncoder
from base.serializers import StringFallbackJSONEncoder


@pytest.mark.parametrize(
    ("spec", "expected"),
    (
        (FieldFile, "url"),
        (UploadedFile, "<Unsaved file: name>"),
        (BaseModel, "to_dict"),
        (Decimal, "str"),
        (Promise, "force_str"),
        (None, "default"),
    ),
)
def test_model_encoder(spec, expected):
    with (
        patch("base.serializers.force_str", return_value="force_str"),
        patch(
            "django.core.serializers.json.DjangoJSONEncoder.default",
            return_value="default",
        ),
    ):
        obj = MagicMock(spec=spec)
        obj.url = "url"
        obj.name = "name"
        obj.__str__.return_value = "str"
        obj.to_dict = MagicMock(return_value="to_dict")
        assert ModelEncoder().default(obj) == expected


@pytest.mark.parametrize(
    ("obj", "patch_str"),
    (
        (
            datetime.fromisoformat("2023-07-12T15:30:45.123456+03:00"),
            "base.serializers.StringFallbackJSONEncoder.process_datetime",
        ),
        (
            datetime.fromisoformat("2023-07-12T15:30:45.123456").date(),
            "base.serializers.StringFallbackJSONEncoder.process_date",
        ),
        (
            datetime.fromisoformat("2023-07-12T15:30:45.123456").time(),
            "base.serializers.StringFallbackJSONEncoder.process_time",
        ),
        (
            timedelta(days=1),
            "base.serializers.StringFallbackJSONEncoder.process_timedelta",
        ),
        (
            Decimal("1.1"),
            "base.serializers.StringFallbackJSONEncoder.process_decimal_uuid_or_promise",
        ),
        (
            uuid.uuid4(),
            "base.serializers.StringFallbackJSONEncoder.process_decimal_uuid_or_promise",
        ),
        (
            Promise(),
            "base.serializers.StringFallbackJSONEncoder.process_decimal_uuid_or_promise",
        ),
    ),
)
def test_string_fall_back_json_encoder_default(obj, patch_str):
    with patch(patch_str) as mock:
        StringFallbackJSONEncoder().default(obj)
        mock.assert_called_once_with(obj)


@pytest.mark.parametrize(
    ("obj", "expected"),
    (
        ({"a": 1}, {"a": 1}),
        (b"\x80\x81\x82", "default"),
    ),
)
def test_string_fall_back_json_encoder_process_other(obj, expected):
    with patch(
        "base.serializers.JSONEncoder.default",
        return_value="default",
    ):
        assert StringFallbackJSONEncoder().process_other(obj) == expected


@pytest.mark.parametrize(
    ("obj", "expected"),
    (
        (Decimal("1.1"), "1.1"),
        (Decimal("1"), "1"),
    ),
)
def test_string_fall_back_json_encoder_process_decimal_uuid_or_promise(obj, expected):
    assert StringFallbackJSONEncoder().process_decimal_uuid_or_promise(obj) == expected


def test_string_fall_back_json_encoder_process_timedelta():
    obj = timedelta(days=1)
    assert StringFallbackJSONEncoder().process_timedelta(obj) == "P1DT00H00M00S"


@pytest.mark.parametrize(
    ("obj", "expected", "expectation"),
    (
        (
            time.fromisoformat("15:30:45.123456+03:00"),
            None,
            pytest.raises(ValueError),
        ),
        (
            time.fromisoformat("15:30:45.123456"),
            "15:30:45.123",
            does_not_raise(),
        ),
        (
            time.fromisoformat("15:30:45"),
            "15:30:45.000",
            does_not_raise(),
        ),
    ),
    ids=(
        "time-micros-with-tz",
        "time-micros-without-tz",
        "time-secs-without-tz",
    ),
)
def test_string_fall_back_json_encoder_process_time(obj, expected, expectation):
    with expectation:
        assert StringFallbackJSONEncoder().process_time(obj) == expected


def test_string_fall_back_json_encoder_process_date():
    obj = datetime.fromisoformat("2023-07-12T15:30:45.123456")
    expected = "2023-07-12T15:30:45.123456"
    assert StringFallbackJSONEncoder().process_date(obj) == expected


@pytest.mark.parametrize(
    ("obj", "expected"),
    (
        (
            datetime.fromisoformat("2023-07-12T15:30:45.123456"),
            "2023-07-12T15:30:45.123",
        ),
        (
            datetime.fromisoformat("2023-07-12T15:30:45.123456+00:00"),
            "2023-07-12T15:30:45.123+00:00",
        ),
    ),
)
def test_string_fall_back_json_encoder_process_datetime(obj, expected):
    assert StringFallbackJSONEncoder().process_datetime(obj) == expected
