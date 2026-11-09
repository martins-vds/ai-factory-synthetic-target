from datetime import date

import pytest
from django.db import IntegrityError

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


@pytest.mark.django_db(transaction=True)
def test_updated_catalog_record_survives_database_connection_restart(client):
    loan = Loan.objects.get(pk='L1')
    loan.member = 'ada'
    loan.save(update_fields=['member'])
    from django.db import connection

    connection.close()

    response = client.get('/loans/L1')

    assert response.status_code == 200
    assert response.content.decode() == 'L1;ada;9780134685991;2026-01-02;2026-01-16;\n'


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


@pytest.mark.django_db(transaction=True)
def test_repository_write_rolls_back_failed_transaction():
    with pytest.raises(IntegrityError):
        LoanRepository.create(
            id='L1',
            member='duplicate',
            isbn='123',
            lent_on=date(2026, 3, 1),
        )

    assert Loan.objects.get(pk='L1').member == 'ana'
