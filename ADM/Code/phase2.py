from math import exp, factorial
from random import randint, random
from enum import IntEnum
from functools import reduce
import sys
import pandas as pd

COUT_PRESENCE_SYSTEME_ORDI = 25 / 60
COUT_PRESENCE_SYSTEME_RELATIF = 35 / 60
COUT_PRESENCE_SYSTEME_ABSOLU = 45 / 60
COUT_OCCUPATION_ORDI = 30 / 60
COUT_OCCUPATION_PRIO = 32 / 60
COUT_INOCCUPATION = 18 / 60
COUT_PERTE_CLIENT_ORDI = 15
COUT_PERTE_CLIENT_PRIO = 20
V_PRIORITAIRE = 0.7
V_ORDINAIRE = 2
PROPORTION_ABSOLU = 0.3

class CoutsStation:
    def __init__(self):
        self.duree_occupation_absolu = 0
        self.duree_occupation_relatif = 0
        self.duree_occupation_ordinaire = 0 
        self.duree_inoccupation = 0 

class StatutClient(IntEnum):
    ORDINAIRE = 1
    RELATIF = 2
    ABSOLU = 3

class Client:
    def __init__(self, statut):
        self.statut = statut
        self.duree_traitement = 0
        self.duree_attente = 0

contient_client_statut = lambda clients, statut : any(map(lambda client : client.statut == statut, clients))
esperance = lambda Ci, ri : sum([x * y for x, y in zip(Ci, ri)]) / sum(ri)
nombre_stations_minimun = lambda 𝜆, DS: int((𝜆 * DS) + 1)

def dernier_client_statut(liste_clients, statut):
    index = 0

    while index < len(liste_clients) and liste_clients[index].statut == statut:
        index += 1

    return index

        
def loi_poisson(k, v):
    return (exp(-v) * (v**k)) / factorial(k)

def nombre_aleatoire(a, c, m, x0):
    return (a * x0 + c) % m

def generer_nb_arrivees(a, c, m, x0, v):
    x1 = nombre_aleatoire(a, c, m, x0)
    u1 = x1 / m
    x0 = x1
    k = 0
    probabilite = loi_poisson(k, v)
    while u1 >= probabilite:
        k += 1
        probabilite += loi_poisson(k, v)
    
    return (k, x0)

def duree_traitement(a, c, m, x0):
    x1 = nombre_aleatoire(a, c, m, x0)
    u1 = x1 / m
    proba = (2 / 62)
    if u1 < proba:
        duree_traitement = 6
    else:
        proba += (3 / 62)
        if u1 < proba:
            duree_traitement = 5
        else:
            proba += (4 / 62)
            if u1 < proba: 
                duree_traitement = 4
            else:
                proba += (11 / 62)
                if u1 < proba:
                    duree_traitement = 3
                else:
                    proba += (18 / 62)
                    if u1 < proba:
                        duree_traitement = 2
                    else:
                        duree_traitement = 1

    return (duree_traitement, x1)


def gestion_impatience(file, couts):
    pos_file = 1
    clients_perdus = []
    
    for client in file:
        client.duree_attente += 1

        if client.statut == StatutClient.ABSOLU:
            couts["duree_totale_client_absolu"] += 1
            couts["duree_file_client_absolu"] += 1
        elif client.statut == StatutClient.RELATIF:
            couts["duree_totale_client_relatif"] += 1
            couts["duree_file_client_relatif"] += 1
        else:
            couts["duree_totale_client_ordinaire"] += 1
            couts["duree_file_client_ordinaire"] += 1

        if client.duree_attente >= 10 and pos_file > 3:
            clients_perdus.append(client)
        pos_file += 1

    for client in clients_perdus:
        file.remove(client)

    return (couts, clients_perdus)

