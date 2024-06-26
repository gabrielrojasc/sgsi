import pytest

from information_assets.enums import ClassificationChoices
from information_assets.enums import CriticalityChoices
from information_assets.models.asset import Asset
from information_assets.models.asset_role import AssetRole
from information_assets.models.asset_role_user import AssetRoleUser
from information_assets.models.asset_type import AssetType


@pytest.fixture
@pytest.mark.django_db
def asset_type():
    return AssetType.objects.create(
        name="test asset type", description="test description"
    )


@pytest.fixture
@pytest.mark.django_db
def asset(regular_user, asset_type):
    asset = Asset.objects.create(
        owner=regular_user,
        name="test asset",
        description="test description",
        criticality=CriticalityChoices.MEDIUM,
        classification=ClassificationChoices.INTERNAL,
    )
    asset.asset_types.set((asset_type,))
    return asset


@pytest.fixture
@pytest.mark.django_db
def asset_role(asset):
    return AssetRole.objects.create(asset=asset, name="test asset role")


@pytest.fixture
@pytest.mark.django_db
def asset_role_user(asset_role, regular_user):
    return AssetRoleUser.objects.create(role=asset_role, user=regular_user)
