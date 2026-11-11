import pytest


@pytest.fixture(autouse=True)
def django_db_serialized_rollback():
    return True