def nouveaux_clients(v_prioritaire, v_ordinaire, a, c, m, x0):
    clients = []

    nb_ordinaires, x0 = generer_nb_arrivees(a, c, m, x0, v_ordinaire)
    nb_prioritaires, x0 = generer_nb_arrivees(a, c, m, x0, v_prioritaire)
    nb_absolus = 0
    nb_relatifs = 0

    for i in range(nb_prioritaires):
        x1 = nombre_aleatoire(a, c, m, x0)
        x0 = x1
        u1 = x1 / m 
        if u1 < PROPORTION_ABSOLU:
            nb_absolus += 1
        else:
            nb_relatifs += 1
    
    nb_arrivees = nb_ordinaires + nb_relatifs + nb_absolus

    for i in range(nb_absolus):
        clients.append(Client(StatutClient.ABSOLU))
    for i in range(nb_relatifs):
        clients.append(Client(StatutClient.RELATIF))
    for i in range(nb_ordinaires):
        clients.append(Client(StatutClient.ORDINAIRE))

    return (clients, x0)

def gestion_file(file, clients):
    if contient_client_statut(file, StatutClient.ABSOLU):
        dernier_absolu = dernier_client_statut(file, StatutClient.ABSOLU)
    else:
        dernier_absolu = 0

    if contient_client_statut(file, StatutClient.RELATIF):
        dernier_relatif = dernier_client_statut(file, StatutClient.RELATIF)
    elif not contient_client_statut(file, StatutClient.ABSOLU):
        dernier_relatif = 0
    else:
        dernier_relatif = dernier_absolu + 1
    
    for client in clients:
        if client.statut == StatutClient.ABSOLU:
            file.insert(dernier_absolu, client)
            dernier_absolu += 1
            dernier_relatif += 1
        elif client.statut == StatutClient.RELATIF:
            file.insert(dernier_relatif, client)
            dernier_relatif += 1
        else:
            file.append(client)

def gestion_clients_prioritaire(stations, file, a, c, m, x0):
    clients_ejectes = []
    iClient = 0

    while iClient < len(file) and file[iClient].statut == StatutClient.ABSOLU:
        temps_traitement_max = -sys.maxsize - 1
        num_station_max = -1
        for station in stations:
            if station.statut is None:
                num_station_max = stations.index(station)
                break;
            if station.statut == StatutClient.ORDINAIRE and station.duree_traitement > temps_traitement_max:
                num_station_max = stations.index(station)
                temps_traitement_max = station.duree_traitement

        if num_station_max != -1:
            if stations[num_station_max].statut is not None:
                clients_ejectes.append(stations[num_station_max])
            stations[num_station_max] = file.pop(iClient)
            stations[num_station_max].duree_traitement, x0 = duree_traitement(a, c, m, x0)

        iClient += 1
    
    i_client_ejecte = 0
    for client in clients_ejectes:
        client.statut = StatutClient.ABSOLU
        file.insert(i_client_ejecte, client)
        i_client_ejecte += 1

