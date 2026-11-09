# THROWAWAY UI prototype for issue martins-vds/ai-factory-synthetic-target#50.
# Three radically different loans, late-fee, and About screens on one route.
# Run: ENABLE_UI_PROTOTYPE=1 python manage.py runserver 127.0.0.1:8000
# Open: http://127.0.0.1:8000/prototype/library/ (variants: reading-room, desk, ledger)

from datetime import date, timedelta

from django.shortcuts import render


VARIANTS = [
    {'key': 'reading-room', 'name': 'Reading Room — editorial'},
    {'key': 'desk', 'name': 'Circulation Desk — command center'},
    {'key': 'ledger', 'name': 'Pocket Ledger — high contrast'},
]

today = date.today()
LOANS = [
    {
        'id': 'L102',
        'member': 'Avery Chen',
        'isbn': '9780375703867',
        'title': 'The City & the City',
        'due': today - timedelta(days=1),
        'returned_on': None,
    },
    {
        'id': 'L103',
        'member': 'Rafael Ortiz',
        'isbn': '9781571313560',
        'title': 'Braiding Sweetgrass',
        'due': today - timedelta(days=12),
        'returned_on': None,
    },
    {
        'id': 'L104',
        'member': 'Morgan Bell',
        'isbn': '9780374275631',
        'title': 'The Overstory',
        'due': today - timedelta(days=7),
        'returned_on': today - timedelta(days=4),
    },
    {
        'id': 'L105',
        'member': 'Priya Nair',
        'isbn': '9780374533557',
        'title': 'Piranesi',
        'due': today + timedelta(days=7),
        'returned_on': None,
    },
    {
        'id': 'L106',
        'member': 'D. Kim',
        'isbn': '9780441007318',
        'title': 'The Left Hand of Darkness',
        'due': today - timedelta(days=60),
        'returned_on': today - timedelta(days=10),
    },
]
NEXT_LOAN_NUMBER = 107


def late_fee(loan):
    end_date = loan['returned_on'] or today
    late_days = max(0, (end_date - loan['due']).days)
    cents = min(max(late_days - 2, 0) * 25, 1000)
    return {
        'loan': loan,
        'late_days': late_days,
        'amount': f'${cents / 100:.2f}',
    }


def prototype_library(request):
    global NEXT_LOAN_NUMBER

    variant = request.GET.get('variant', VARIANTS[0]['key'])
    if variant not in {item['key'] for item in VARIANTS}:
        variant = VARIANTS[0]['key']
    screen = request.GET.get('screen', 'loans')
    if screen not in {'loans', 'fees', 'about'}:
        screen = 'loans'

    errors = {}
    form_values = {'member': '', 'isbn': ''}
    feedback = ''

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'lend':
            form_values = {
                'member': request.POST.get('member', ''),
                'isbn': request.POST.get('isbn', ''),
            }
            member = form_values['member'].strip()
            isbn = form_values['isbn'].strip()
            if not member:
                errors['member'] = 'Enter a member name; blank values are not accepted.'
            if not isbn:
                errors['isbn'] = 'Enter an ISBN; blank values are not accepted.'
            if not errors:
                LOANS.append({
                    'id': f'L{NEXT_LOAN_NUMBER}',
                    'member': member,
                    'isbn': isbn,
                    'title': 'Newly loaned book',
                    'due': today + timedelta(days=14),
                    'returned_on': None,
                })
                feedback = f'Loan L{NEXT_LOAN_NUMBER} added to this server’s in-memory sample.'
                NEXT_LOAN_NUMBER += 1
        elif action == 'return':
            loan = next((item for item in LOANS if item['id'] == request.POST.get('loan_id')), None)
            if loan is None:
                feedback = 'No such loan.'
            elif loan['returned_on']:
                feedback = (
                    f'{loan["id"]} was already returned on {loan["returned_on"]}; '
                    'repeat return rejected and original date retained.'
                )
            else:
                loan['returned_on'] = today
                feedback = f'{loan["id"]} marked returned today.'
        screen = 'loans'

    fees = [late_fee(loan) for loan in LOANS]
    loan_id = request.GET.get('loan', '')
    selected_fee = next((fee for fee in fees if fee['loan']['id'] == loan_id), None)
    if selected_fee is None:
        selected_fee = next((fee for fee in fees if fee['amount'] != '$0.00'), fees[0])

    return render(request, 'prototype_library.html', {
        'variant': variant,
        'variants': VARIANTS,
        'screen': screen,
        'loans': LOANS,
        'fees': fees,
        'selected_fee': selected_fee,
        'errors': errors,
        'form_values': form_values,
        'feedback': feedback,
        'loan_count': len(LOANS),
        'overdue_count': sum(fee['late_days'] > 0 and not fee['loan']['returned_on'] for fee in fees),
    })
