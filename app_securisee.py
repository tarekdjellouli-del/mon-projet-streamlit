
import streamlit as st
import pandas as pd
from pathlib import Path
from streamlit_option_menu import option_menu

FICHIER_COMPTES = Path(__file__).parent / "accounts.csv"

#  GESTION DES COMPTES UTILISATEURS

def charger_comptes():

    comptes = pd.read_csv(
        FICHIER_COMPTES,
        sep=";",
        dtype={"nom": str, "mot de passe": str, "email": str })
    return comptes

def sauvegarder_comptes(comptes):

    comptes.to_csv( FICHIER_COMPTES, sep=";", index=False, encoding="utf-8-sig" )

#  FONCTION DE CONNEXION

def connecter_utilisateur(username, password):

    try:
        comptes = charger_comptes()

        # Vérifier que les colonnes nécessaires existent
        colonnes_requises = [
            "nom",
            "mot de passe",
            "failed_login_attempts",
            "logged_in"
        ]

        if not all(col in comptes.columns for col in colonnes_requises):
            return False

        # Rechercher l'utilisateur
        utilisateur = comptes[comptes["nom"] == username]

        # Si le nom d'utilisateur n'existe pas
        if utilisateur.empty:
            return False

        index = utilisateur.index[0]

        # Vérifier le mot de passe
        if comptes.loc[index, "mot de passe"] == password:

            comptes.loc[index, "failed_login_attempts"] = 0
            comptes.loc[index, "logged_in"] = True

            sauvegarder_comptes(comptes)

            return True

        else:

            comptes.loc[index, "failed_login_attempts"] += 1

            sauvegarder_comptes(comptes)

            return False

    except Exception:
        return False

#  FONCTION DE DÉCONNEXION

def deconnecter_utilisateur(username):

    comptes = charger_comptes()

    utilisateur = comptes[comptes["nom"] == username]

    if not utilisateur.empty:

        index = utilisateur.index[0]

        comptes.loc[index, "logged_in"] = False

        sauvegarder_comptes(comptes)

#  INITIALISATION DE LA SESSION

if "authentifie" not in st.session_state:

    st.session_state.authentifie = False

if "username" not in st.session_state:

    st.session_state.username = None

#  PAGE DE CONNEXION OBLIGATOIRE

if not st.session_state.authentifie:

    st.title("🔐 Connexion à l'application")

    st.write("Veuillez vous identifier pour accéder à l'application.")

    with st.form("formulaire_connexion"):

        username = st.text_input("Nom d'utilisateur")

        password = st.text_input( "Mot de passe",type="password" )

        connexion = st.form_submit_button("Se connecter")

    # Vérification des identifiants
    if connexion:

        if connecter_utilisateur(username.strip(), password):

            st.session_state.authentifie = True
            st.session_state.username = username.strip()

            st.rerun()

        else:

            st.error("Nom d'utilisateur ou mot de passe incorrect.")

    # Bloquer l'accès aux autres pages
    st.stop()

#  BARRE LATÉRALE ET NAVIGATION

username = st.session_state.username

with st.sidebar:

    st.markdown(
    f"""
    <div style="font-size:24px; font-weight:bold; color:#218838;">
        👋 Bienvenue {username} 👋
    </div>
    """,
    unsafe_allow_html=True
)

    choix = option_menu( menu_title="Navigation", options=[ "Accueil", "Galerie Photos" ], icons=[ "house", "images" ],  menu_icon="cast", default_index=0,orientation="vertical"
    )

    # Bouton de déconnexion
    if st.button(
        "Se déconnecter",
        use_container_width=True
    ):

        deconnecter_utilisateur(username)

        st.session_state.authentifie = False

        st.session_state.username = None

        st.rerun()


#  PAGE ACCUEIL


if choix == "Accueil":

    st.title("🐱 Accueil 🐱")

    st.subheader(f"Bienvenue {username} !")

    st.write(""" Vous êtes connecté à l'application sécurisée, 
    utilisez le menu latéral pour naviguer entre les différentes pages de l'application. """ )
    st.write(""" Accès déconseillé aux personnes allergiques aux poils de chat. 🐱 """ )
#  PAGE GALERIE PHOTOS

elif choix == "Galerie Photos":

    st.title("🐱 Galerie Photos")
    st.write("Découvrez notre galerie de chats.")

    # Liste des photos
    photos = [
        ("Chat 1", "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=700"),
        ("Chat 2", "https://images.unsplash.com/photo-1518791841217-8f162f1e1131?w=700"),
        ("Chat 3", "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=700"),
   
    ]

    # Création de 3 colonnes fixes
    col1, col2, col3 = st.columns(3)

    # Affichage des photos dans les 3 colonnes
    for i, (nom, url) in enumerate(photos):

        if i % 3 == 0:
            with col1:
                st.image(url, caption=nom, use_container_width=True)

        elif i % 3 == 1:
            with col2:
                st.image(url, caption=nom, use_container_width=True)

        else:
            with col3:
                st.image(url, caption=nom, use_container_width=True)
