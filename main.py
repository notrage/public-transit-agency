#!/usr/bin/python3

try:
    import PySimpleGUI as sg
except:
    print("ATTENTION : vous n'avez pas la librairie PySimpleGUI")
    print("py -m pip install pysimplegui")
    exit()

from utils import db
from utils.requete import *
import os 

############################### GLOBAL VALUES ##################################
size=(400, 300)


def main_screen(conn:sqlite3.Connection):
    """
    Menu de base

    :param conn: Connexion à la base de données
    """
    layout = [  [sg.Button("Connexion en tant qu'Administrateur",size=(50,1))],
                [sg.Button("Connexion en tant qu'Utilisateur",size=(50,1))],
                [sg.Text("",size=(0,1))],
                [sg.Button("Quitter",size=(15,1),pad=((5,0), (155, 10)))]
            ]

    # Create the Window
    window = sg.Window('LOGIN', layout,size=size)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Quitter': # if user closes window or clicks cancel
            break
        if event == "Connexion en tant qu'Administrateur":
            window.hide()
            admin_panel(conn)
            window.UnHide()
        if event == "Connexion en tant qu'Utilisateur":
            window.hide()
            user_panel(conn)
            window.UnHide()
    window.close()

def admin_panel(conn:sqlite3.Connection):
    """
    Menu administrateur

    :param conn: Connexion à la base de données
    """
    # All the stuff inside your window.
    layout = [  [sg.Button("Visualiser une table",size=(50,1))],
                [sg.Button("Ajouter un conducteur",size=(50,1))],
                [sg.Button("Supprimer un conducteur",size=(50,1))],
                [sg.Button("Ajouter un véhicule",size=(50,1))],
                [sg.Button("Supprimer un véhicule",size=(50,1))],
                [sg.Button("Ajouter un arrêt",size=(50,1))],
                [sg.Button("Supprimer un arrêt",size=(50,1))],
                [sg.Button("Déconnexion",size=(15,1),pad=((5,0), (125, 10)))]
            ]
    window = sg.Window('ADMIN PANEL', layout,size=(400,400))
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Déconnexion': # if user closes window or clicks cancel
            break
        if event == "Ajouter un conducteur":
            window.Hide()
            Ajouter_un_conducteur(conn)
            window.UnHide()
        if event == "Supprimer un conducteur":
            window.Hide()
            relancer = Supprimer_une_valeur(conn,"Conducteurs")
            window.UnHide()
            while relancer:
                window.Hide()
                relancer = Supprimer_une_valeur(conn,"Conducteurs")
                window.UnHide()
        if event == "Ajouter un véhicule":
            window.Hide()
            Ajouter_un_vehicule(conn)
            window.UnHide()
        if event == "Supprimer un véhicule":
            window.Hide()
            relancer = Supprimer_une_valeur(conn,"Vehicules")
            window.UnHide()
            while relancer:
                window.Hide()
                relancer = Supprimer_une_valeur(conn,"Vehicules")
                window.UnHide()
        if event == "Ajouter un arrêt":
            window.Hide()
            Ajouter_un_arret(conn)
            window.UnHide()
        if event == "Supprimer un arrêt":
            window.Hide()
            relancer = Supprimer_une_valeur(conn,"Arrets")
            window.UnHide()
            while relancer:
                window.Hide()
                relancer = Supprimer_une_valeur(conn,"Arrets")
                window.UnHide()
        if event == "Visualiser une table":
            window.Hide()
            Afficher_table_menu(conn) 
            window.UnHide()  
    window.close()

def Afficher_table_menu(conn:sqlite3.Connection):
    """
    Menu d'affichage des tables de la DB

    :param conn: Connexion à la base de données
    """
    layout =  [[sg.Button("Conducteurs",size=(50,1))],
                [sg.Button("Modeles",size=(50,1))],
                [sg.Button("Tarifs",size=(50,1))],
                [sg.Button("Lignes",size=(50,1))],
                [sg.Button("Arrets",size=(50,1))],
                [sg.Button("Vehicules",size=(50,1))],
                [sg.Button("Etapes",size=(50,1))],
                [sg.Button("ConducteursModeles",size=(50,1))],
                [sg.Text("")],
                [sg.Button("Retour",size=(15,1),pad=((5,0), (70, 10)))]]
    window = sg.Window('ADMIN PANEL', layout,size=(400, 400))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Retour': # quit
            break
        elif event != None:
            requete = "SELECT * FROM " + event + ";"
            window.Hide()
            Afficher_table(conn,requete)
            window.UnHide()
    window.close()


def user_panel(conn:sqlite3.Connection):
    """
    Menu utilisateur

    :param conn: Connexion à la base de données
    """
    # All the stuff inside your window.
    layout = [  [sg.Button("...",size=(50,1))],
                [sg.Button("...",size=(50,1))],
                [sg.Button("...",size=(50,1))],
                [sg.Button("Déconnexion",size=(15,1),pad=((5,0), (150, 10)))]
            ]
    window = sg.Window('USER', layout,size=size)
        # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Déconnexion': # if user closes window or clicks cancel
            break
    window.close()


def main():
    # Nom de la BD à créer
    db_file = "data/transports.db"

    # Créer une connexion a la BD
    conn = db.creer_connexion(db_file)
    # initiation de la db 
    db.mise_a_jour_bd(conn,"data/transports_init.sql")
    db.mise_a_jour_bd(conn, "data/transports_mtag_values.sql")
    #db.mise_a_jour_bd(conn,"data/transports_init_values.sql")

    # theme des UI
    sg.theme('DarkAmber')
    
    main_screen(conn)
    conn.commit()
    print("Données mises à jour")
    conn.close()
    print("Connection fermée")


if __name__ == "__main__":
    main()

