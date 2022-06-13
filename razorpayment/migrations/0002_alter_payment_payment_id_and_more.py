# Generated by Django 4.0.4 on 2022-06-13 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('razorpayment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_signature',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(blank=True, choices=[('ACCEPTED', 'ACCEPTED'), ('FAILED', 'FAILED')], max_length=50),
        ),
    ]
