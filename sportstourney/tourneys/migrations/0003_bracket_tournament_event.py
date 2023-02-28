# Generated by Django 4.0.3 on 2022-10-05 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tourneys', '0002_team_tem_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bracket',
            fields=[
                ('brac_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('brac_roun', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('tourney_id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('eve_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tour_n', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tourneys.tournament')),
            ],
        ),
    ]
