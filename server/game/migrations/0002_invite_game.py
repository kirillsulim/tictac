# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invite',
            name='game',
            field=models.ForeignKey(null=True, blank=True, to='game.Game'),
        ),
    ]
