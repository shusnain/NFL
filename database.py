import cPickle
# import nflgame
import re
from collections import OrderedDict

beginYear = 2010
endYear = 2015

def saveDB(fname, db):
	f = open(fname, 'wb')
	cPickle.dump(db, f, protocol=cPickle.HIGHEST_PROTOCOL)
	f.close()

def create_stats_db():
	player_stats_db = OrderedDict()
	for year in range(beginYear, endYear + 1):
		for i in range(1, 18):
			games = nflgame.games(year, week=i)
			players = nflgame.combine_game_stats(games)
			for p in players:
				player = [val for val in re.split('[\s(),]', str(p.player)) if val != '']
				first_name, last_name = player[0], player[1]
				if len(player) > 2:
					position = player[2]
				else:
					position = 'NA'

				player_name = first_name + ' ' + last_name
				if player_name not in player_stats_db:
					player_stats_db[player_name] = OrderedDict()
				if year not in player_stats_db[player_name]:
					player_stats_db[player_name][year] = OrderedDict()
				player_stats_db[player_name][year][i] = {p_s: p.stats[p_s] for p_s in p.stats}
			OrderedDict(sorted(player_stats_db[player_name][year].items(), key=lambda t: t[0]))
	return player_stats_db

def create_player_db():
	players_db = {}
	players = nflgame.players
	for p in players:
		player = players[p]
		fullname = player.first_name + ' ' + player.last_name
		if fullname not in players_db:
			players_db[fullname] = {}
		players_db[fullname]['birthdate'] = player.birthdate
		players_db[fullname]['position'] = player.position
	return players_db

def loadDB(fname):
    f = open(fname, 'rb')
    db = cPickle.load(f)
    f.close()
    return db

# player_stats_db = create_stats_db()
# saveDB('nfldb', player_stats_db)
# players_db = create_player_db()
# saveDB('playersdb', players_db)
