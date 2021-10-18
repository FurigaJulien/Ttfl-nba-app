from nba_api.stats.endpoints import playergamelog,boxscoretraditionalv2
from nba_api.stats.static.players import find_players_by_full_name
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt 





def get_player_record(player_name,nb,season_type):


    player_name_list = []
    ttfl_points_list = []
    player_team_list = []
    date_list=[]
    game_id_list=[]

    player_name = player_name

    player_id = find_players_by_full_name(player_name)[0]['id']
    time.sleep(1)
    print(player_id)

    j=0
    for i in range(nb):

        year = 2020-i
        if i>21:
            year2 = 121-i
        else:
            year2 = 21-i

        if year2<10:
            year2 = f'0{year2}'

        season = f'{year}-{year2}'
        yield i,season,player_id
        print(season)

        data_match = playergamelog.PlayerGameLog(player_id=player_id,season=season,season_type_all_star=season_type,league_id_nullable='00').get_data_frames()[0]
        time.sleep(1)

        for i in range(len(data_match)):
            
            player = data_match.iloc[i]
            player_name = player_name
            game_id = player['Game_ID']
            three_pt_fg = player['FG3M']
            three_pt_attempted = player['FG3A']
            assists = player['AST']
            blocks = player['BLK']
            field_goals = player['FGM']
            field_goals_attempted = player['FGA']
            free_throw = player['FTM']
            free_throw_attempted = player['FTA']
            rebunds = player['REB']
            steal = player['STL']
            turnover = player['TOV']
            points = player['PTS']
            game_date = player['GAME_DATE']
            ttfl_points = three_pt_fg - (three_pt_attempted-three_pt_fg) + assists + blocks + field_goals - (field_goals_attempted-field_goals) + free_throw - (free_throw_attempted-free_throw) + rebunds + steal - turnover + points
            
            try:

                ttfl_points = int(ttfl_points)
                ttfl_points_list.append(ttfl_points)
                player_name_list.append(player_name)
                player_team_list.append(player['MATCHUP'])
                game_id_list.append(game_id)
                date_list.append(game_date)
                

            except:
                pass

    data = pd.DataFrame({'Player': player_name_list,'Team':player_team_list,'ttfl_points':ttfl_points_list,'Date':date_list,'Game ID':game_id_list})

    yield data,season,player_id


def get_player_best_match_graph(game_id,player_id):
    data_match = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id= game_id).get_data_frames()[0]


        
    player = data_match[data_match['PLAYER_ID'] == player_id ]
    player_name = player['PLAYER_NAME']
    three_pt_fg = player['FG3M']
    three_pt_attempted = player['FG3A']
    assists = player['AST']
    blocks = player['BLK']
    field_goals = player['FGM']
    field_goals_attempted = player['FGA']
    free_throw = player['FTM']
    free_throw_attempted = player['FTA']
    rebunds = player['REB']
    steal = player['STL']
    turnover = player['TO']
    points = player['PTS']
    ttfl_points = three_pt_fg - (three_pt_attempted-three_pt_fg) + assists + blocks + field_goals - (field_goals_attempted-field_goals) + free_throw - (free_throw_attempted-free_throw) + rebunds + steal - turnover + points
    ttfl_points = ttfl_points



    def add_to_radar(player, label,color):
        values = player
        values += values[:1]
        ax.plot(angles, values, color=color, linewidth=1, label=label)
        ax.fill(angles, values, color=color, alpha=0.25)

    player_attempted = [points,rebunds,assists,three_pt_attempted,field_goals_attempted,free_throw_attempted,steal,blocks,turnover]
    player_success = [points,rebunds,assists,three_pt_fg,field_goals,free_throw,steal,blocks,turnover]

    labels=["Points","Rebonds","Assist","3 points tentés / réussis","FG tentés / réussis","LF tentés / réussis","Steal","Block","Turn-over"]
    # Number of variables we're plotting.
    num_vars = len(labels)

    # Split the circle into even parts and save the angles
    # so we know where to put each axis.
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # The plot is a circle, so we need to "complete the loop"
    # and append the start value to the end.
    angles += angles[:1]

    # ax = plt.subplot(polar=True)
    fig, ax = plt.subplots(figsize=(15, 15), subplot_kw=dict(polar=True))

    add_to_radar(player_attempted,"Tentés",'#1aaf6c')
    add_to_radar(player_success,"Réussi",'#1aaf8c')

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim(0,int(points))
    # Draw axis lines for each angle and label.
    ax.set_thetagrids(np.degrees(angles), labels)
    for label, angle in zip(ax.get_xticklabels(), angles):
        
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')



    # Add title.
    ax.set_title(f"", y=1.08)


