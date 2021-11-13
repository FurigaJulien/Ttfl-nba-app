from nba_api.stats.endpoints import playergamelog,boxscoretraditionalv2,commonallplayers
from nba_api.stats.static.players import find_players_by_full_name
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt 


def get_player_shoot(player_name,nb,season_type,shoot_type):
    all_season={}

    try :

        player = find_players_by_full_name(player_name)[0]
        player_id = player['id']


    except:

        all_players = commonallplayers.CommonAllPlayers().get_data_frames()[0]
        player_id = all_players[all_players['DISPLAY_FIRST_LAST'] == player_name]['PERSON_ID'].values[0]



    time.sleep(1)
    print(player_id)

    j=0
    for i in range(nb):

        year = 2021-i
        if i>22:
            year2 = 122-i
        else:
            year2 = 22-i

        if year2<10:
            year2 = f'0{year2}'

        season = f'{year}-{year2}'
        yield i,season,player_id
        print(season)

        data_match = playergamelog.PlayerGameLog(player_id=player_id,season=season,season_type_all_star=season_type,league_id_nullable='00').get_data_frames()[0]
        time.sleep(1)
        player_name_list = []
        ttfl_points_list = []
        player_team_list = []

        nb_attempted=[]
        nb_succeed=[]

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
            
            ttfl_free_throw_points = free_throw*2 - (free_throw_attempted-free_throw) 
            ttfl_f3_points = three_pt_fg*4 - (three_pt_attempted-three_pt_fg)
            ttfl_fg_poitns = field_goals*3 - (field_goals_attempted-field_goals)

            if shoot_type == 'LF':

                try:

                    ttfl_points_list.append(ttfl_free_throw_points)
                    player_name_list.append(player_name)
                    player_team_list.append(player['MATCHUP'])
                    nb_attempted.append(free_throw_attempted)
                    nb_succeed.append(free_throw)
                    

                except:
                    pass
            
            if shoot_type == 'field_goals_3':

                try:

                    ttfl_points_list.append(ttfl_f3_points)
                    player_name_list.append(player_name)
                    player_team_list.append(player['MATCHUP'])
                    nb_attempted.append(three_pt_attempted)
                    nb_succeed.append(three_pt_fg)
                    

                except:
                    pass

                    
            if shoot_type == 'field_goals':

                try:

                    ttfl_points_list.append(ttfl_fg_poitns)
                    player_name_list.append(player_name)
                    player_team_list.append(player['MATCHUP'])
                    nb_attempted.append(field_goals_attempted)
                    nb_succeed.append(field_goals)
                    

                except:
                    pass



        d = pd.DataFrame({'Player': player_name_list,'Team':player_team_list,'ttfl_points':ttfl_points_list,"Attempted":nb_attempted,"Succed":nb_succeed}).groupby('Player').mean()
        d['ttfl/attempted']=d['ttfl_points']/d['Attempted']
        d["season"]=[season]
        all_season[season]=d.iloc[0].to_dict()

    ttfl_points =[]
    attempted = []
    succed =[]
    tt_attempt = []
    season = []

    for values in all_season.values():
        ttfl_points.append(values['ttfl_points'])
        attempted.append(values['Attempted'])
        succed.append(values['Succed'])
        tt_attempt.append(values['ttfl/attempted'])
        season.append(values['season'])

    data = pd.DataFrame({'Season':season,'TTFL points in shoot sector':ttfl_points,'Attempted':attempted,"Succed":succed,'ttfl/attempted':tt_attempt})
    yield data,season,player_id
