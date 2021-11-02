from nba_api.stats.endpoints import boxscoretraditionalv2,PlayerCareerStats,LeagueGameFinder
from nba_api.stats.static import players,teams
import pandas as pd
import time


def get_matchup_team(player1_name,team_name,nb_year,season_type):

    team_id = teams.find_teams_by_full_name(team_name)[0]['id']
    player_name = players.find_players_by_full_name(player1_name)[0]['full_name']
    player1 = players.find_players_by_full_name(player1_name)[0]['id']

    
    data = PlayerCareerStats(player_id=player1).get_data_frames()[0]
    dict_player_1={}
    for row in data.itertuples():
        if row.SEASON_ID not in list(dict_player_1.keys()):
            dict_player_1[row.SEASON_ID] = []
            dict_player_1[row.SEASON_ID].append(row.TEAM_ID)
        else :

            if row.TEAM_ID != 0:
                dict_player_1[row.SEASON_ID].append(row.TEAM_ID)

    time.sleep(.600)

    player_name_list = []
    ttfl_points_list = []
    player_team_list = []
    date_list=[]
    game_id_list=[]
    vs_team=[]
    win_or_lose=[]

    player_name = player_name




    for i in range(nb_year):

        year = 2021-i
        if i>22:
            year2 = 122-i
        else:
            year2 = 22-i

        if year2<10:
            year2 = f'0{year2}'

        season = f'{year}-{year2}'

        yield i

        print(season)


        
        match_list = LeagueGameFinder(player_id_nullable=player1,vs_team_id_nullable=team_id,league_id_nullable='00',season_nullable=season,season_type_nullable=season_type).get_data_frames()[0]
        print(match_list)
        set_list_game_ids = set(match_list['GAME_ID'])
        time.sleep(0.600) 
        for game_id in set_list_game_ids:

            data_match = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id).get_data_frames()[0]     
            time.sleep(0.600) 




            player = data_match[data_match['PLAYER_ID']== player1].iloc[0]
            player_name = player_name

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
            
            try:

                ttfl_points = int(ttfl_points)
                ttfl_points_list.append(ttfl_points)
                player_name_list.append(player_name)
                player_team_list.append(player['TEAM_ABBREVIATION'])
                game_id_list.append(game_id)
                date_list.append(match_list[match_list['GAME_ID'] == game_id].iloc[0]['GAME_DATE'])
                win_or_lose.append(match_list[match_list['GAME_ID'] == game_id].iloc[0]['WL'])
                vs_team.append(team_name)
                

            except:
                pass

    yield pd.DataFrame({'Player': player_name_list,'Team':player_team_list,"VS team":vs_team,'ttfl_points':ttfl_points_list,"Date":date_list,"W/L ?" : win_or_lose})

