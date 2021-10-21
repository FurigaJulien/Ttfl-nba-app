import streamlit as st
import pandas as pd
from get_player_records import *
from urllib.error import URLError
import pandas as pd
from get_player_records import *



def app():


    st.set_option('deprecation.showPyplotGlobalUse', False)


    try:

        col1, col2 = st.columns(2)

        with col1:
            with st.form('Les records des joueurs !'):
                player_name = st.text_input('Selectionnez un joueur')
                season_type = st.selectbox('Selectionnez un type de saison', ['Regular Season', 'Playoffs','Pre Season',"All Star"])
                best_worst = st.selectbox('Le meilleur ou le pire ?', ['Le meilleur',"Le pire"], key=2)
                nb_year = st.slider(label='Depuis combien de temps ?', min_value=1, max_value=40, key=4)
                submitted1 = st.form_submit_button('Rechercher')


        
        if submitted1:
            with col1:
                bar = st.progress(0)
                try :
                    for values,season,player_id in get_player_record(player_name,nb_year,season_type=season_type):
                        try :
                            data,season,player_id = values,season,player_id
                            
                            bar.progress(int((data+1)*100/nb_year))
                        except:
                            data,season,player_id = values,season,player_id


                    if best_worst == 'Le meilleur' :
                        st.write("Records TTFL :",data.sort_values('ttfl_points',ascending=False)[:30])
                        game_id = str(data.sort_values('ttfl_points',ascending=False)[:30].iloc[0]['Game ID'])
                        graph = get_player_best_match_graph(game_id,player_id)
                        st.pyplot(graph)

                    else :
                        st.write("Records TTFL :",data.sort_values('ttfl_points',ascending=True)[:30])
                        game_id = str(data.sort_values('ttfl_points',ascending=False)[:30].iloc[0]['Game ID'])
                        graph = get_player_best_match_graph(game_id,player_id)
                        st.pyplot(graph)



                except:
                        
                        st.error("Le joueur n'a pas pu être trouvé, désolé ! Verifiez peut être l'orthographe ! " )



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


