import functions
import pandas as pd
import streamlit as st
import time
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans



#Gather user inoput

st.title("Hello!")

placeholder = st.empty()

title = st.text_input('Please enter the song title', value = "", key='1')

artist = st.text_input("Please enter artist name", value= "", key='2')

if (len(title)>0) and (len(artist)>0):

	df_results = functions.search_song(title, artist)

	if type(df_results) == pd.DataFrame:

		st.dataframe(df_results[['titles', 'artists', 'album']])

		
		row_number = st.multiselect("Pick a number", [0,1,2,3,4])

		if len(row_number) > 0:

			row_number = row_number[0]

			id_number = df_results.iloc[row_number]['id']
			id_list = []
			id_list.append(id_number)

			df_selection = df_results.iloc[[row_number]]
			df_selection = df_selection[['id', 'titles', 'artists']]

			
			# #get features
			features_df = functions.get_audio_features(id_list)


			# #merge features to song title, id, artist
			song_with_features_df = functions.add_audio_features(df_selection, features_df)



			#scale
			with open('scalers/scaler.pickle', "rb") as file:
			    scaler = pickle.load(file)

			numeric_features = song_with_features_df[['danceability', 'energy', 'acousticness', 'instrumentalness', 'tempo']]

			song_with_features_scaled =scaler.transform(numeric_features)

			song_with_features_scaled_df = pd.DataFrame(song_with_features_scaled, columns = numeric_features.columns)

			

			#model predict cluster

			with open('models/kmeans_13.pickle', "rb") as file:
			    kmeans = pickle.load(file)

			cluster = kmeans.predict(song_with_features_scaled_df)

			clustered_songs = pd.read_csv("data/clustered_songs.csv")

			hot_ids = clustered_songs[clustered_songs['dataset'] == 'H']['id'].tolist()


			
			if id_number in hot_ids:
				suggestion = clustered_songs[(clustered_songs['dataset'] == 'H') & (clustered_songs['cluster'] == cluster[0]) & ~(clustered_songs['id'] == id_number)]
				suggestion.reset_index(drop = True, inplace=True)
				st.markdown("Here are some songs to check out")
				st.write(suggestion[['titles', 'artists']].sample(5))

			else:
				suggestion = clustered_songs[(clustered_songs['dataset'] == 'N')& (clustered_songs['cluster'] == cluster[0]) & ~(clustered_songs['id'] == id_number)]
				suggestion.reset_index(drop = True, inplace=True)
				st.markdown("Here are some songs to check out")
				st.write(suggestion[['titles', 'artists']].sample(5))

			
			response = st.selectbox("Would you like to search for another song?", ['', "Yes, please", "No thanks"])

			if response == "Yes, please":
				st.markdown('Please enter a new song')

			elif response == "No thanks":
				st.markdown("OK, see you soon")




	else:
		st.markdown("Sorry, your song wasn't found on Spotify")








	# Update user answer

