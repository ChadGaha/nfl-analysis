#this python script pulls data from nfldb via nfldb_queries
#it produces a figure with two line charts using matplotlib which shows how passing has surpassed rushing in both yards produced and attempts

import pandas as pd
import matplotlib.pyplot as plt
from nfldb_queries import o_stats_per_game_avg_since_1970 #importing the function which returns a SQL query as a dataframe

offensive_season_averages = o_stats_per_game_avg_since_1970() #calling the function

fig, axes = plt.subplots(1, 2, figsize=(15, 6)) #using subplots() to show two graphs in one viz

#creating the first graph
axes[0].plot(offensive_season_averages['season'], offensive_season_averages['pass_yards'], label='Pass Yards')
axes[0].plot(offensive_season_averages['season'], offensive_season_averages['rush_yards'], label='Rush Yards')

axes[0].set_xlim(1970, 2024)
axes[0].set_ylim(50, 300) #setting the y axis limit appropriately
axes[0].legend() #adding a legend for the first graph
axes[0].set_title('Offensive Yard Averages Per Game By Season')

#creating the second graph
axes[1].plot(offensive_season_averages['season'], offensive_season_averages['pass_attempts'], label='Pass Attempts')
axes[1].plot(offensive_season_averages['season'], offensive_season_averages['rush_attempts'], label='Rush Attempts')

axes[1].set_xlim(1970, 2024)
axes[1].set_ylim(15, 50) #setting the y axis limit appropriately
axes[1].legend() #adding a legend for the first graph
axes[1].set_title('Passing and Rushing Attempts Per Game Per Season')

plt.show()