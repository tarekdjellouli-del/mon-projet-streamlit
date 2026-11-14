
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#  TITRE DU DASHBOARD

st.title("✈️ Dashboard - Analyse du trafic aérien")

st.write("Explorez l'évolution du nombre de passagers ""entre 1949 et 1960.")

#  CHARGEMENT DES DONNÉES
@st.cache_data
def charger_donnees():

    url = ("https://raw.githubusercontent.com/""mwaskom/seaborn-data/master/flights.csv")

    df = pd.read_csv(url)

    return df


df = charger_donnees()



#FILTRE SUR LES ANNÉES

st.subheader("🔎 Filtrer les données")

annee_min = int(df["year"].min())
annee_max = int(df["year"].max())

annees = st.slider(
    "Sélectionnez une plage d'années :",
    min_value=annee_min,
    max_value=annee_max,
    value=(annee_min, annee_max),
    step=1
)


# FILTRE SUR LES MOIS


ordre_mois = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

mois_disponibles = ["Tous les mois"] + ordre_mois

mois_selectionne = st.selectbox(
    "Choisissez un mois :",
    mois_disponibles
)

#  FILTRAGE DU DATAFRAME

df_filtre = df[
    (df["year"] >= annees[0]) &
    (df["year"] <= annees[1])
]

if mois_selectionne != "Tous les mois":

    df_filtre = df_filtre[
        df_filtre["month"] == mois_selectionne
    ]

# INDICATEURS KPI

st.subheader("📊 Indicateurs clés")

total_passagers = df_filtre["passengers"].sum()

st.metric(
    label="Nombre total de passagers",
    value=f"{total_passagers:,}".replace(",", " ")
)

st.metric(
    label="Nombre de périodes mensuelles",
    value=len(df_filtre)
)



#  GRAPHIQUE D'ÉVOLUTION

st.subheader("📈 Évolution du nombre de passagers")

mode_graphique = st.radio(
    "Choisissez l'affichage du graphique :",
    ["Tous les mois", "Un mois par année"],
    horizontal=True
)


# Dictionnaire pour convertir les mois en numéros

ordre_mois_num = {
    mois: numero
    for numero, mois in enumerate(ordre_mois, start=1)
}


if mode_graphique == "Tous les mois":

    # Conversion des mois en numéros

    evolution = df_filtre.copy()

    evolution["mois_num"] = evolution["month"].map(
        ordre_mois_num
    )

    # Création d'une vraie date

    evolution["date"] = pd.to_datetime(
        dict(
            year=evolution["year"],
            month=evolution["mois_num"],
            day=1
        )
    )

    # Tri chronologique

    evolution = evolution.sort_values("date")

    # Affichage du graphique

    st.line_chart(
        evolution.set_index("date")["passengers"],
        y_label="Nombre de passagers",
        x_label="Date"
    )


else:

    # Choix du mois à comparer

    mois_graphique = st.selectbox(
        "Sélectionnez le mois à comparer :",
        ordre_mois
    )

    # Filtrage du mois sélectionné

    evolution = df[
        (df["year"] >= annees[0]) &
        (df["year"] <= annees[1]) &
        (df["month"] == mois_graphique)
    ].sort_values("year")

    # Affichage du graphique

    st.line_chart(
    evolution.assign(
        year=evolution["year"].astype(str)
    ).set_index("year")["passengers"],
    y_label="Nombre de passagers",
    x_label="Année"
)
    


#  HEATMAP SEABORN

st.subheader("🌡️ Répartition des passagers")

afficher_heatmap = st.checkbox(
    "Afficher la Heatmap de répartition des passagers"
)

if afficher_heatmap:

    # Création du tableau croisé

    df_pivot = df_filtre.pivot(
        index="month",
        columns="year",
        values="passengers"
    )

    # Respecter l'ordre chronologique des mois

    df_pivot = df_pivot.reindex(ordre_mois)

    # Création de la figure

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.heatmap(
        df_pivot,
        annot=True,
        fmt=".0f",
        cmap="YlOrRd",
        linewidths=0.5,
        ax=ax
    )

    ax.set_title(
        "Nombre de passagers par année et par mois"
    )

    ax.set_xlabel("Années")
    ax.set_ylabel("Mois")

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)

#  AFFICHAGE DU TABLEAU DE DONNÉES

st.subheader("📋 Données filtrées")

st.write(
    f"Période sélectionnée : "
    f"{annees[0]} - {annees[1]}"
)

st.write(
    f"Nombre de lignes : {len(df_filtre)}"
)

st.dataframe(
    df_filtre,
    use_container_width=True
)
