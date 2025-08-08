#this python file contains functions with pre-written SQL queries that can be imported into other scripts for quicker analysis
#all query results are returned as a dataframe


import sqlite3
import os
import pandas as pd

os.chdir('/Users/chadgahafer/Desktop/Scripts/databases')
conn = sqlite3.connect('nfldb.sqlite')
cur = conn.cursor()

#query which returns average rush attempts for all teams by year
def season_average_rush_attempts():

    ra_sql = '''SELECT season AS year, AVG(rush_attempts) AS rush_attempts
                        FROM season_offensive_stats
                        GROUP BY year;
                        '''

    df = pd.read_sql_query(ra_sql, conn)
    conn.close()
    return df

#query which returns the average of all offensive stats for all teams per year
def offensive_season_averages_by_year():
    sql = '''SELECT season,
                AVG(games) AS games,
                AVG(rush_attempts) AS rush_attempts, 
                AVG(rush_yards) AS rush_yards,
                AVG(rush_tds) AS rush_tds,
                AVG(fumbles) AS fumbles,
                AVG(rush_expected_points) AS rush_expected_points,
                AVG(pass_attempts) AS pass_attempts,
                AVG(completions) AS completions ,
                AVG(s.pass_yards) AS net_pass_yards,
                AVG(s.pass_yards + s.sack_yards) AS gross_pass_yards,
                AVG(pass_tds) AS pass_touchdowns,
                AVG(interceptions) AS interceptions,
                AVG(sacks) AS sacks,
                AVG(sack_yards) AS sack_yards_lost,
                AVG( fourth_quarter_comebacks) AS fourth_quarter_comebacks,
                AVG(game_winning_drives)  AS game_winning_drives,
                AVG(pass_expected_points) AS pass_expected_points
            FROM season_offensive_stats
            GROUP BY season;'''
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

#same as above query, but only since 1970 when the full merge happened and we have data for all NFL teams
def team_offensive_averages_since_1970():
    sql = '''SELECT (t.location || ' ' || t.name) AS team,
                AVG(s.games) AS games,
                AVG(s.rush_attempts) AS rush_attempts, 
                AVG(s.rush_yards) AS rush_yards,
                AVG(s.rush_tds) AS rush_tds,
                AVG(s.fumbles) AS fumbles,
                AVG(s.rush_expected_points) AS rush_expected_points,
                AVG(s.pass_attempts) AS pass_attempts,
                AVG(s.completions) AS completions ,
                AVG(s.pass_yards) AS net_pass_yards,
                AVG(s.pass_yards + s.sack_yards) AS gross_pass_yards,
                AVG(s.pass_tds) AS pass_touchdowns,
                AVG(s.interceptions) AS interceptions,
                AVG(s.sacks) AS sacks,
                AVG(s.sack_yards) AS sack_yards_lost,
                AVG( s.fourth_quarter_comebacks) AS fourth_quarter_comebacks,
                AVG(s.game_winning_drives)  AS game_winning_drives,
                AVG(s.pass_expected_points) AS pass_expected_points
            FROM season_offensive_stats AS s
            LEFT JOIN teams AS t
                ON s.team_id = t.id
            WHERE season > 1969 
            GROUP BY team_id;'''
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

def offensive_season_averages_by_year_since_1970():
    sql = '''SELECT season,
                AVG(games) AS games,
                AVG(rush_attempts) AS rush_attempts, 
                AVG(rush_yards) AS rush_yards,
                AVG(rush_tds) AS rush_tds,
                AVG(fumbles) AS fumbles,
                AVG(rush_expected_points) AS rush_expected_points,
                AVG(pass_attempts) AS pass_attempts,
                AVG(completions) AS completions ,
                AVG(pass_yards + sack_yards) AS pass_yards,
                AVG(pass_tds) AS pass_touchdowns,
                AVG(interceptions) AS interceptions,
                AVG(sacks) AS sacks,
                AVG(sack_yards) AS sack_yards_lost,
                AVG( fourth_quarter_comebacks) AS fourth_quarter_comebacks,
                AVG(game_winning_drives)  AS game_winning_drives,
                AVG(pass_expected_points) AS pass_expected_points,
                AVG(pass_yards + sack_yards + rush_yards) AS total_yards
            FROM season_offensive_stats AS "sos"
            WHERE season > 1969
            GROUP BY season;'''
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

