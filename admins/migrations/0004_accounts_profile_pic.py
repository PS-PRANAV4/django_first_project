# Generated by Django 4.0.4 on 2022-06-12 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0003_alter_accounts_is_superadmin'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='profile_pic',
            field=models.ImageField(blank=True, max_length=300, upload_to='photos/profile_pic'),
        ),
    ]
