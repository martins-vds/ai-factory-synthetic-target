"""Project-wide test isolation (AFS harness: target.shared_test_files).

Each database test restores the rows that migrations seeded, so a test
that flushes the database (live-server and browser tests do) can't leave
the next test without its seed data.

pytest-django saves the database contents at setup only for tests whose
django_db marker asks for serialized_rollback; the fixture below is
ignored there for marked tests. The hook makes every marker ask, so the
contents are always saved, whatever tests are collected.
"""

import pytest


def pytest_collection_modifyitems(items):
    for item in items:
        marker = item.get_closest_marker('django_db')
        if marker is not None and not marker.kwargs.get('serialized_rollback'):
            kwargs = {**marker.kwargs, 'serialized_rollback': True}
            # In front: get_closest_marker returns the first of the item's own markers.
            item.add_marker(pytest.mark.django_db(*marker.args, **kwargs), append=False)


@pytest.fixture(autouse=True)
def django_db_serialized_rollback():
    return True
