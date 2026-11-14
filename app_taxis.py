import streamlit as st
import pandas as pd
# Titre principal de la page
st.title("Dashboard Analyse Taxis - DJELLOULI Tarek")
taxis = pd.read_csv("taxis.csv")

quartiers = sorted(
    taxis["pickup_borough"].dropna().unique())

#  Créer le menu déroulant
pickup_borough = st.selectbox("Choisissez un quartier de prise en charge",quartiers)

#Filtrer le DataFrame
df_filtre = taxis[taxis["pickup_borough"] == pickup_borough]

#  Afficher les résultats
st.write("Quartier sélectionné :",   pickup_borough)
st.dataframe(df_filtre.head(5))
# Calculer le nombre total de courses
nb_courses = len(df_filtre)

# Afficher la métrique
st.metric(label="Nombre total de courses",value=nb_courses)