class League:
	def __init__(self):
		self.fantasy_scoring = {'receiving_yds': 0.1, 'receiving_tds': 6, 'receiving_rec': 0.5, 'passing_yds': 0.04, 'passing_cmp': 0.25, 'passing_inc': -0.25, 'passing_tds': 6, 'rushing_yds': 0.1, 'rushing_tds': 6, 'fumbles_lost': -2, 'passing_ints': -3, 'twoptm': 2, 'puntret_tds': 6, 'kickret_tds': 6}
		self.league_type = 'standard'
		self.ppr = self.fantasy_scoring['receiving_rec']
		self.positions = {'QB': 1, 'RB': 2, 'WR': 3, 'TE': 1, 'Flex': 1, 'K': 1, 'DST': 1, 'Bench': 5}
		self.teams = 10