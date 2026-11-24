import datetime

from django.db import migrations, models


def seed_holds(apps, schema_editor):
    hold = apps.get_model('holds', 'Hold')
    hold.objects.using(schema_editor.connection.alias).create(
        id='H1',
        sequence=1,
        member='bo',
        isbn='9780134685991',
        placed_on=datetime.date(2026, 1, 5),
    )


class Migration(migrations.Migration):
    initial = True

    dependencies = [  # noqa: RUF012
        ('loans', '0001_initial'),
    ]

    operations = [  # noqa: RUF012
        migrations.CreateModel(
            name='Hold',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('sequence', models.PositiveIntegerField(unique=True)),
                ('member', models.CharField(max_length=255)),
                ('isbn', models.CharField(max_length=255)),
                ('placed_on', models.DateField()),
                ('cancelled_on', models.DateField(blank=True, null=True)),
            ],
            options={'ordering': ('sequence',)},
        ),
        migrations.RunPython(seed_holds, migrations.RunPython.noop),
    ]
