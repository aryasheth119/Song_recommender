import functions
import pandas as pd
import streamlit as st
import time
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

answer = True
#while answer:

#Gather user inoput

st.title("Hello!")

title = st.text_input('Please enter the song title', value = "", key='1')

artist = st.text_input("Please enter artist name", value= "", key='2')

if (title is not None) and (artist is not None):
	# with st.spinner("Waiting for song title and artist"):
	# 	time.sleep(20)


	#get id number

	#if len(title)>0 & len(artist)>0:

	df_results = functions.search_song(title, artist)



	if type(df_results) == pd.DataFrame:

		st.dataframe(df_results[['titles', 'artists', 'album']])
		
		row_number = st.radio("Pick a number", [0,1,2,3,4])

		id_number = df_results.iloc[row_number]['id']
		id_list = []
		id_list.append(id_number)

		df_selection = df_results.iloc[[row_number]]
		df_selection = df_selection[['id', 'titles', 'artists']]

		#st.dataframe(df_selection)

		#st.write(id_list)
		
		# #get features
		features_df = functions.get_audio_features(id_list)

		#st.dataframe(features_df)


		# #merge features to song title, id, artist
		song_with_features_df = functions.add_audio_features(df_selection, features_df)

		#st.write(song_with_features_df)


		#scale
		with open('scalers/scaler.pickle', "rb") as file:
		    scaler = pickle.load(file)

		numeric_features = song_with_features_df[['danceability', 'energy', 'acousticness', 'instrumentalness', 'tempo']]

		song_with_features_scaled =scaler.transform(numeric_features)

		song_with_features_scaled_df = pd.DataFrame(song_with_features_scaled, columns = numeric_features.columns)

		#st.dataframe(song_with_features_scaled_df)



		#model predict cluster

		with open('models/kmeans_13.pickle', "rb") as file:
		    kmeans = pickle.load(file)

		cluster = kmeans.predict(song_with_features_scaled_df)

		st.write(cluster[0])

		clustered_songs = pd.read_csv("data/clustered_songs.csv")
		#st.write(clustered_songs)

		hot_ids = clustered_songs[clustered_songs['dataset'] == 'H']['id'].tolist()
		#st.write(hot_ids)
		
		if id_number in hot_ids:
			suggestion = clustered_songs[(clustered_songs['dataset'] == 'H') & (clustered_songs['cluster'] == cluster[0]) & ~(clustered_songs['id'] == id_number)]
			st.write(suggestion[['titles', 'artists']].sample(5))

		else:
			st.write('false')
			suggestion = clustered_songs[(clustered_songs['dataset'] == 'N')& (clustered_songs['cluster'] == cluster[0]) & ~(clustered_songs['id'] == id_number)]
			st.write(suggestion[['titles', 'artists']].sample(5))


	else:
		st.markdown("Sorry, your song wasn't found on Spotify")



	response = st.radio("Would you like to search for another song?", ["Yes, please", "No thanks"])

	if response == "Yes, please":
		answer = True

	else:
		answer = False

		
		st.markdown("OK, see you soon")




	# Update user answer

