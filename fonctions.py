from datetime import datetime
from array import array
from ctypes.wintypes import PLARGE_INTEGER
from logging import logProcesses
import time
from discord.ext import commands
from operator import index
import requests
import gspread
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json

Decalage_horaire = 2


class user_config:
    def __init__(self, user_id, session_id):
        self.user_id = user_id
        self.session_id = session_id

    def _url(self):
        return 'https://channel-live.thor.snowprintstudios.com/events/lp/userId/{}/sessionId/{}'.format(
            self.user_id, self.session_id)

    def _url2(self):
        return 'https://api-live.thor.snowprintstudios.com/player/player2/userId/{}/sessionId/{}'.format(
            self.user_id, self.session_id)


guild_id = "6158edb1-e2dc-4412-9c5f-a4108e1a85a2"
buildmulti = "966540a51d7fc589b2c37a404dadaef0"
install = "63da37e2-940e-4fc1-b379-d072078c4e22"
gameversion = "828E1D67692F16DBA7A9500E48321C65"
multiconfigversion = "ae55e8b002a401766a0d89b21226bc48"
universe = "52AB1265BA18205FFD9D57B2274317D8"

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'services.json'
creds = None
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SAMPLE_SPREADSHEET_ID = "1rek_sc9er3S-YteHy3MzrM-9elLXf3lpDCDV2l1rbAI"
service = build('sheets', 'v4', credentials=creds)

PLAYER_2 = {
    "builtInMultiConfigVersion": buildmulti,
    "installId": install,
    "playerEvent": {
        "createdOn": str(int(time.time()*1000)),
        "gameConfigVersion": gameversion,
        "multiConfigVersion": multiconfigversion,
        "playerEventData": {},
        "playerEventType": "GET_PLAYER_2",
        "universeVersion": universe
    }
}

recupourguild = {
    "builtInMultiConfigVersion": buildmulti,
    "installId": install,
    "playerEvent": {
        "createdOn": str(int(time.time()*1000)),
        "gameConfigVersion": gameversion,
        "multiConfigVersion": multiconfigversion,
        "playerEventData": {
            "guildId": guild_id
        },
        "playerEventType": "VIEW_GUILD_2",
        "universeVersion": universe
    }
}


def Dic_boss(niveau) -> dict:
    niv = str(niveau)
    return {"01_001_v3": ["Logar", niv, "commun"],
            "01_002_v3": ["Kolger", niv, "commun"],
            "01_003_v3": ["Eldar", niv, "commun"],
            "02_001_v3": ["Skari", niv, "rare"],
            "02_002_v3": ["Harborr", niv, "rare"],
            "02_003_v3": ["Gormr", niv, "rare"],
            "03_001_v3": ["Lokvar", niv, "epique"],
            "03_002_v3": ["Tolir", niv, "epique"],
            "03_003_v3": ["Arnulf", niv, "epique"],
            "04_001_v3": ["Angar", niv, "legendaire"],
            "04_002_v3": ["Verkir", niv, "legendaire"],
            "04_003_v3": ["Eitri", niv, "legendaire"],
            "04_004_v3": ["Pyntir", niv, "legendaire"],
            "05_001_v3": ["Hatur", niv, "mythique"],
            "05_002_v3": ["Halfar", niv, "mythique"],
            "05_003_v3": ["Smanir", niv, "mythique"],
            "05_004_v3": ["Golur", niv, "mythique"]
            }


Dic_boss_guild = {"01_001_v3": ["Logar", "commun"],
                  "01_002_v3": ["Kolger", "commun"],
                  "01_003_v3": ["Eldar", "commun"],
                  "02_001_v3": ["Skari", "rare"],
                  "02_002_v3": ["Harborr", "rare"],
                  "02_003_v3": ["Gormr", "rare"],
                  "03_001_v3": ["Lokvar", "epique"],
                  "03_002_v3": ["Tolir", "epique"],
                  "03_003_v3": ["Arnulf", "epique"],
                  "04_001_v3": ["Angar", "legendaire"],
                  "04_002_v3": ["Verkir", "legendaire"],
                  "04_003_v3": ["Eitri", "legendaire"],
                  "04_004_v3": ["Pyntir", "legendaire"],
                  "05_001_v3": ["Hatur", "mythique"],
                  "05_002_v3": ["Halfar", "mythique"],
                  "05_003_v3": ["Smanir", "mythique"],
                  "05_004_v3": ["Golur", "mythique"]
                  }


