from datetime import date

from django.db import migrations, models


def seed_loans(apps, schema_editor):
    loan = apps.get_model('loans', 'Loan')
    loan.objects.using(schema_editor.connection.alias).bulk_create(
        [
            loan(
                id='L1',
                member='ana',
                isbn='9780134685991',
                lent_on=date(2026, 1, 2),
            ),
            loan(
                id='L2',
                member='bo',
                isbn='9780596007126',
                lent_on=date(2026, 1, 10),
                returned_on=date(2026, 1, 20),
            ),
            loan(
                id='L3',
                member='cy',
                isbn='9781617294945',
                lent_on=date(2025, 12, 1),
                returned_on=date(2026, 1, 3),
            ),
        ]
    )


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('member', models.CharField(blank=True, max_length=255)),
                ('isbn', models.CharField(blank=True, max_length=64)),
                ('lent_on', models.DateField()),
                ('returned_on', models.DateField(blank=True, null=True)),
            ],
            options={'ordering': ('id',)},
        ),
        migrations.RunPython(seed_loans, migrations.RunPython.noop),
    ]