def simulation_file_attente(v_prioritaire, v_ordinaire, a, c, m, x0, nb_stations_min, nb_stations_max, temps_simulation):
    cout_min = sys.maxsize
    nb_stations_optimal = nb_stations_min

    cout_station = {
            "duree_occupation_absolu" : 0,
            "duree_occupation_relatif" : 0,
            "duree_occupation_ordinaire" : 0,
            "duree_inoccupation" : 0,
        }

    for nb_stations in range(nb_stations_min, nb_stations_max + 1):
        couts = {
            "duree_totale_client_absolu" : 0,
            "duree_totale_client_ordinaire" : 0,
            "duree_totale_client_relatif" : 0,
            "duree_file_client_absolu" : 0,
            "duree_file_client_ordinaire" : 0,
            "duree_file_client_relatif" : 0,
            "duree_occupation_prio" : 0,
            "duree_occupation_ordi" : 0,
            "duree_inoccupation" : 0,
            "clients_prio_perdus" : 0,
            "clients_ordinaires_perdus" : 0,
        }

        couts_stations = [CoutsStation() for _ in range(nb_stations)]
        
        stations = [Client(None) for _ in range(nb_stations)]
        file = []

        for temps in range(temps_simulation):
            if temps % 20 == 0 and nb_stations == nb_stations_min:
                print("---TEMPS DE SIMULTATION : " + str(temps) + "---")
                print("---DEBUT DE MINUTE---")
                print()
                afficher_stations(stations)
                afficher_file(file)
                
            couts, clients_perdus = gestion_impatience(file, couts)
            
            for client in clients_perdus:
                if client.statut == StatutClient.ORDINAIRE:
                    couts["clients_ordinaires_perdus"] += 1
                else:
                    couts["clients_prio_perdus"] += 1
            
            clients, x0 = nouveaux_clients(v_prioritaire, v_ordinaire, a, c, m, x0)

            if temps % 20 == 0 and nb_stations == nb_stations_min:
                afficher_arrivees(clients)

            gestion_file(file, clients)
            gestion_clients_prioritaire(stations, file, a, c, m, x0)

            if temps % 20 == 0 and nb_stations == nb_stations_min:
                print("---FILE & STATIONS APRES PLACEMENT PRIO---")
                print()
                afficher_stations(stations)
                afficher_file(file)

            iStation = 0
            while iStation < nb_stations:
                if stations[iStation].statut is None:
                    if len(file) != 0:
                        traitement, x0 = duree_traitement(a, c, m, x0)
                        stations[iStation] = file.pop(0)
                        stations[iStation].duree_traitement = traitement - 1
                    else:
                        couts["duree_inoccupation"] += 1
                        couts_stations[iStation].duree_inoccupation += 1
                else:
                    stations[iStation].duree_traitement -= 1

                if stations[iStation].statut == StatutClient.ABSOLU:
                    couts["duree_totale_client_absolu"] += 1
                    couts["duree_occupation_prio"] += 1
                    couts_stations[iStation].duree_occupation_absolu += 1
                elif stations[iStation].statut == StatutClient.RELATIF:
                    couts["duree_totale_client_relatif"] += 1
                    couts["duree_occupation_prio"] += 1
                    couts_stations[iStation].duree_occupation_relatif += 1
                else:
                    couts["duree_totale_client_ordinaire"] += 1
                    couts["duree_occupation_ordi"] += 1
                    couts_stations[iStation].duree_occupation_ordinaire += 1

                if stations[iStation].duree_traitement == 0:
                    stations[iStation].statut = None

                iStation += 1
            
            if temps % 20 == 0 and nb_stations == nb_stations_min:
                print("---TEMPS DE SIMULTATION : " + str(temps) + "---")
                print("---FIN DE MINUTES---")
                print()
                afficher_stations(stations)
                afficher_file(file)

        cout_total = ((COUT_INOCCUPATION * couts["duree_inoccupation"]) + 
        (COUT_PERTE_CLIENT_ORDI * couts["clients_ordinaires_perdus"]) +
        (COUT_PERTE_CLIENT_PRIO * couts["clients_prio_perdus"]) + 
        (COUT_OCCUPATION_PRIO * couts["duree_occupation_prio"]) +
        (COUT_OCCUPATION_ORDI * couts["duree_occupation_ordi"]) +
        (COUT_PRESENCE_SYSTEME_ABSOLU * couts["duree_totale_client_absolu"]) +
        (COUT_PRESENCE_SYSTEME_RELATIF * couts["duree_totale_client_relatif"]) +
        (COUT_PRESENCE_SYSTEME_ORDI * couts["duree_totale_client_ordinaire"]))

        afficher_couts(couts, nb_stations, couts_stations, cout_total)

        if cout_min > cout_total:
            cout_min = cout_total
            nb_stations_optimal = nb_stations

    return nb_stations_optimal


