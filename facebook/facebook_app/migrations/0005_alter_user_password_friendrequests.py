# Generated by Django 4.2.3 on 2023-07-24 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("facebook_app", "0004_user_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.TextField(),
        ),
        migrations.CreateModel(
            name="FriendRequests",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("friend_email", models.EmailField(max_length=254)),
                ("approval_status", models.BooleanField(default=False)),
                (
                    "user_email",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="facebook_app.user",
                    ),
                ),
            ],
        ),
    ]