def o_stats_per_game_avg_since_1970():
    sql = '''SELECT season,
                AVG(games) AS games,
                AVG(rush_attempts) / games AS rush_attempts, 
                AVG(rush_yards) / games AS rush_yards,
                AVG(rush_tds) / games  AS rush_tds,
                AVG(fumbles) / games  AS fumbles,
                AVG(rush_expected_points) / games  AS rush_expected_points,
                AVG(pass_attempts) / games  AS pass_attempts,
                AVG(completions) / games  AS completions ,
                AVG(pass_yards + sack_yards) / games AS pass_yards,
                AVG(pass_tds) / games  AS pass_touchdowns,
                AVG(interceptions) / games  AS interceptions,
                AVG(sacks) / games AS sacks,
                AVG(sack_yards) / games  AS sack_yards_lost,
                AVG( fourth_quarter_comebacks) / games  AS fourth_quarter_comebacks,
                AVG(game_winning_drives) / games  AS game_winning_drives,
                AVG(pass_expected_points) / games AS pass_expected_points,
                AVG(pass_yards + sack_yards + rush_yards) / games AS total_yards
            FROM season_offensive_stats AS "sos"
            WHERE season > 1969
            GROUP BY season'''
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

def off_and_def_expected_points_joined():
    sql = '''SELECT (teams.location || " " || teams.name) AS team,
                off_stats.season,
                off_stats.pass_expected_points AS off_pass_epa,
                off_stats.rush_expected_points AS off_rush_epa,
                off_stats.rush_attempts AS off_rush_attempts,
                (off_stats.rush_expected_points / off_stats.rush_attempts) AS off_rush_epa_play,
                off_stats.rush_attempts AS off_rush_attempts,
                (off_stats.pass_expected_points / off_stats.pass_attempts) AS off_pass_epa_play,
                def_stats.pass_expected_points AS def_pass_epa,
                def_stats.rush_expected_points AS def_rush_epa,
                def_stats.rush_attempts AS def_rush_attempts,
                (def_stats.rush_expected_points / def_stats.rush_attempts) AS def_rush_epa_play,
                def_stats.pass_attempts AS def_pass_attempts,
                (def_stats.pass_expected_points / def_stats.pass_attempts) AS def_pass_epa_play,
                (off_stats.pass_expected_points + off_stats.rush_expected_points) AS total_off_epa,
                ((off_stats.pass_expected_points + off_stats.rush_expected_points) / (off_stats.rush_attempts + off_stats.pass_attempts)) AS total_off_epa_play,
                (def_stats.pass_expected_points + def_stats.rush_expected_points) AS total_def_epa,
                ((def_stats.pass_expected_points + def_stats.rush_expected_points) / (def_stats.rush_attempts + def_stats.pass_attempts)) AS total_def_epa_play,
                (CAST(rec.wins AS REAL) / (rec.wins + rec.losses + rec.ties)) AS win_pct
            FROM season_offensive_stats AS off_stats
            LEFT JOIN season_defensive_stats AS def_stats
                ON off_stats.team_id = def_stats.team_id AND off_stats.season = def_stats.season
            LEFT JOIN season_records AS rec 
                ON off_stats.team_id = rec.team_id AND off_stats.season = rec.season
            LEFT JOIN teams
                ON teams.id = off_stats.team_id
            WHERE off_stats.pass_expected_points IS NOT NULL 
                AND off_stats.rush_expected_points IS NOT NULL
                AND def_stats.pass_expected_points IS NOT NULL
                AND def_stats.rush_expected_points IS NOT NULL'''
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df


def most_wins_2020():
    sql = '''SELECT (teams.location || " " || teams.name) AS team, season_records.wins
            FROM season_records
            LEFT JOIN teams
                ON season_records.team_id = teams.id
            WHERE season = 2020
            ORDER BY wins DESC
            LIMIT 1'''
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

def seasons_team_8wins_8losses():
    sql = '''SELECT DISTINCT(season)
            FROM season_records
            WHERE wins = 8 AND losses = 8'''
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

def pos_pt_diff_2021():
    sql = '''SELECT (t.location || " " || t.name) AS team, sr.point_differential
            FROM season_records AS sr
            LEFT JOIN teams AS t
            ON sr.team_id = t.id
            WHERE season = 2021 AND point_differential > 0'''
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

def fewest_points_2019():
    sql = '''SELECT (t.location || " " || t.name) AS team, sr.points_allowed
            FROM season_records AS sr
            LEFT JOIN teams AS t
                ON sr.team_id = t.id
            WHERE season = 2019
            ORDER BY points_allowed ASC
            LIMIT 1'''
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df


def top5_forced_points():
    sql = '''SELECT (t.location || " " || t.name) AS team, sr.points_forced, sr.season
            FROM season_records AS sr
            LEFT JOIN teams AS t
                ON sr.team_id = t.id
            ORDER BY points_forced DESC
            LIMIT 5'''
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

if __name__ == "__main__":
    x = season_average_rush_attempts()
    print(x)