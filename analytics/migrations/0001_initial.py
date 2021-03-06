# Generated by Django 2.1.1 on 2018-12-13 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('impression_token', models.UUIDField()),
                ('url', models.CharField(max_length=255)),
                ('impression_type', models.CharField(max_length=50)),
                ('session_token', models.UUIDField()),
                ('elapsed_time_in_ms', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitor_token', models.UUIDField()),
                ('event_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('impression_token', models.UUIDField()),
                ('event_name', models.CharField(max_length=255)),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='analytics.Track')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='pageevent',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='analytics.Track'),
        ),
    ]
