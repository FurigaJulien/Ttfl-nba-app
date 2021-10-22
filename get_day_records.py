import datetime
from nba_api.stats.endpoints import playergamelog,leaguegamefinder,boxscoretraditionalv2
from nba_api.stats.static.players import find_players_by_full_name
import pandas as pd
import time
from nba_api.stats.endpoints import CumeStatsPlayer
from Proxy_List_Scrapper import Scrapper



def get_day_records():

    today = datetime.date.today()
    game_date = today.strftime("%m/%d/20%y")
    print("game_date =", game_date)

    data = []
    while len(data)==0:
        print(game_date)
        data = find_ttfl_record_for_day(game_date)
        date = game_date.split('/')
        game_date = f'{date[0]}/{int(date[1])-1}/{date[2]}'

    return data

def find_ttfl_record_for_day(game_date):

    player_name_list = []
    game_id_list = []
    ttfl_points_list = []
    player_team_list = []
    date_list=[]
    game_status_list=[]


 
            
    set_list_game_ids = set(leaguegamefinder.LeagueGameFinder(date_from_nullable=game_date,date_to_nullable=game_date,league_id_nullable='00').get_data_frames()[0]['GAME_ID'])
    time.sleep(0.600)



    print(f"Checking datas for {len(set_list_game_ids)} games")

    if len(set_list_game_ids)>0:

      for game_id in set_list_game_ids:

                  
        data_match = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id).get_data_frames()[0]
        time.sleep(0.600)

            
    for i in range(len(data_match)):
        
        player = data_match.iloc[i]
        player_name = player['PLAYER_NAME']
        if player['MIN'] is not None:
            
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
            game_status="Terminé"
            ttfl_points = three_pt_fg - (three_pt_attempted-three_pt_fg) + assists + blocks + field_goals - (field_goals_attempted-field_goals) + free_throw - (free_throw_attempted-free_throw) + rebunds + steal - turnover + points
        else:
            player = CumeStatsPlayer(player_id=player['PLAYER_ID'],game_ids=[player['GAME_ID']]).get_data_frames()[0]
            time.sleep(0.600)

            three_pt_fg = player['FG3']
            three_pt_attempted = player['FG3A']
            assists = player['AST']
            blocks = player['BLK']
            field_goals = player['FG']
            field_goals_attempted = player['FGA']
            free_throw = player['FT']
            free_throw_attempted = player['FTA']
            rebunds = player['TOT_REB']
            steal = player['STL']
            turnover = player['TURNOVERS']
            points = player['PTS']
            game_status="En cours"
            ttfl_points = three_pt_fg - (three_pt_attempted-three_pt_fg) + assists + blocks + field_goals - (field_goals_attempted-field_goals) + free_throw - (free_throw_attempted-free_throw) + rebunds + steal - turnover + points
            

        try:
            ttfl_points = int(ttfl_points)
        except:
            ttfl_points = 0
        ttfl_points_list.append(ttfl_points)
        player_name_list.append(player_name)
        game_id_list.append(game_id)
        game_status_list.append(game_status)
        date_list.append(game_date)
                
                


    return pd.DataFrame({'Player': player_name_list,'ttfl_points':ttfl_points_list,"Game Status":game_status_list,'Date':date_list,'game_id':game_id_list})




