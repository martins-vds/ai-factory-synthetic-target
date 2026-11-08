import pytest
from django.db import connection


@pytest.mark.django_db
def test_postgresql_connection_executes_query():
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        assert cursor.fetchone() == (1,)
