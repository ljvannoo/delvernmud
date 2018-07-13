#!/usr/bin/env python3

import django
from django.conf import settings
import os



# settings.configure(default_settings=defaults, DEBUG=True)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_settings')
django.setup()

from src.entities.models import PlayerModel

# player = PlayerModel(name="Willis")
# print("Id: " + str(player.id))
# player.save()
# print("Id: " + str(player.id))


all_players = PlayerModel.objects.filter(name="Vylar2")
for player in all_players:
  print("Found: " + player.name)