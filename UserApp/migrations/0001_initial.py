# Generated by Django 5.2.3 on 2025-06-23 10:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coreApp', '0003_delete_userprogress'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coreApp.topic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Progress',
                'unique_together': {('user', 'topic')},
            },
        ),
    ]
