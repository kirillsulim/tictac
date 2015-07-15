# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_invite_game'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='state',
            field=models.CharField(default='XP', max_length=2, choices=[('XP', 'X pending'), ('OP', 'O pending'), ('XW', 'X won'), ('OW', 'O won'), ('TT', 'Tie')]),
        ),
    ]
