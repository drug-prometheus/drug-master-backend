# Generated by Django 5.0.6 on 2024-10-14 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicationInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medication_name', models.CharField(max_length=100)),
                ('properties_classification', models.CharField(max_length=100)),
                ('medical_properties', models.TextField()),
                ('usage_capacity', models.TextField()),
                ('side_effects', models.TextField()),
                ('prohibition', models.TextField()),
                ('medication_guide', models.TextField()),
            ],
        ),
    ]
