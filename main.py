import json
import os
from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
application = get_wsgi_application()

from db.models import Race, Skill, Guild, Player

def main():
    with open('players.json', 'r') as f:
        players_data = json.load(f)

    for player_data in players_data:
        race_name = player_data['race']
        guild_name = player_data.get('guild')

        race, _ = Race.objects.get_or_create(name=race_name)

        guild = None
        if guild_name:
            guild, _ = Guild.objects.get_or_create(name=guild_name)

        player, _ = Player.objects.get_or_create(
            nickname=player_data['nickname'],
            defaults={
                'email': player_data['email'],
                'bio': player_data['bio'],
                'race': race,
                'guild': guild,
            }
        )

        for skill_name in player_data.get('skills', []):
            Skill.objects.get_or_create(name=skill_name, race=race, defaults={'bonus': 'Опис бонусу для ' + skill_name})

    print("Дані гравців успішно додано до бази даних.")

if __name__ == "__main__":
    main()
