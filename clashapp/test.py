from clashapp.models import db
from clashapp.load_clan_data import PlayerBuilder

adi = PlayerBuilder('#2VLV0JJ9')
adi.create_player_current_entry()
db.session.commit()
