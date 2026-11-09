import importlib

import pytest
from django.apps import apps
from django.db import connection


@pytest.fixture(scope='module')
def restore_seed_loans(django_db_blocker):
    yield
    with django_db_blocker.unblock():
        apps.get_model('loans', 'Loan').objects.all().delete()
        seed_loans = importlib.import_module('src.loans.migrations.0001_initial').seed_loans
        with connection.schema_editor() as schema_editor:
            seed_loans(apps, schema_editor)
