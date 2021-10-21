import streamlit as st
import pandas as pd
from get_player_records import *
from urllib.error import URLError
import pandas as pd
from get_special_records import *



def app():


    st.set_option('deprecation.showPyplotGlobalUse', False)


    try:




        with st.form('Les records des joueurs !'):
            special_day = st.selectbox('Quelle date ?', ["Opening night","Christmas day","MLK day","Closing night"], key=2)
            best_worst = st.selectbox('Le meilleur ou le pire ?', ['Le meilleur',"Le pire"], key=2)
            nb_year = st.slider(label='Depuis combien de temps ?', min_value=1, max_value=40, key=4)
            submitted1 = st.form_submit_button('Rechercher')


        
        if submitted1:

            bar = st.progress(0)
            try :

                with st.spinner('Les requetes sont plutot longues, si tu as demandé plus de 15 ans, tu peux aller te faire un petit café !'):

                    for values in get_special_dates_records(special_day,nb_year):
                        try :
                            data = values
                            bar.progress(int((data+1)*100/nb_year))
                        except:
                            data = values


                    if best_worst == 'Le meilleur' :
                        st.write("Records TTFL :",data.sort_values('ttfl_points',ascending=False)[:30])



                    else :
                        st.write("Records TTFL :",data.sort_values('ttfl_points',ascending=True)[:30])





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



