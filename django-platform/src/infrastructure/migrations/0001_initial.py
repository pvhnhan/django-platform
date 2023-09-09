# Generated by Django 4.1.7 on 2023-09-08 07:58

from django.db import migrations, models
import src.infrastructure.entities.user
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MediaEntity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateField()),
                ('created_by', models.CharField(max_length=50)),
                ('updated_date', models.DateField()),
                ('updated_by', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('name_upload', models.CharField(max_length=200)),
                ('extension', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('path', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'Media',
            },
        ),
        migrations.CreateModel(
            name='UserEntity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateField()),
                ('created_by', models.CharField(max_length=50)),
                ('updated_date', models.DateField()),
                ('updated_by', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=100)),
                ('avatar', models.FileField(upload_to=src.infrastructure.entities.user.user_directory_path)),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]