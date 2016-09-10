import database
import stats as nfl_stats
import nfl_graphs
import numpy as np
import league

name = "Greg Olsen"
position = nfl_stats.players_db[name]['position']
league_info = league.League()
top_x = league_info.positions[position] * league_info.teams
year = 2015
nfl_stats.player_forecast_position(position)
# nfl_stats.describe_position(position, 2011, 2011, 20, False)
# player_stats = nfl_stats.get_player_stats(name, year)
# player_stats_fantasy = nfl_stats.player_fantasy_points(player_stats, False)
# nfl_graphs.player_weekly_points(name, year, player_stats_fantasy)
# yearly_stats = nfl_stats.get_player_stats(name)
# nfl_graphs.player_yearly_stats_avg(name, position, yearly_stats)
# print [round(np.percentile(yearly_stats[i], 50), 3) for i in yearly_stats]
# print [round(np.mean(yearly_stats[i]), 3) for i in yearly_stats]
# nfl_graphs.position_fantasy_points_age_distribution(position, 10)
# nfl_graphs.player_score_breakdown(name, year)