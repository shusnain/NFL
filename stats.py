import numpy as np
from collections import OrderedDict
import database as nfldatabase
from math import log10, floor
import nfl_graphs
import league
from datetime import datetime


sig_fig = 2
thisYear = 2016

def get_player_advanced_stats(player_name):
	player_stats = {}
	for year in range(nfldatabase.beginYear, nfldatabase.endYear + 1):
		player = get_player_stats(player_name, year)
		if player:
			fantasy_pts = player_fantasy_points(player)
			# multi_receiving_tds = len([i for i in receiving_tds if i > 1])
			
			# total_receiving_yds = sum(receiving_yds)
			# total_receiving_tds = sum(receiving_tds)
			# total_receiving_rec = sum(receiving_rec)
			# print total_receiving_yds, total_receiving_rec, total_receiving_tds
			# rec_per_td = float(total_receiving_rec)/float(total_receiving_tds)
			# yards_per_rec = float(total_receiving_yds)/float(total_receiving_rec)
			
			# print rec_per_td, yards_per_rec

			total, minimum, maximum, average, std, percentile_25, percentile_75, percentile_5, percentile_95, games_played = get_stats(fantasy_pts)
			player_stats[year] = {'total': total, 'minimum': minimum, 'maximum': maximum, 'average': average, 'std': std, 'percentile_25': percentile_25, 'percentile_75': percentile_75, 'percentile_5': percentile_5, 'percentile_95': percentile_95, 'games_played': games_played}
			# describe(fantasy_pts)
		else:
			player_stats[year] = {'total': 0.0, 'minimum': 0.0, 'maximum': 0.0, 'average': 0.0, 'std': 0.0, 'percentile_25': 0.0, 'percentile_75': 0.0, 'percentile_5': 0.0, 'percentile_95': 0.0, 'games_played': 0.0}

	return player_stats

def get_stats(p_stats):
	total = sum(p_stats)
	minimum = min(p_stats)
	maximum = max(p_stats)
	average = np.mean(p_stats)
	std = np.std(p_stats)
	percentile_25 = np.percentile(p_stats, 25)
	percentile_75 = np.percentile(p_stats, 75)
	percentile_5 = np.percentile(p_stats, 5)
	percentile_95 =  np.percentile(p_stats, 95)
	games_played = len(p_stats)

	stats = [total, minimum, maximum, average, std, percentile_25, percentile_75, percentile_5, percentile_95, games_played]
	return [round(s, sig_fig) for s in stats]

def fantasy_stats_position(position, begin = 0, end = 0, top = -1, remove_zeros = True):
	if not begin:
		begin = nfldatabase.beginYear
		end = nfldatabase.endYear + 1
	elif not end:
		end = begin + 1
	else:
		end += 1

	pos_stats = []
	for year in range(begin, end):
		year_stats = []
		for p in player_stats_db:
			if players_db[p]['position'] == position or position == 'All':
				player = get_player_stats(p, year)
				if player:
					fantasy_pts = player_fantasy_points(player, remove_zeros)
					if sum(fantasy_pts) != 0:
						year_stats += [[p, year, fantasy_pts]]

		year_stats.sort(key = lambda x: sum(x[2]), reverse = True)
		if top != -1:
			year_stats = year_stats[:top]
		pos_stats += year_stats
	pos_stats.sort(key = lambda x: sum(x[2]), reverse = True)
	return pos_stats

def top_position_stats_week(position_stats, top = -1):
	position_stats_week = []
	for week in range(0,17):
		week_stat_pos = []
		for pos_stats in position_stats:
			if pos_stats[2][week] != 0:
				week_stat_pos.append(pos_stats[2][week])
		week_stat_pos.sort(reverse = True)
		if top != -1:
			position_stats_week.append(week_stat_pos[:top])
		else:
			position_stats_week.append(week_stat_pos)
	return position_stats_week

def avg_position_stats_year(position_stats, beginYear, endYear):
	position_stats_year = []
	for year in range(beginYear, endYear + 1):
		year_stats_pos = []
		for pos_stats in position_stats:
			if pos_stats[1] == year:
				year_stats_pos.append(pos_stats[2])
		year_stats_pos = [x for sublist in year_stats_pos for x in sublist]
		year_stats_pos.sort(reverse = True)
		position_stats_year.append(np.mean(year_stats_pos))
	return position_stats_year