def afficher_couts(couts, nb_stations, couts_stations, cout_total):
    print("Cout de la simulation avec " + str(nb_stations) + " stations")
    print("---" * 20)
    print()
    print("Cout total du systeme : " + str(cout_total))
    print()
    print("Les clients absolus en file ont coute : " + str(couts["duree_file_client_absolu"] * COUT_PRESENCE_SYSTEME_ABSOLU))
    print("Les clients relatif en file ont coute : " + str(couts["duree_file_client_relatif"] * COUT_PRESENCE_SYSTEME_RELATIF))
    print("Les clients ordinaire en file ont coute : " + str(couts["duree_file_client_ordinaire"] * COUT_PRESENCE_SYSTEME_ORDI))
    print()
    print("La perte de clients prioritaires a coute : " + str(couts["clients_prio_perdus"] * COUT_PERTE_CLIENT_PRIO))
    print("La perte de clients ordinaire a coute : " + str(couts["clients_ordinaires_perdus"] * COUT_PERTE_CLIENT_ORDI))
    print()
    cout_file = (
        couts["duree_file_client_absolu"] * COUT_PRESENCE_SYSTEME_ABSOLU + 
        couts["duree_file_client_relatif"] * COUT_PRESENCE_SYSTEME_RELATIF +
        couts["duree_file_client_ordinaire"] * COUT_PRESENCE_SYSTEME_ORDI +
        couts["clients_prio_perdus"] * COUT_PERTE_CLIENT_PRIO + 
        couts["clients_ordinaires_perdus"] * COUT_PERTE_CLIENT_ORDI
        )
    print("Le cout de la file est donc de : " + str(cout_file))
    print()
    print("Les couts pour chaque stations")
    print()
    for i in range(nb_stations):
        print("Station " + str(i + 1) + " : ")
        print("Cout pour les clients absolu : " + str(couts_stations[i].duree_occupation_absolu * COUT_OCCUPATION_PRIO))
        print("Cout pour les clients relatif : " + str(couts_stations[i].duree_occupation_relatif * COUT_OCCUPATION_PRIO))
        print("Cout pour les clients ordinaire : " + str(couts_stations[i].duree_occupation_ordinaire * COUT_OCCUPATION_ORDI))
        print("Cout inoccupation : " + str(couts_stations[i].duree_inoccupation * COUT_INOCCUPATION))
        print()

def afficher_arrivees(clients):
    i = 1
    print("---INFO NOUVELLES ARRIVeES---")
    print("Il y a " + str(len(clients)) + " clients qui viennent d'arriver.")
    for client in clients:
        statut_client = "ordinaire" if client.statut == StatutClient.ORDINAIRE else "absolu" if client.statut == StatutClient.ABSOLU else "relatif"
        print("---Client " + str(i) + "---")
        print("Statut du client :\t" + str(statut_client))
        print("-" * 20)
        print()
        i += 1

    print("-" * 30)
    print()


def afficher_stations(stations):
    i = 1
    print("---INFO STATIONS---")
    for station in stations:
        print("---Station " + str(i) + "---")
        if station.statut is None:
            print("Inocuppee")
        else:
            statut_client = "ordinaire" if station.statut == StatutClient.ORDINAIRE else "absolu" if station.statut == StatutClient.ABSOLU else "relatif"
            print("Statut du client :\t\t" + str(statut_client))
            print("Duree de service restante : \t" + str(station.duree_traitement))
            print("-" * 20)
            print()
        i += 1
    
    print("-" * 30)
    print()
   

def afficher_file(file):
    print("---INFO FILE---")
    i = 1
    if len(file) == 0:
        print("La file est vide")
    else:
        for client in file:
            print("---Client " + str(i) + "---")
            statut_client = "ordinaire" if client.statut == StatutClient.ORDINAIRE else "absolu" if client.statut == StatutClient.ABSOLU else "relatif"
            print("Statut du client :\t" + str(statut_client))
            print("Duree d'attente' : \t" + str(client.duree_attente))
            print("-" * 20)
            print()

            i += 1
    
    print("-" * 30)
    print()
    

if __name__ == "__main__":
    a = 121
    c = 789
    m = 15000
    x0 = 25
    Ci = [1,2,3,4,5,6]
    ri = [24,18,11,4,3,2]
    DS = esperance(Ci, ri)
    Ci = []
    ri = []
    for i in range(250):
        nb_arrivees_ordi, x0 = generer_nb_arrivees(a,c,m, x0, 2) 
        nb_arrivees_prio, x0 = generer_nb_arrivees(a,c,m, x0, 0.7)
        nb_arrivees = nb_arrivees_prio + nb_arrivees_ordi

        if nb_arrivees in Ci:
            i = Ci.index(nb_arrivees)
            ri[i] += 1
        else:
            Ci.append(nb_arrivees)
            ri.append(1)

    𝜆 = esperance(Ci, ri)
    nb_stations_optimal = simulation_file_attente(V_PRIORITAIRE,V_ORDINAIRE,a,c,m,x0,nombre_stations_minimun(𝜆, DS), 50, 600)

    print("Nombre de stations optimale : " + str(nb_stations_optimal))