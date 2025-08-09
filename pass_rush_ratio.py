import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('bmh')
from nfldb_queries import o_stats_per_game_avg_since_1970 #importing the function which returns a SQL query as a dataframe
import matplotlib.pyplot as plt

offensive_season_averages = o_stats_per_game_avg_since_1970() 

pass_rush_ratio = offensive_season_averages[['season', 'pass_attempts', 'rush_attempts']].copy()
pass_rush_ratio['pass_rush_ratio'] = (
    offensive_season_averages['pass_attempts'] /
    offensive_season_averages['rush_attempts']
)


plt.plot(pass_rush_ratio['season'], pass_rush_ratio['pass_rush_ratio'])
plt.xlabel('Season')
plt.ylabel('Pass / Rush Ratio')
plt.xlim(1970, 2024)
plt.ylim(0, 1.75)
plt.title("Ratio of Pass Attempts to Rush Attempts by NFL Season")

plt.axhline(y=1, c