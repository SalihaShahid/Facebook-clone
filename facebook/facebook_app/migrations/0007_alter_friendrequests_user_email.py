# Generated by Django 4.2.3 on 2023-07-24 10:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("facebook_app", "0006_alter_friendrequests_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="friendrequests",
            name="user_email",
            field=models.EmailField(max_length=254),
        ),
    ]
