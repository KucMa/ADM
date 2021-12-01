from math import exp, factorial
from random import randint
from enum import IntEnum
import sys

class StatusClient(IntEnum):
    ORDINAIRE = 1
    RELATIF = 2
    ABSOLU = 3

class Client:
    def __init__(self, status):
        self.status = status
        self.durée_traitement = None
        self.durée_attente = 0
        
def loi_poisson(k, v):
    return (exp(-v) * (v**k)) / factorial(k)

def nombre_aléatoire(a, c, m, x0):
    return (a * x0 + c) % m

def générer_nb_arrivées(a, c, m, x0, v):
    x1 = nombre_aléatoire(a, c, m, x0)
    u1 = x1 / m
    x0 = x1
    k = 1
    probabilité = loi_poisson(0, v)
    while u1 >= probabilité:
        probabilité += loi_poisson(k, v)
        k += 1
    
    return k - 1

def durée_traitement(a, c, m, x0):
    x1 = nombre_aléatoire(a, c, m, x0)
    u1 = x1 / m
    proba = (2 / 62)
    if u1 < proba:
        durée_traitement = 6
    else:
        proba += (3 / 62)
        if u1 < proba:
            durée_traitement = 5
        else:
            proba += (4 / 62)
            if u1 < proba: 
                durée_traitement = 4
            else:
                proba += (11 / 62)
                if u1 < proba:
                    durée_traitement = 3
                else:
                    proba += (18 / 62)
                    if u1 < proba:
                        durée_traitement = 2
                    else:
                        durée_traitement = 1

    return (durée_traitement, x1)


def gestion_impatience(file, durée_totale_client_ordinaire, durée_totale_client_absolu, durée_totale_client_relatif):
    pos_file = 1
    
    for client in file:
        client.duréeAttente += 1

        if client.status == "ORDINAIRE":
            durée_totale_client_ordinaire += 1
        elif client.status == "RELATIF":
            durée_totale_client_relatif += 1
        else:
            durée_totale_client_absolu += 1

        if client.duréeAttente >= 10 and pos_file > 3:
            file.remove(client)
        pos_file += 1

def nouveaux_clients(v_prioritaire, v_ordinaire, a, c, m, x0):
    clients = []

    nb_ordinaires, x0 = générer_nb_arrivées(a, c, m, x0, v_ordinaire)
    nb_prioritaires, x0 = générer_nb_arrivées(a, c, m, x0, v_prioritaire)
    nb_absolus = int(nb_prioritaires * .3)
    nb_relatifs = nb_prioritaires - nb_absolus
    nb_arrivées = nb_ordinaires + nb_relatifs + nb_absolus

    for i in range(len(nb_absolus)):
        clients.append(Client(StatusClient.ABSOLU))
    for i in range(len(nb_relatifs)):
        clients.append(Client(StatusClient.RELATIF))
    for i in range(len(nb_ordinaires)):
        clients.append(Client(StatusClient.ORDINAIRE))

    return (clients, nb_arrivées, x0)

def gestion_file(file, clients):
    dernier_absolu = len(file) - 1 - file[::-1].index(StatusClient.ABSOLU)
    dernier_relatif = len(file) - 1 - file[::-1].index(StatusClient.RELATIF)
    
    for client in clients:
        if client.status == StatusClient.ABSOLU:
            dernier_absolu += 1
            dernier_relatif += 1
            file.insert(client, dernier_absolu)
        elif client.status == StatusClient.RELATIF:
            dernier_relatif += 1
            file.insert(client, dernier_relatif)
        else:
            file.append(client)

def gestion_clients_prioritaire(stations, file, a, c, m, x0):
    clients_éjectés = []
    iClient = 0

    while iClient < len(file and file[iClient].status == StatusClient.ABSOLU):
        temps_traitement_max = sys.maxsize
        num_station_max = -1
        for station in stations:
            if station.status == StatusClient.ORDINAIRE and station.durée_traitement > temps_traitement_max:
                num_station_max = stations.index(station)
                temps_traitement_max = station.durée_traitement

        if num_station_max != -1:
            clients_éjectés.append(stations[num_station_max])
            stations[num_station_max] = file[iClient]
            stations[num_station_max].durée_traitement, x0 = durée_traitement(a, c, m, x0)

        iClient += 1
    
    i_client_éjecté = 0
    for client in clients_éjectés:
        file.insert(client, i_client_éjecté)