def chats(name):
    return {
        "channels": [
            {
                "name": name,
                "seq": 0
            }
        ],
        "gameConfigVersion": gameversion,
        "multiConfigVersion": multiconfigversion
    }


def motsuivant(phrase, mot):
    phr = str(phrase)
    mo = str(mot)
    deb = phr.index(mo)
    phr = phr[deb:]
    deb = phr.index(":")
    try:
        fin = phr.index(",")
    except:
        fin = phr.index("}")
    res = phr[deb+1:fin]
    if res[0] == '"':
        res = res[1:]
        res = res[:-1]
    return res


def dateheure(tmps):
    annee = 1970
    tmps = int(tmps)+2*3600*1000
    while (tmps > 365*24*3600*1000 and annee % 4 != 0) or (tmps > 366*24*3600*1000 and (annee % 4 == 0)):
        if annee % 4 == 0:
            tmps = tmps-366*24*3600*1000
            annee += 1
        else:
            tmps = tmps-365*24*3600*1000
            annee += 1
    jour = tmps//(24*3600000)
    tmps = tmps-jour*24*3600000
    if annee % 4 != 0:
        if jour < 31:
            mois = "janvier"
        elif jour < 31+28:
            mois = "février"
            jour = jour-30
        elif jour < 31+28+31:
            mois = 'mars'
            jour = jour-30-28
        elif jour < 31+28+31+30:
            mois = 'avril'
            jour = jour-30-28-31
        elif jour < 31+28+31+30+31:
            mois = 'mai'
            jour = jour-30-28-31-30
        elif jour < 31+28+31+30+31+30:
            mois = 'juin'
            jour = jour-30-28-31-30-31
        elif jour < 31+28+31+30+31+30+31:
            mois = 'juillet'
            jour = jour-30-28-31-30-31-30
        elif jour < 31+28+31+30+31+30+31+31:
            mois = 'aout'
            jour = jour-30-28-31-30-31-30-31
        elif jour < 31+28+31+30+31+30+31+31+30:
            mois = 'septembre'
            jour = jour-30-28-31-30-31-30-31-31
        elif jour < 31+28+31+30+31+30+31+31+30+31:
            mois = 'octobre'
            jour = jour-30-28-31-30-31-30-31-31-30
        elif jour < 31+28+31+30+31+30+31+31+30+31+30:
            mois = 'novembre'
            jour = jour-30-28-31-30-31-30-31-31-30-31
        elif jour < 31+28+31+30+31+30+31+31+30+31+30+31:
            mois = 'decembre'
            jour = jour-30-28-31-30-31-30-31-31-30-31-30
    else:
        if jour < 31:
            mois = "janvier"
        elif jour < 31+29:
            mois = "février"
            jour = jour-30
        elif jour < 31+29+31:
            mois = 'mars'
            jour = jour-30-28
        elif jour < 31+29+31+30:
            mois = 'avril'
            jour = jour-30-28-31
        elif jour < 31+29+31+30+31:
            mois = 'mai'
            jour = jour-30-28-31-30
        elif jour < 31+29+31+30+31+30:
            mois = 'juin'
            jour = jour-30-28-31-30-31
        elif jour < 31+29+31+30+31+30+31:
            mois = 'juillet'
            jour = jour-30-28-31-30-31-30
        elif jour < 31+29+31+30+31+30+31+31:
            mois = 'aout'
            jour = jour-30-28-31-30-31-30-31
        elif jour < 31+29+31+30+31+30+31+31+30:
            mois = 'septembre'
            jour = jour-30-28-31-30-31-30-31-31
        elif jour < 31+29+31+30+31+30+31+31+30+31:
            mois = 'octobre'
            jour = jour-30-28-31-30-31-30-31-31-30
        elif jour < 31+29+31+30+31+30+31+31+30+31+30:
            mois = 'novembre'
            jour = jour-30-28-31-30-31-30-31-31-30-31
        elif jour < 31+29+31+30+31+30+31+31+30+31+30+31:
            mois = 'decembre'
            jour = jour-30-29-31-30-31-30-31-31-30-31-30
    heure = tmps//3600000
    tmps = tmps-heure*3600000
    if heure < 10:
        heure = str(heure)
        heure = "0"+heure
    minute = tmps//60000
    tmps = tmps-minute*60000
    if minute < 10:
        minute = str(minute)
        minute = "0"+minute
    seconde = tmps//1000
    if seconde < 10:
        seconde = str(seconde)
        seconde = "0"+seconde

    return "le {} {} {} à {}:{}:{}".format(jour, mois, annee, heure, minute, seconde)


