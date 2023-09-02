# Generated by Django 4.1.7 on 2023-04-19 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_no', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=100)),
                ('content', models.TextField()),
                ('author', models.CharField(default='', max_length=50)),
                ('publishing_time', models.DateTimeField(blank=True)),
            ],
        ),
    ]