def fifty_percentile_position_stats_year(position_stats, beginYear, endYear):
	position_stats_year = []
	for year in range(beginYear, endYear + 1):
		year_stats_pos = []
		for pos_stats in position_stats:
			if pos_stats[1] == year:
				year_stats_pos.append(pos_stats[2])
		year_stats_pos = [x for sublist in year_stats_pos for x in sublist]
		year_stats_pos.sort(reverse = True)
		position_stats_year.append(np.percentile(year_stats_pos, 50))
	return position_stats_year

def sorted_position_stats_year(position_stats, year):
	year_stats_pos = []
	for pos_stats in position_stats:
		if pos_stats[1] == year:
			year_stats_pos.append(sum(pos_stats[2]))
	year_stats_pos.sort(reverse = True)
	return year_stats_pos

def print_player_stats(stats):
	print 'games_played', [stats[year]['games_played'] for year in stats]
	print 'total', [stats[year]['total'] for year in stats]
	print 'minimum', [stats[year]['minimum'] for year in stats]
	print 'maximum', [stats[year]['maximum'] for year in stats]
	print 'average', [stats[year]['average'] for year in stats]
	print 'std', [stats[year]['std'] for year in stats]
	print 'percentile_25', [stats[year]['percentile_25'] for year in stats]
	print 'percentile_75', [stats[year]['percentile_75'] for year in stats]
	print 'percentile_5', [stats[year]['percentile_5'] for year in stats]
	print 'percentile_95', [stats[year]['percentile_95'] for year in stats]

def describe(scores):
	print 'total: %f' % sum(scores)
	print('(min, max) : (%f, %f)' % (min(scores), max(scores)))
	print('average: %f' % np.mean(scores))
	print('std: %f' % np.std(scores))
	print('(25, 75): (%f, %f)' % (np.percentile(scores, 25), np.percentile(scores, 75)))
	print('(5, 95): (%f, %f)' % (np.percentile(scores, 5), np.percentile(scores, 95)))

def describe_position(position, begin = 0, end = 0, top = -1, remove_zeros = True):
	vals = fantasy_stats_position(position, begin, end, top, remove_zeros)
	mod_vals = [sum(v[2]) for v in vals]
	for v in vals:
		print v[0], v[1], sum(v[2]), scipy_stats.percentileofscore(mod_vals, sum(v[2]))
	print

	print('(min, max) : (%f, %f)' % (min(mod_vals), max(mod_vals)))
	print('average: %f' % np.mean(mod_vals))
	print('std, percent: (%f, %f)' % (np.std(mod_vals), np.std(mod_vals)/np.mean(mod_vals) * 100))
	print('(25, 75): (%f, %f)' % (np.percentile(mod_vals, 25), np.percentile(mod_vals, 75)))
	print('(5, 95): (%f, %f)' % (np.percentile(mod_vals, 5), np.percentile(mod_vals, 95)))

def get_player_stats(name, year = nfldatabase.endYear+1, week = -1):
	if name in player_stats_db:
		if year in player_stats_db[name]:
			if week == -1:
				return player_stats_db[name][year]
			else:
				return player_stats_db[name][year][week]
	return None

def player_annual_stats(name):
	beginYear = nfldatabase.beginYear
	endYear = nfldatabase.endYear
	yearly_stats = OrderedDict()
	for year in range(beginYear, endYear + 1):
		if year in player_stats_db[name]:
			yearly_stats[year] =  player_fantasy_points(get_player_stats(name, year), True)
	return yearly_stats

def player_weekly_percentile(name, year, top = -1):
	player = get_player_stats(name, year)
	player_weekly_stats = player_fantasy_points(player, False)
	position = players_db[name]['position']
	position_stats = fantasy_stats_position(position, year, year, -1, False)
	position_stats_week = top_position_stats_week(position_stats, top)
	weekly_percentile = [scipy_stats.percentileofscore(y, x) for x, y in zip(player_weekly_stats, position_stats_week)]
	return [round(week_stat, sig_fig) for week_stat in weekly_percentile]