def lireattaqueclash(reponse, dic):
    reponse = str(reponse)
    data = [[]]
    i = 0
    maxattaque = reponse.count("type")
    while i < maxattaque-1:
        data.append([])
        i += 1
    i = 0

    while i < maxattaque:
        findtype = reponse.index("type")
        reponse = reponse[findtype+4:]
        try:
            test = reponse.index("GUILD_CHALLENGE_ENCOUNTER_ENDED_EVENT")
        except:
            test = 0
        if test == 3:
            try:
                test = reponse.index("currentHp")
            except:
                test = 500

            if test < 450:
                data[i].append("defaite")
                data[i].append(motsuivant(reponse, "timestamp"))
                try:
                    data[i].append(
                        dic[motsuivant(reponse, "enemyUserId")])
                except:
                    data[i].append(motsuivant(reponse, "enemyUserId"))
                data[i].append(motsuivant(reponse, "winningTeam"))
                data[i].append(motsuivant(reponse, "currentHp"))
                data[i].append(motsuivant(reponse, "damage"))
                data[i].append(motsuivant(
                    reponse, "defensiveFortificationDamage"))
                data[i].append(motsuivant(reponse, "userId"))
                data[i].append(motsuivant(reponse, "displayName"))
            else:
                data[i].append("victoire")
                data[i].append(motsuivant(reponse, "timestamp"))
                try:
                    data[i].append(
                        dic[motsuivant(reponse, "enemyUserId")])
                except:
                    data[i].append(motsuivant(reponse, "enemyUserId"))
                data[i].append(motsuivant(reponse, "winningTeam"))
                data[i].append(motsuivant(
                    reponse, "defensiveFortificationDamage"))
                data[i].append(motsuivant(reponse, "userId"))
                data[i].append(motsuivant(reponse, "displayName"))
        else:
            data[i].append("open")
            data[i].append("lancement d'une attaque ...")
        i += 1
    return data


def guildmakedic(reponse, ajust) -> dict:
    rep = str(reponse)
    # ajust=1 pour allié 0 pour ennemi
    nbmember = rep.count("displayName")-ajust
    dic = {}
    i = 0
    while i < nbmember:
        dic[motsuivant(rep, "userId")] = motsuivant(
            rep, "displayName")
        deb = rep.index("level")
        rep = rep[deb+15:]
        i += 1
    return dic


def recupduelpower(reponse) -> dict:
    rep = str(reponse)
    deb = rep.index("encounterSetId")
    rep = rep[deb+100:]
    nbmember = rep.count("encounterSetId")
    deb = rep.index("encounterSetId")
    rep = rep[deb-15:]
    tab = []
    i = 0
    while i < nbmember:
        powers = []
        j = 0
        while j < 3:
            powers.append(motsuivant(
                rep, "duelPower"))
            deb = rep.index("duelPower")
            rep = rep[deb+30:]
            j += 1
        tab.append(powers)
        try:
            deb = rep.index("encounterSetId")
            rep = rep[deb-15:]
        except:
            pass
        i += 1
    return tab


def recupguilboss(reponse, boostend=0):
    # 0temps #1bomboucombat #2cible #3degat #4hprestant #5membre #6nomboss #seq #bonuspourattaque
    rep = str(reponse)
    data = [[]]
    maxdata = rep.count("GuildBossEncounterCompleted")
    i = 0
    while i < maxdata-1:
        data.append([])
        i += 1
    i = 0
    while i < maxdata:
        if motsuivant(rep, 'type') == "GuildBossEncounterCompleted":
            data[i].append(motsuivant(rep, "timestamp"))
            if motsuivant(rep, "damageType") == "Battle":
                data[i].append('Combat')
            else:
                data[i].append('Bombe')
            data[i].append(motsuivant(rep, "guildBossEncounterType"))
            data[i].append(motsuivant(rep, "damageDealt"))
            data[i].append(motsuivant(rep, "currentHp"))
            data[i].append(motsuivant(rep, "displayName"))
            data[i].append("{} ({})".format(Dic_boss_guild[motsuivant(
                rep, "levelId")[-9:]][0], Dic_boss_guild[motsuivant(rep, "levelId")[-9:]][1]))
            data[i].append(motsuivant(rep, "seq")[:6])
            if int(motsuivant(rep, "timestamp")) < int(boostend) and motsuivant(rep, "damageType") == "Battle":
                data[i].append(70)
            elif motsuivant(rep, "damageType") == "Battle":
                data[i].append(50)
            i += 1
        deb = rep.index("seq")
        rep = rep[deb+5:]
    return data


