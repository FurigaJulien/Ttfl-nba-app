from nba_api.stats.endpoints import leaguegamefinder,boxscoretraditionalv2,playergamelog
from nba_api.stats.static.players import find_players_by_full_name
import calendar

import pandas as pd
import time



def get_mlk_day_date(year):


    c = calendar.Calendar(firstweekday=calendar.SUNDAY)
    year = year; month = 1

    monthcal = c.monthdatescalendar(year,month)
    third_monday = [day for week in monthcal for day in week if \
                    day.weekday() == calendar.FRIDAY and \
                    day.month == month][2]
    return third_monday.day


def get_special_dates_records(special_day,nb):



    player_name_list = []
    game_id_list = []
    ttfl_points_list = []
    player_team_list = []
    date_list=[]

    for i in range(nb):

        yield i


        if special_day == "Closing night":
            year = 2020-i
            if i>21:
                year2 = 121-i
            else:
                year2 = 21-i

            if year2<10:
                year2 = f'0{year2}'
        else:
            year = 2021-i
            if i>22:
                year2 = 122-i
            else:
                year2 = 22-i

            if year2<10:
                year2 = f'0{year2}'

        season = f'{year}-{year2}'
        print(season)

        if special_day == "Opening night":
            game_date = leaguegamefinder.LeagueGameFinder(season_nullable=season,season_type_nullable='Regular Season',league_id_nullable='00').get_data_frames()[0].sort_values('GAME_DATE').iloc[0]['GAME_DATE']
            time.sleep(.600)
            print(game_date)
            date = game_date.split('-')
            game_date = f'{date[1]}/{date[2]}/{date[0]}'

        if special_day == "Closing night":
            game_date = leaguegamefinder.LeagueGameFinder(season_nullable=season,season_type_nullable='Regular Season',league_id_nullable='00').get_data_frames()[0].sort_values('GAME_DATE').iloc[-1]['GAME_DATE']
            time.sleep(.600)
            
            date = game_date.split('-')
            game_date = f'{date[1]}/{date[2]}/{date[0]}'

        if special_day == "Christmas day":

            game_date = f'12/25/{year}'

        if special_day == "MLK day":

            day = get_mlk_day_date(year)
            game_date = f'01/{day}/{year}'

        print(game_date)

        set_list_game_ids = set(leaguegamefinder.LeagueGameFinder(date_from_nullable=game_date,date_to_nullable=game_date,season_type_nullable='Regular Season',league_id_nullable='00').get_data_frames()[0]['GAME_ID'])
        
        for game_id in set_list_game_ids:

            data_match = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id).get_data_frames()[0]
            time.sleep(.600)

            for i in range(len(data_match)):
                
                player = data_match.iloc[i]
                player_name = player['PLAYER_NAME']
                minutes_played = player['MIN']
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
                    date_list.append(game_date)
                    

                except:
                    pass

    yield pd.DataFrame({'Player': player_name_list,'Team':player_team_list,'ttfl_points':ttfl_points_list,'Date':date_list,'game_id':game_id_list})