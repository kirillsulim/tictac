# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('state', models.CharField(choices=[('XP', 'X pending'), ('OP', 'O pending'), ('XW', 'X won'), ('OW', 'O won')], default='XP', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('order', models.IntegerField()),
                ('code', models.CharField(choices=[('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3'), ('C1', 'C1'), ('C2', 'C2'), ('C3', 'C3')], max_length=2)),
                ('for_game', models.ForeignKey(to='game.Game')),
                ('player', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='moves',
            field=models.ManyToManyField(to='game.Move'),
        ),
        migrations.AddField(
            model_name='game',
            name='o_player',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='o_player'),
        ),
        migrations.AddField(
            model_name='game',
            name='x_player',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='x_player'),
        ),
    ]