def TimeThisMorning() -> int:
    now = int(time.time())
    actualhour = (now-(7-Decalage_horaire)*3600) % (24*3600)
    return (now-actualhour)*1000


def bombesrestantes(reponse, tabj):
    log = recupguilboss(reponse)
    joueurs = tabj
    bombes = len(joueurs)
    limittime = TimeThisMorning()
    for logs in log:
        if logs[1] == 'Bombe' and int(logs[0]) > limittime:
            joueurs.remove(logs[5])
            bombes -= 1
    return [bombes, joueurs]


def attaquesrestantes(reponse, tabatt, nbjoueur):
    log = recupguilboss(reponse)
    total = nbjoueur*2
    joueurs = tabatt
    limittime = TimeThisMorning()
    for logs in log:
        if "Combat" in logs[1] and int(logs[0]) > limittime:
            for joueur in joueurs:
                if joueur[0] == logs[5]:
                    total -= 1
                    if joueur[1] == 1:
                        joueurs.remove(joueur)
                    else:
                        joueur[1] -= 1
    return [total, joueurs]


def liremessageguildechat(reponse):
    reponse = str(reponse)
    data = [[]]
    deb = reponse.index("[")
    fin = reponse.index(']')
    reponse = reponse[deb:fin+1]
    i = 0
    max = reponse.count('sourceUser')
    while i < max-1:
        data.append([])
        i += 1
    i = 0
    while i < max:
        data[i].append(motsuivant(reponse, 'displayName'))
        data[i].append(motsuivant(reponse, 'timestamp'))
        data[i].append(motsuivant(reponse, 'content'))
        fin = reponse.index('seq')
        reponse = reponse[fin+10:]
        i += 1
    return data


def recuperer_clashID_ennemyguildID(player2) -> array:
    data = str(player2)
    clashID = motsuivant(data, "guildChallengeId")
    ennemyguildID = clashID[8:]
    deb = ennemyguildID.index("_")
    ennemyguildID = ennemyguildID[deb+1:]
    fin = ennemyguildID.index("_")
    ennemyguildID = ennemyguildID[:fin]
    return [clashID, ennemyguildID]


def ClashDispo() -> bool:
    now = time.time()
    diffwithJeudi = (now - (24+16-Decalage_horaire)*3600) % (7*24*3600)
    debutclash = (now-diffwithJeudi)*1000
    finclash = debutclash+(24*3)*3600*1000
    if debutclash < now*1000 < finclash:
        return True
    else:
        return False


def TimeStampDebutSaison() -> array:
    now = time.time()
    # Temps qui nous separe du lundi précedent, 4 jours entre lundi et jeudi (4*24*3600 en seconde)
    jouractuelle = (now+24*3600-(7-Decalage_horaire)
                    * 3600) % (14*24*3600)
    # on retire ce temps pour se retrouver le timestamp du lundi precedent le plus proche
    debutsaison = (now-jouractuelle)*1000
    finsaison = debutsaison+13*24*3600*1000
    return [debutsaison, finsaison]


def GetBoostsDatas(reponse) -> array:  # 0 time #1 typebuff #2 user #3 seq
    rep = str(reponse)
    nbboost = rep.count("GuildBuffAddedEvent")
    i = 0
    data = [[]]
    while i < nbboost-1:
        data.append([])
        i += 1
    i = 0
    while i < nbboost:
        deb = rep.index("eventId")
        rep = rep[deb+10:]
        data[i].append(str(motsuivant(rep, "timestamp")))
        data[i].append(motsuivant(rep, "buffId"))
        data[i].append(motsuivant(rep, "displayName"))
        data[i].append(motsuivant(rep, "seq")[:6])
        i += 1
    return data
