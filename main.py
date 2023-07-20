import functions
import pandas as pd
import streamlit as st
import time


# answer = True
# while answer:

#Gather user inoput

st.title("Hello!")

title = st.text_input('Please enter the song title')

artist = st.text_input("Please enter artist name")


# with st.spinner("Waiting for song title and artist"):
# 	time.sleep(20)


#get id number

#if len(title)>0 & len(artist)>0:

df_results = functions.search_song(title, artist)



if type(df_results) == pd.DataFrame:

	st.dataframe(df_results[['titles', 'artists', 'album']])
	
	row_number = st.radio("Pick a number", [0,1,2,3,4])

	id_number = df_results.iloc[row_number]['id']

	df_selection = df_results.iloc[[row_number]]
	df_selection = df_selection[['id', 'titles', 'artists']]


	
	#get features
	features_df = functions.get_audio_features(id_number)


	#merge features to song title, id, artist
	song_with_features_df = functions.add_audio_features(df_selection, features_df)


	#scale


	#model predict cluster


















else:
	st.markdown("Sorry, your song wasn't found on Spotify")

	response = st.radio("Would you like to search for another song?", ["Yes, please", "No thanks"])

	if response == "Yes, please":
		answer = True

	else:
		answer = False

		st.markdown("OK, see you soon")






# Update user answer

