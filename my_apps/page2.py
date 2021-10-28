import streamlit as st
import pandas as pd
from urllib.error import URLError
import pandas as pd
from get_day_records import *


def app():


    liste_player = ["Trae Young","Clint Capela" ,
"John Collins",
"Bogdan Bogdanovic",
"De'Andre Hunter",
"Cam Reddish",
"Jayson Tatum" ,
"Jaylen Brown",
"Dennis Schroder",
"Al Horford",
"Marcus Smart",
"Enes Kanter",
"Robert Williams",
"LaMelo Ball",
"Terry Rozier",
"Miles Bridges",
"Aleksej Pokusevski",
"Gordon Hayward",
"Mason Plumlee",
"Kelly Oubre" ,
"James Bouknight",
"Jerami Grant",
"Cade Cunningham" ,
"Kelly Olynyk" ,
"Saddiq Bey" ,
"Christian Wood",
"Jalen Green" ,
"Kevin Porter Jr.",
"LeBron James" ,
"Anthony Davis" ,
"Russell Westbrook",
"Carmelo Anthony",
"Dwight Howard" ,
"Kendrick Nunn",
"Paul George" ,
"Reggie Jackson" ,
"Terance Mann",
"Ivica Zubac" ,
"Marcus Morris",
"Eric Bledsoe",
"Zion Williamson" ,
"Brandon Ingram",
"Jonas Valanciunas",
"Devont'e Graham" ,
"Nickeil Alexander-Walker" ,
"Luka Doncic",
"Kristaps Porzingis" ,
"Tim Hardaway Jr.",
"Jalen Brunson" ,
"Evan Mobley",
"Collin Sexton" ,
"Darius Garland" ,
"Jarrett Allen" ,
"Lauri Markkanen" ,
"Shai Gilgeous-Alexander" ,
"Luguentz Dort",
"Darius Bazley",
"Josh Giddey" ,
"Theo Maledon" ,
"Damian Lillard",
"C.J. McCollum",
"Norman Powell",
"Jusuf Nurkic",
"Anfernee Simons" ,
"Pascal Siakam",
"Fred VanVleet",
"OG Anunoby" ,
"Scottie Barnes" ,
"Gary Trent Jr.",
"Chris Boucher",
"Zach LaVine" ,
"DeMar DeRozan",
"Nikola Vucevic" ,
"Lonzo Ball" ,
"Coby White" ,
"Patrick Williams" ,
"Bradley Beal",
"Spencer Dinwiddie",
"Rui Hachimura" ,
"Kyle Kuzma",
"Montrezl Harrell",
"Davis Bertans" ,
"Kevin Durant" ,
"James Harden" ,
"Kyrie Irving" ,
"Joe Harris" ,
"Steven Adams",
"LaMarcus Aldridge" ,
"Nikola Jokic",
"Michael Porter Jr.",
"Aaron Gordon" ,
"Will Barton" ,
"Kemba Walker" ,
"Julius Randle",
"Evan Fournier" ,
"Bojan Bogdanovic",
"R.J. Barrett" ,
"Derrick Rose",
"Devonte' Graham",
"Ja Morant",
"Jaren Jackson Jr.",
"Dillon Brooks",
"Kyle Anderson",
"Stephen Curry",
"Klay Thompson",
"Draymond Green",
"Andrew Wiggins",
"Jordan Poole",
"James Wiseman" ,
"Jimmy Butler" ,
"Bam Adebayo" ,
"Kyle Lowry",
"Duncan Robinson" ,
"Tyler Herro",
"Victor Oladipo",
"Joel Embiid",
"Ben Simmons" ,
"Tobias Harris" ,
"Andre Drummond" ,
"Devin Booker" ,
"Deandre Ayton",
"Chris Paul" ,
"Mikal Bridges" ,
"Giannis Antetokounmpo" ,
"Jrue Holiday" ,
"Khris Middleton" ,
"Brook Lopez" ,
"Rudy Gobert" ,
"Donovan Mitchell" ,
"Mike Conley" ,
"Bogdan Bogdanovic" ,
"Jordan Clarkson" ,
"Domantas Sabonis" ,
"Malcolm Brogdon" ,
"Caris LeVert" ,
"Myles Turner" ,
"T.J Warren",
"Chris Duarte",
"Wendell Carter Jr.",
"Mo Bamba" ,
"Cole Anthony",
"Jalen Suggs",
"Dejounte Murray" 
"Derrick White" ,
"Keldon Johnson" ,
"Joe Ingles",
"Goran Dragic",
"Thaddeus Young","Jakob Poeltl",
"De'Aaron Fox","Tyrese Haliburton" ,"Richaun Holmes","Harrison Barnes" ,"Buddy Hield","Davion Mitchell",
"Karl-Anthony Towns","Anthony Edwards" ,
"D'Angelo Russell","Malik Beasley"]

    try:

            with st.spinner('Wait for it...'):

                data=get_day_records()
            st.success('Done!')
            st.balloons()

            data = data.sort_values(by='ttfl_points',ascending=False)

            data_top=data[data['ttfl_points']>=40]
            st.write("### Ils ont cartonné", data_top)

            data_boulot=data[data['ttfl_points'].between(31,39)]
            st.write("### Ils ont assuré", data_boulot)

            data_mieux=data[data['ttfl_points'].between(26,30)]
            data_mieux=data_mieux[data_mieux['Player'].isin(liste_player)]
            st.write("### C'est pas trop mal", data_mieux)

            data_pourri=data[data['ttfl_points'].between(16,25)]
            data_pourri=data_pourri[data_pourri['Player'].isin(liste_player)]

            st.write("### Un peu pourri quand même", data_pourri)


            data_carote=data[data['ttfl_points']<16]
            data_carote=data_carote[data_carote['Player'].isin(liste_player)]
            st.write("### Les belles carottes", data_carote)


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