def player_weekly_ranking(name, year, top = -1):
	player = get_player_stats(name, year)
	player_weekly_stats = player_fantasy_points(player, False)
	position = players_db[name]['position']
	position_stats = fantasy_stats_position(position, year, year, -1, False)
	position_stats_week = top_position_stats_week(position_stats, top)
	weekly_ranking = [y.index(x) + 1 if x in y else 0 for x, y in zip(player_weekly_stats, position_stats_week)]
	return weekly_ranking

def player_annual_percentile(name):
	yearly_stats = player_annual_stats(name)
	years = [year for year in yearly_stats]
	position = players_db[name]['position']
	position_stats = fantasy_stats_position(position, min(years), max(years), -1, True)
	annual_percentile = []
	for year in yearly_stats:
		year_stats_pos = sorted_position_stats_year(position_stats, year)
		annual_percentile.append(scipy_stats.percentileofscore(sum(yearly_stats[year]), position_stats))
	return [round(week_stat, sig_fig) for week_stat in annual_percentile]

def player_annual_ranking(name):
	yearly_stats = player_annual_stats(name)
	years = [year for year in yearly_stats]
	position = players_db[name]['position']
	position_stats = fantasy_stats_position(position, min(years), max(years), -1, True)
	annual_ranking = []
	for year in yearly_stats:
		year_stats_pos = sorted_position_stats_year(position_stats, year)
		annual_ranking.append(year_stats_pos.index(sum(yearly_stats[year])) + 1)
	return annual_ranking

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%m/%d/%Y")
    d2 = datetime.strptime(d2, "%m/%d/%Y")
    return abs((d2 - d1).days)

def position_stats_by_age(position, remove_zeros = True):
	stats_by_age = {}
	for p in player_stats_db:
		if p in players_db and players_db[p]['position'] == position:
			for year in player_stats_db[p]:
				player = get_player_stats(p, year)
				if player:
					fantasy_pts = player_fantasy_points(player)
					birthdate = players_db[p]['birthdate']
					season_begin_date = '9/1/' + str(year)
					age = days_between(season_begin_date, birthdate)/365
					if year not in stats_by_age:
						stats_by_age[year] = {}
					if age not in stats_by_age[year]:
						stats_by_age[year][age] = []
					if remove_zeros and sum(fantasy_pts) == 0:
						continue
					else:
						stats_by_age[year][age].append(sum(fantasy_pts))

	return stats_by_age

def player_forecast_position(position):
	base_weighting = 0.50
	individual_weighting = 1.0 - base_weighting
	remove_zeros = False
	fantasy_points = position_stats_by_age(position, remove_zeros)
	fantasy_points_by_age = {}
	for year in fantasy_points:
		for age in fantasy_points[year]:
			if age not in fantasy_points_by_age:
				fantasy_points_by_age[age] = []
			for x in fantasy_points[year][age]:
				fantasy_points_by_age[age].append(x)

	for x in fantasy_points_by_age:
		fantasy_points_by_age[x] = np.mean(fantasy_points_by_age[x])

	player_forecast = OrderedDict()
	
	for p in player_stats_db:
		if p in players_db and players_db[p]['position'] == position:
			p_annual_stats = player_annual_stats(p)
			years = [year for year in p_annual_stats]
			minYear = 2013
			maxYear = 2015
			num_years = max(maxYear - minYear, 1)

			birthdate = players_db[p]['birthdate']
			season_begin_date = '9/1/' + str(thisYear)
			age = days_between(season_begin_date, birthdate)/365

			year_percentages = OrderedDict()
			p_yearly_stats = {}
			for year in range(minYear, maxYear + 1):
				year_percentages[year] = individual_weighting/(num_years+1)
				if year in p_annual_stats:
					p_yearly_stats[year] = sum(p_annual_stats[year])
				else:
					p_yearly_stats[year] = 0

			# Set annual weightings
			n = num_years
			i = 0
			divisor = 2
			while i < n/2:
				carry = year_percentages[minYear + i]/divisor
				year_percentages[minYear + i]  -= carry
				year_percentages[minYear + n - i] += carry
				divisor *= 2
				i += 1			
			individual_stats = 0
			for year in range(minYear, maxYear + 1):
				individual_stats += p_yearly_stats[year] * year_percentages[year]
				while age + minYear - year not in fantasy_points_by_age:
					age -= 1
					print age
				base_stats = fantasy_points_by_age[age + minYear - year] * year_percentages[year]
			while age not in fantasy_points_by_age:
				age -= 1
			# print p, age, individual_stats, fantasy_points_by_age[age]
			player_forecast[p] = individual_stats + base_stats # fantasy_points_by_age[age] * base_weighting
			
	player_forecast = OrderedDict(sorted(player_forecast.iteritems(), key=lambda x: x[1], reverse = True))
	for p in player_forecast:
		print p, player_forecast[p]

