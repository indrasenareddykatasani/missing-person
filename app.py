import streamlit as st 
import pandas as pd
from utils import *
from mail import send_email


def app():
    
    
    st.title('Missing Person Identification System')

    tab1, tab2 = st.tabs(['Report', 'Find'])
    
    with tab1:
        st.header('Report a Missing Person here')
        
        name = st.text_input('Enter Name')
        date = st.date_input('Select date of Missing')
        contact_email = st.text_input('Enter E-Mail for contact')
        up_img = st.file_uploader('Upload the person image', type=['jpg', 'jpeg', 'png'])
        
        if st.button('Add Data'):
            with open('./database/data/details.json') as json_file:
                json_decoded = json.load(json_file)


            if up_img is not None:
                save_dir = f'./database/missing_persons/{name}.png'
                with open(save_dir, 'wb') as f:
                    f.write(up_img.read())
                    
                    
                json_decoded[name] = contact_email

                with open('./database/data/details.json', 'w') as json_file:
                    json.dump(json_decoded, json_file)
                    
                encode_folder()
                
                
                
                st.warning('Data Added Sucessfully')
                
                
    with tab2:
        st.header('Finding a Missing Person')
        
        if st.button('Start Camera'):
            match_status, name = detect()
            name = name.title()
            if match_status:
                st.warning('Match Found')
                
               
                
                try:
                    json_file = open('./database/data/details.json')
                    json_obj = json.load(json_file)
                    con_email = json_obj[name]
                    
                    lat, long = get_coordinates()
                    
                    send_email(name, (lat, long), con_email)
                    
                    json_file.close()
                    
                except:
                    print('Error Occured')
        
        
        
if __name__=='__main__':
    app()