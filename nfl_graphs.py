import plotly.tools as py_tools
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import stats as nfl_stats
import plotly_info
from collections import OrderedDict

py_tools.set_credentials_file(username=plotly_info.username, api_key=plotly_info.api_key)
sig_figs = 2

def player_weekly_points(name, year, player_pts):
	scatter = go.Scatter(
		x = range(1, 18),
		y = player_pts,
		mode = 'lines+markers'
		)

	data = [scatter]
	layout = dict(title = name + "'s Weekly Points for " + str(year) + "/" + str(year + 1),
		xaxis = dict(title = 'Week'),
		yaxis = dict(title = 'Fantasy Points'))
	fig = dict(data = data, layout = layout)
	py.iplot(fig, filename = "Player's Weekly Fantasy Points")

def player_yearly_stats_avg(name, position, yearly_stats):	
	x = [i for i in yearly_stats]
	y = [round(np.mean(yearly_stats[i]), sig_figs) for i in x]
	
	position_stats = nfl_stats.fantasy_stats_position(position, min(x), max(x), 30, True)
	y_2 = nfl_stats.avg_position_stats_year(position_stats, min(x), max(x))
	y_2 = [round(i, sig_figs) for i in y_2]
	scatter = go.Scatter(
		x = x,
		y = y,
		mode = 'lines+markers',
		name = name
		)

	scatter2 = go.Scatter(
		x = x,
		y = y_2,
		mode = 'lines+markers',
		name = position + ' Average'
		)

	data = [scatter, scatter2]
	layout = dict(title = name + "'s Yearly Average Fantasy Points",
		xaxis = dict(title = 'Year', dtick = 1),
		yaxis = dict(title = 'Fantasy Points'))
	fig = dict(data = data, layout = layout)
	py.iplot(fig, filename = "Player's Yearly Average Fantasy Points")

def position_fantasy_points_age_distribution(position, top = -1, remove_zeros = True):
	fantasy_points = nfl_stats.position_stats_by_age(position, remove_zeros)
	fantasy_points_by_age = {}
	for year in fantasy_points:
		for age in fantasy_points[year]:
			if age not in fantasy_points_by_age:
				fantasy_points_by_age[age] = []
			for x in fantasy_points[year][age]:
				fantasy_points_by_age[age].append(x)

	x = [i for i in fantasy_points_by_age]
	y = [fantasy_points_by_age[i] for i in x]
	
	if top != -1:
		for i in range(0, len(y)):
			y[i].sort(reverse = True)
			y[i] = y[i][:top]

	N = len(x)
	colors = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]

	traces = []

	for xd, yd, color in zip(x, y, colors):
	        traces.append(go.Box(
	            y=yd,
	            name=xd,
	            boxpoints='all',
	            jitter=0.5,
	            whiskerwidth=0.2,
	            fillcolor=color,
	            marker=dict(
	                size=3,
	                color = 'rgb(0, 0, 0)'
	            ),
	            line=dict(width=1),
	            boxmean = 'sd'
	        ))

	layout = go.Layout(
	    title = position + " Fantasy Points Distribution by Age",
	    xaxis = dict(title = 'Age', dtick = 1),
	    yaxis=dict(
	        autorange=True,
	        showgrid=True,
	        zeroline=True,
	        gridcolor='rgb(255, 255, 255)',
	        gridwidth=1,
	        zerolinecolor='rgb(255, 255, 255)',
	        zerolinewidth=2,
	        title = 'Fantasy Points'
	    ),
	    margin=dict(
	        l=40,
	        r=30,
	        b=80,
	        t=100,
	    ),
	    paper_bgcolor='rgb(243, 243, 243)',
	    plot_bgcolor='rgb(243, 243, 243)',
	    showlegend=False
	)

	fig = go.Figure(data=traces, layout=layout)
	py.iplot(fig, filename = "Position Fantasy Points Distribution by Age")

def player_score_breakdown(player_name, year):
	yearly_stats = nfl_stats.annual_score_breakdown(player_name, year)
	
	# total = sum(yearly_stats[i] for i in yearly_stats)
	# pi_graph_stats = OrderedDict()
	# limit = 5
	# count = 0
	# for i in yearly_stats:
	# 	pi_graph_stats[i] = yearly_stats[i]
	# 	count += 1
	# 	if count >= limit:
	# 		break
	# pi_graph_stats['Other'] = total - sum(pi_graph_stats[i] for i in pi_graph_stats)
	# print pi_graph_stats

	fig = {
	  "data": [
	    {
	      "labels": [i for i in yearly_stats],
	      "values": [yearly_stats[i] for i in yearly_stats],
	      "hoverinfo":"label+percent+name",
	      "hole": .4,
	      "type": "pie"
	    }],
	  "layout": {
	        "title": player_name + "'s " + str(year) + " Fantasy Points Breakdown",
	    }
	}
	py.iplot(fig, filename = "Fantasy Points Breakdown")