fantasy_scoring = league.League().fantasy_scoring
def player_fantasy_points(player, remove_zeros = True):
	# rushing stats
	rushing_att = [player[i]['rushing_att'] if i in player and 'rushing_att' in player[i] else 0 for i in range(1, 18)]
	rushing_yds = [player[i]['rushing_yds'] if i in player and 'rushing_yds' in player[i] else 0 for i in range(1, 18)]
	rushing_tds = [player[i]['rushing_tds'] if i in player and 'rushing_tds' in player[i] else 0 for i in range(1, 18)]
	rushing_twoptm = [player[i]['rushing_twoptm'] if i in player and 'rushing_twoptm' in player[i] else 0 for i in range(1, 18)]
	
	# receiving stats
	receiving_yds = [player[i]['receiving_yds'] if i in player and 'receiving_yds' in player[i] else 0 for i in range(1, 18)]
	receiving_tds = [player[i]['receiving_tds'] if i in player and 'receiving_tds' in player[i] else 0 for i in range(1, 18)]
	receiving_rec = [player[i]['receiving_rec'] if i in player and 'receiving_rec' in player[i] else 0 for i in range(1, 18)]
	receiving_twoptm = [player[i]['receiving_twoptm'] if i in player and 'receiving_twoptm' in player[i] else 0 for i in range(1, 18)]

	# passing stats
	passing_yds = [player[i]['passing_yds'] if i in player and 'passing_yds' in player[i] else 0 for i in range(1, 18)]
	passing_tds = [player[i]['passing_tds'] if i in player and 'passing_tds' in player[i] else 0 for i in range(1, 18)]
	passing_att = [player[i]['passing_att'] if i in player and 'passing_att' in player[i] else 0 for i in range(1, 18)]
	passing_cmp = [player[i]['passing_cmp'] if i in player and 'passing_cmp' in player[i] else 0 for i in range(1, 18)]
	passing_inc = [att - inc for att, inc in zip(passing_att, passing_cmp)]
	passing_ints = [player[i]['passing_ints'] if i in player and 'passing_ints' in player[i] else 0 for i in range(1, 18)]
	passing_twoptm = [player[i]['passing_twoptm'] if i in player and 'passing_twoptm' in player[i] else 0 for i in range(1, 18)]

	# kick stats .....

	# other stats
	fumbles_lost = [player[i]['fumbles_lost'] if i in player and 'fumbles_lost' in player[i] else 0 for i in range(1, 18)]
	puntret_tds = [player[i]['puntret_tds'] if i in player and 'puntret_tds' in player[i] else 0 for i in range(1, 18)]
	kickret_tds = [player[i]['kickret_tds'] if i in player and 'kickret_tds' in player[i] else 0 for i in range(1, 18)]

	fantasy_pts_receiving = [fantasy_scoring['receiving_rec'] * rec +  fantasy_scoring['receiving_yds'] * yds + fantasy_scoring['receiving_tds'] * tds + fantasy_scoring['twoptm'] * twoptm for rec, yds, tds, twoptm in zip(receiving_rec, receiving_yds, receiving_tds, receiving_twoptm)]
	
	fantasy_pts_passing = [fantasy_scoring['passing_cmp'] * comp +  fantasy_scoring['passing_yds'] * yds + fantasy_scoring['passing_inc'] * inc + fantasy_scoring['passing_tds'] * tds + fantasy_scoring['passing_ints'] * ints + fantasy_scoring['twoptm'] * twoptm for comp, inc, yds, tds, ints, twoptm in zip(passing_cmp, passing_inc, passing_yds, passing_tds, passing_ints, passing_twoptm)]

	fantasy_pts_rushing = [fantasy_scoring['rushing_yds'] * yds + fantasy_scoring['rushing_tds'] * tds + fantasy_scoring['twoptm'] * twoptm for yds, tds, twoptm in zip(rushing_yds, rushing_tds, rushing_twoptm)]

	fantasy_pts_other = [fantasy_scoring['fumbles_lost'] * fumbles + fantasy_scoring['puntret_tds'] * pret_tds + fantasy_scoring['kickret_tds'] * kret_tds for fumbles, pret_tds, kret_tds in zip(fumbles_lost, puntret_tds, kickret_tds)]

	fantasy_pts = [rush + throw + rec + neg for rush, throw, rec, neg in zip(fantasy_pts_rushing, fantasy_pts_passing, fantasy_pts_receiving, fantasy_pts_other)]
	
	if remove_zeros:
		while 0 in fantasy_pts: fantasy_pts.remove(0)
	return fantasy_pts

