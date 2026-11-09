from datetime import date

import pytest
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import IntegrityError
from django.utils import timezone

from src.loans.models import Loan
from src.loans.repository import LoanRepository


@pytest.mark.django_db
def test_list_endpoint_returns_seeded_records(client):
    response = client.get('/loans')

    assert response.status_code == 200
    assert response['Content-Type'] == 'text/plain'
    assert response.content.decode() == (
        'L1;ana;9780134685991;2026-01-02;2026-01-16;\n'
        'L2;bo;9780596007126;2026-01-10;2026-01-24;2026-01-20\n'
        'L3;cy;9781617294945;2025-12-01;2025-12-15;2026-01-03\n'
    )


@pytest.mark.django_db
def test_detail_endpoint_returns_one_formatted_loan(client):
    response = client.get('/loans/L1')

    assert response.status_code == 200
    assert response['Content-Type'] == 'text/plain'
    assert response.content.decode() == 'L1;ana;9780134685991;2026-01-02;2026-01-16;\n'


@pytest.mark.django_db
def test_detail_endpoint_returns_not_found_for_unknown_loan(client):
    response = client.get('/loans/unknown')

    assert response.status_code == 404
    assert response['Content-Type'] == 'text/plain'
    assert response.content.decode() == 'no such loan\n'


@pytest.mark.django_db
def test_lend_endpoint_creates_a_loan_with_fourteen_day_due_date(client):
    lent_on = timezone.localdate()
    due_on = lent_on + date.resolution * 14

    response = client.post('/loans', {'member': 'dee', 'isbn': '123'})

    assert response.status_code == 201
    assert response['Content-Type'] == 'text/plain'
    assert response.content.decode() == (
        f'L4;dee;123;{lent_on.isoformat()};{due_on.isoformat()};\n'
    )
    loan = Loan.objects.get(pk='L4')
    assert loan.member == 'dee'
    assert loan.isbn == '123'
    assert loan.lent_on == lent_on
    assert loan.due_on == due_on


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('payload', 'field'),
    [
        ({}, 'member'),
        ({'member': 'dee'}, 'isbn'),
        ({'member': ' ', 'isbn': '123'}, 'member'),
        ({'member': 'dee', 'isbn': ' '}, 'isbn'),
    ],
)
def test_lend_endpoint_rejects_missing_or_blank_fields(client, payload, field):
    response = client.post('/loans', payload)

    assert response.status_code == 400
    assert field.encode() in response.content
    assert Loan.objects.count() == 3


@pytest.mark.django_db
def test_return_endpoint_records_the_return_date(client):
    returned_on = timezone.localdate()

    response = client.post('/loans/L1/return')

    assert response.status_code == 200
    assert response['Content-Type'] == 'text/plain'
    assert response.content.decode() == (
        f'L1;ana;9780134685991;2026-01-02;2026-01-16;{returned_on.isoformat()}\n'
    )
    assert Loan.objects.get(pk='L1').returned_on == returned_on


@pytest.mark.django_db
def test_return_endpoint_rejects_repeated_return_without_replacing_date(client):
    original_return_date = date(2026, 1, 20)

    response = client.post('/loans/L2/return')

    assert response.status_code == 409
    assert response.content.decode() == 'already returned\n'
    assert Loan.objects.get(pk='L2').returned_on == original_return_date


@pytest.mark.django_db
def test_return_endpoint_returns_not_found_for_unknown_loan(client):
    response = client.post('/loans/unknown/return')

    assert response.status_code == 404
    assert response['Content-Type'] == 'text/plain'
    assert response.content.decode() == 'no such loan\n'


@pytest.mark.django_db
def test_saved_catalog_record_is_available_to_a_later_request(client):
    Loan.objects.create(
        id='L8',
        member='reader',
        isbn='123',
        lent_on=date(2026, 3, 1),
    )

    response = client.get('/loans/L8')

    assert response.status_code == 200
    assert response.content.decode() == 'L8;reader;123;2026-03-01;2026-03-15;\n'


@pytest.mark.django_db
def test_migration_startup_does_not_replace_persisted_records():
    loan = Loan.objects.get(pk='L1')
    loan.member = 'ada'
    loan.save(update_fields=['member'])

    call_command('migrate', interactive=False, verbosity=0)

    assert Loan.objects.get(pk='L1').member == 'ada'


@pytest.mark.django_db
def test_due_date_is_fourteen_calendar_days_after_lending():
    loan = Loan(
        id='L9',
        member='reader',
        isbn='123',
        lent_on=date(2024, 2, 15),
    )

    assert loan.due_on == date(2024, 2, 29)


@pytest.mark.django_db
def test_detail_export_quotes_delimiters_quotes_and_line_breaks(client):
    Loan.objects.create(
        id='L9',
        member='Reader; Example\nSecond line',
        isbn='978"xyz',
        lent_on=date(2026, 3, 1),
    )

    response = client.get('/loans/L9')

    assert response.status_code == 200
    assert response.content.decode() == (
        'L9;"Reader; Example\nSecond line";"978""xyz";2026-03-01;2026-03-15;\n'
    )


@pytest.mark.django_db
def test_model_enforces_required_fields_and_source_string_limits():
    with pytest.raises(ValidationError) as missing_fields:
        Loan(id='L9', member='', isbn='', lent_on=date(2026, 3, 1)).full_clean()

    assert set(missing_fields.value.message_dict) == {'member', 'isbn'}

    valid_maximum = Loan(
        id='I' * 255,
        member='M' * 255,
        isbn='B' * 255,
        lent_on=date(2026, 3, 1),
    )
    valid_maximum.full_clean()
    assert valid_maximum.due_on == date(2026, 3, 15)

    for field in ('id', 'member', 'isbn'):
        values = {'id': 'L9', 'member': 'reader', 'isbn': '123'}
        values[field] = 'x' * 256
        loan = Loan(**values, lent_on=date(2026, 3, 1))
        with pytest.raises(ValidationError) as long_field:
            loan.full_clean()
        assert field in long_field.value.message_dict


@pytest.mark.django_db
def test_unreturned_loan_is_valid():
    loan = Loan(id='L9', member='reader', isbn='123', lent_on=date(2026, 3, 1))

    loan.full_clean()
    returned_on = Loan._meta.get_field('returned_on')
    assert loan.returned_on is None
    assert loan.due_on == date(2026, 3, 15)
    assert returned_on.null
    assert returned_on.blank


@pytest.mark.django_db
def test_list_endpoint_orders_all_records_by_id(client):
    Loan.objects.create(
        id='L10',
        member='reader',
        isbn='123',
        lent_on=date(2026, 3, 1),
    )
    Loan.objects.create(
        id='L0',
        member='reader',
        isbn='456',
        lent_on=date(2026, 3, 1),
    )

    response = client.get('/loans')

    assert response.status_code == 200
    assert [line.split(';', 1)[0] for line in response.content.decode().splitlines()] == [
        'L0',
        'L1',
        'L10',
        'L2',
        'L3',
    ]


@pytest.mark.django_db
def test_browser_detail_page_shows_loan_dates(client):
    response = client.get('/ui/loans/L1/')

    assert response.status_code == 200
    assert b'Loan record \xc2\xb7 L1' in response.content
    assert b'Jan 2, 2026' in response.content
    assert b'Jan 16, 2026' in response.content


@pytest.mark.django_db
def test_repository_write_rolls_back_failed_transaction():
    with pytest.raises(IntegrityError):
        LoanRepository().create(
            id='L1',
            member='duplicate',
            isbn='123',
            lent_on=date(2026, 3, 1),
        )

    assert Loan.objects.get(pk='L1').member == 'ana'
