# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('state', models.CharField(max_length=2, default='XP', choices=[('XP', 'X pending'), ('OP', 'O pending'), ('XW', 'X won'), ('OW', 'O won')])),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('order', models.IntegerField()),
                ('code', models.CharField(max_length=2, choices=[('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3'), ('C1', 'C1'), ('C2', 'C2'), ('C3', 'C3')])),
                ('game', models.ForeignKey(to='game.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nickname', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='move',
            name='player',
            field=models.ForeignKey(to='game.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='o_player',
            field=models.ForeignKey(to='game.Player', related_name='o_player'),
        ),
        migrations.AddField(
            model_name='game',
            name='x_player',
            field=models.ForeignKey(to='game.Player', related_name='x_player'),
        ),
    ]