def annual_score_breakdown(player, year = nfldatabase.endYear):
	player_stats = get_player_stats(player, year)
	# receiving stats
	receiving_yds = [player_stats[i]['receiving_yds'] if i in player_stats and 'receiving_yds' in player_stats[i] else 0 for i in range(1, 18)]
	receiving_tds = [player_stats[i]['receiving_tds'] if i in player_stats and 'receiving_tds' in player_stats[i] else 0 for i in range(1, 18)]
	receiving_rec = [player_stats[i]['receiving_rec'] if i in player_stats and 'receiving_rec' in player_stats[i] else 0 for i in range(1, 18)]
	receiving_twoptm = [player_stats[i]['receiving_twoptm'] if i in player_stats and 'receiving_twoptm' in player_stats[i] else 0 for i in range(1, 18)]

	fantasy_pts_receiving_rec = sum(fantasy_scoring['receiving_rec'] * rec for rec in receiving_rec)
	fantasy_pts_receiving_yds = sum(fantasy_scoring['receiving_yds'] * yds for yds in receiving_yds)
	fantasy_pts_receiving_tds = sum(fantasy_scoring['receiving_tds'] * tds for tds in receiving_tds)
	fantasy_pts_receiving_twoptm = sum(fantasy_scoring['twoptm'] * twoptm for twoptm in receiving_twoptm)

	fantasy_pts_receiving = fantasy_pts_receiving_rec + fantasy_pts_receiving_yds + fantasy_pts_receiving_tds + fantasy_pts_receiving_twoptm

	# rushing stats
	rushing_att = [player_stats[i]['rushing_att'] if i in player_stats and 'rushing_att' in player_stats[i] else 0 for i in range(1, 18)]
	rushing_yds = [player_stats[i]['rushing_yds'] if i in player_stats and 'rushing_yds' in player_stats[i] else 0 for i in range(1, 18)]
	rushing_tds = [player_stats[i]['rushing_tds'] if i in player_stats and 'rushing_tds' in player_stats[i] else 0 for i in range(1, 18)]
	rushing_twoptm = [player_stats[i]['rushing_twoptm'] if i in player_stats and 'rushing_twoptm' in player_stats[i] else 0 for i in range(1, 18)]

	fantasy_pts_rushing_tds = sum(fantasy_scoring['rushing_tds'] * tds for tds in rushing_tds)
	fantasy_pts_rushing_yds = sum(fantasy_scoring['rushing_yds'] * yds for yds in rushing_yds)
	fantasy_pts_rushing_twoptm = sum(fantasy_scoring['twoptm'] * twoptm for twoptm in rushing_twoptm)

	fantasy_pts_rushing = fantasy_pts_rushing_yds + fantasy_pts_rushing_tds + fantasy_pts_rushing_twoptm

	# passing stats
	passing_yds = [player_stats[i]['passing_yds'] if i in player_stats and 'passing_yds' in player_stats[i] else 0 for i in range(1, 18)]
	passing_tds = [player_stats[i]['passing_tds'] if i in player_stats and 'passing_tds' in player_stats[i] else 0 for i in range(1, 18)]
	passing_att = [player_stats[i]['passing_att'] if i in player_stats and 'passing_att' in player_stats[i] else 0 for i in range(1, 18)]
	passing_cmp = [player_stats[i]['passing_cmp'] if i in player_stats and 'passing_cmp' in player_stats[i] else 0 for i in range(1, 18)]
	passing_inc = [att - inc for att, inc in zip(passing_att, passing_cmp)]
	passing_ints = [player_stats[i]['passing_ints'] if i in player_stats and 'passing_ints' in player_stats[i] else 0 for i in range(1, 18)]
	passing_twoptm = [player_stats[i]['passing_twoptm'] if i in player_stats and 'passing_twoptm' in player_stats[i] else 0 for i in range(1, 18)]

	fantasy_pts_passing_cmp = sum(fantasy_scoring['passing_cmp'] * comp for comp in passing_cmp)
	fantasy_pts_passing_inc = sum(fantasy_scoring['passing_inc'] * inc for inc in passing_inc)
	fantasy_pts_passing_yds = sum(fantasy_scoring['passing_yds'] * yds for yds in passing_yds)
	fantasy_pts_passing_tds = sum(fantasy_scoring['passing_tds'] * tds for tds in passing_tds)
	fantasy_pts_passing_ints = sum(fantasy_scoring['passing_ints'] * ints for ints in passing_ints)
	fantasy_pts_passing_twoptm = sum(fantasy_scoring['twoptm'] * twoptm for twoptm in passing_twoptm)

	fantasy_pts_passing = fantasy_pts_passing_cmp + fantasy_pts_passing_inc + fantasy_pts_passing_yds + fantasy_pts_passing_tds + fantasy_pts_passing_ints + fantasy_pts_passing_twoptm

	# kick stats .....

	# other stats
	fumbles_lost = [player_stats[i]['fumbles_lost'] if i in player_stats and 'fumbles_lost' in player_stats[i] else 0 for i in range(1, 18)]
	puntret_tds = [player_stats[i]['puntret_tds'] if i in player_stats and 'puntret_tds' in player_stats[i] else 0 for i in range(1, 18)]
	kickret_tds = [player_stats[i]['kickret_tds'] if i in player_stats and 'kickret_tds' in player_stats[i] else 0 for i in range(1, 18)]

	fantasy_pts_fumbles_lost = sum(fantasy_scoring['fumbles_lost'] * fumbles for fumbles in fumbles_lost)
	fantasy_pts_puntret_tds = sum(fantasy_scoring['puntret_tds'] * td for td in puntret_tds)
	fantasy_pts_kickret_tds = sum(fantasy_scoring['kickret_tds'] * td for td in kickret_tds)

	fantasy_pts_other = fantasy_pts_fumbles_lost + fantasy_pts_puntret_tds + fantasy_pts_kickret_tds

	fantasy_pts_total = fantasy_pts_receiving + fantasy_pts_rushing + fantasy_pts_passing + fantasy_pts_other

	stats_dict = OrderedDict({
		'Passing Yards': fantasy_pts_passing_yds,
		'Completions': fantasy_pts_passing_cmp,
		'Incompletions': fantasy_pts_passing_inc,
		'Passing Touchdowns': fantasy_pts_passing_tds,
		'Passing Two Point Conversion': fantasy_pts_passing_twoptm,
		'Rushing Yards': fantasy_pts_rushing_yds,
		'Rushing Touchdowns': fantasy_pts_rushing_tds,
		'Rushing Two Point Conversion': fantasy_pts_rushing_twoptm,
		'Receiving Yards': fantasy_pts_receiving_yds,
		'Receiving Touchdowns': fantasy_pts_receiving_tds,
		'Receiving Receptions': fantasy_pts_receiving_rec,
		'Receiving Two Point Conversion': fantasy_pts_receiving_twoptm,
		'Fumbles Lost': fantasy_pts_fumbles_lost,
		'Punt return Touchdowns': fantasy_pts_puntret_tds,
		'Kick return Touchdowns': fantasy_pts_kickret_tds,
		})

	# for stat in stats_dict:
	# 	stats_dict[stat] = round(stats_dict[stat]/fantasy_pts_total * 100, sig_fig)

	return OrderedDict(sorted(stats_dict.iteritems(), key=lambda x: x[1], reverse = True))

player_stats_db = nfldatabase.loadDB('nfldb')
players_db = nfldatabase.loadDB('playersdb')