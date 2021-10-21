import streamlit as st
import pandas as pd
from urllib.error import URLError
import pandas as pd
from get_day_records import *


def app():



    liste_player = ["Kawhi Leonard","Paul George","Ja Morant",
    "Rudy Gobert","Donovan Mitchell","De'Aaron Fox","Richaun Holmes","Harrison Barnes","Anthony Davis","LeBron James","Russell Westbrook","Luka Doncic","Kristaps Porzingis","Nikola Jokic","Jamal Murray","Michael Porter Jr.","Brandon Ingram","Zion Williamson","Jonas Valanciunas","John Wall","Christian Wood","Dejounte Murray","Chris Paul","Devin Booker","Deandre Ayton","Shai Gilgeous-Alexander","Karl-Anthony Towns","Damian Lillard","CJ McCollum","Stephen Curry","Klay Thompson","Andrew Wiggins","Joel Embiid","Ben Simmons","Tobias Harris","Andre Drummond","Giannis Antetokounmpo","Khris Middleton","Jrue Holiday",
    "Zach LaVine","Nikola Vucevic","DeMar DeRozan","Jarrett Allen","Collin Sexton","Jayson Tatum","Jaylen Brown","Enes Kanter","Trae Young","John Collins","Clint Capela","Jimmy Butler","Bam Adebayo","Kyle Lowry","Gordon Hayward",
    "LaMelo Ball","Terry Rozier","Julius Randle","Kemba Walker","Kevin Durant","James Harden","Kyrie Irving","Domantas Sabonis","Malcolm Brogdon","Caris LeVert","Jerami Grant","Pascal Siakam","Fred VanVleet","Spencer Dinwiddie","Bradley Beal"]

    try:

            with st.spinner('Wait for it...'):

                data=get_day_records()
            st.success('Done!')
            st.balloons()

            data = data.sort_values(by='ttfl_points',ascending=False)

            data_top=data[data['ttfl_points']>=40]
            st.write("### Ils ont cartonnés", data_top)

            data_boulot=data[data['ttfl_points'].between(30,39)]
            st.write("### Ils ont fait le boulot ", data_boulot)

            data_mieux=data[data['ttfl_points'].between(24,29)]
            data_mieux=data_mieux[data_mieux['Player'].isin(liste_player)]
            st.write("### Ils peuvent faire mieux", data_mieux)

            data_pourri=data[data['ttfl_points'].between(15,23)]
            data_pourri=data_pourri[data_pourri['Player'].isin(liste_player)]

            st.write("### Un peu pourri quand même", data_pourri)


            data_carote=data[data['ttfl_points']<16]
            data_carote=data_carote[data_carote['Player'].isin(liste_player)]
            st.write("### Les belles carrotes", data_carote)


            # except:
            #     st.error('Une erreur est survenue, veuillez réessayer ultérieuerement')

    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )
