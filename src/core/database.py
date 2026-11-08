from django.db import connection


def database_probe() -> int:
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
        return cursor.fetchone()[0]
