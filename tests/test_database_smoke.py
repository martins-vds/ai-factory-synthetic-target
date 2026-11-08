import pytest

from src.core.database import database_probe


@pytest.mark.django_db
def test_postgresql_connection_executes_query():
    assert database_probe() == 1
