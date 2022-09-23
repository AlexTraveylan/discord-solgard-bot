from requests import post
from fonctions import *

#found the connexionpost with mitmproxy

connexionpost = {
    "builtInMultiConfigVersion": "***********************",
    "installId": "***********************",
    "playerEvent": {
        "createdOn": "*************",
        "gameConfigVersion": "********************",
        "multiConfigVersion": "*************************",
        "playerEventData": {
            "clientSecret": "*********************e",
            "deviceData": {
                "buildString": "********************",
                "countryCode": "FR",
                "deviceId": "*****************",
                "graphicsDeviceName": "******************",
                "graphicsShaderLevel": ********,
                "installId": "******************",
                "locale": "*****",
                "manufacturer": "**********",
                "model": "************",
                "os": "******",
                "platform": "******",
                "processorType": "*********",
                "ram": -246,
                "screenHeight": 1792,
                "screenWidth": 828,
                "store": "********"
            },
            "gameCenterUserId": "G:**************",
            "userId": "***************"
        },
        "playerEventType": "CONNECT",
        "universeVersion": "***********************"
    }
}

r = requests.post(
    "https://api-live.thor.snowprintstudios.com/player/player2/userId/**************************", json=connexionpost)

print(r.text)

sessionID = motsuivant(r.text, "sessionId")
#***** -> userid
alex = user_config('***********',
                   sessionID)


testrecupguildclash = {
    "builtInMultiConfigVersion": buildmulti,
    "installId": install,
    "playerEvent": {
        "createdOn": str(int(time.time()*1000)),
        "gameConfigVersion": gameversion,
        "multiConfigVersion": multiconfigversion,
        "playerEventData": {
            "guildId": guild_id},
        "playerEventType": "VIEW_GUILD_2",
        "universeVersion": universe}}

r = requests.post(alex._url2(), json=testrecupguildclash)
Dic_user = guildmakedic(r.text, 1)
Nbmembres = len(Dic_user)


def listguild(dic):
    res = []
    for nom in dic.values():
        res.append(nom)
    return res


def listguildattaque(dic):
    res = []
    for nom in dic.values():
        res.append([nom, 2])
    return res


tabjoueurs = listguild(Dic_user)
tabjoueursatt = listguildattaque(Dic_user)

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print("Prêt à fonctionner ...")
    # channel = bot.get_channel(994960785526763533)
    # await channel.send("`Bonjour, je suis prêt à fonctionner...`")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("```\nJe ne peux pas faire ça, regarde l'aide : \n\nTape:   !help\n\nMoi je me casse ! TELEPORT !```")


@bot.event
async def on_member_join(member):
    channel = member.guild.get.channel(732280430623195241)
    await channel.send(f"`Bienvenue {member.mention} dans le discord de la guilde Solgard The France Factory, n'hesite pas à postuler pour rejoindre notre guilde avec un message ici.`")


# @bot.command()
# async def h(ctx):
#     text = "```\n!a : Afficher les attaques restantes du jour\n!b : Afficher les bombes restantes du jour\n!buildclash : Le bot rempli automatiquement le googlesheet pour le clash ```"
#     await ctx.send(text)


# @bot.command()
# async def chatguilde(ctx):
#     r = requests.post(
#         alex._url(), json=ConsulterChatGuild)
#     chat = liremessageguildechat(r.text)
#     for chatr in chat:
#         await ctx.send("`{} ({}) : {}`".format(chatr[0], dateheure(chatr[1]), chatr[2]))


# @bot.command()
# async def chatclash(ctx):
#     if ClashDispo():
#         r = requests.post(
#             alex._url(), json=ConsulterChatClash)
#         chat = liremessageguildechat(r.text)
#         for chatr in chat:
#             await ctx.send("`{} ({}) : {}`".format(chatr[0], dateheure(chatr[1]), chatr[2]))
#     else:
#         await ctx.send("`Aucun clash en cours, merci d'attendre vendredi 16h`")


# @bot.command()
# async def clash(ctx):
#     r = requests.post(
#         alex._url(), json=ConsulterAttaquesClash)
#     chat = lireattaqueclash(r.text, Dic_user)
#     for chatr in chat:
#         if chatr[0] == "victoire":
#             await ctx.send("`[{}] {} a vaincu une équipe de {}, dégat sur la def : {}`".format(dateheure(chatr[1]), chatr[6], chatr[2], chatr[4]))
#         elif chatr[0] == "defaite":
#             await ctx.send("`[{}] {} a perdu contre une équipe de {} en infligeant {}, il reste {} hp, dégat de la def : {}`".
#                            format(dateheure(chatr[1]), chatr[8], chatr[2], chatr[5], chatr[4], chatr[6]))


# @bot.command()
# # 0temps #1sourcedegat #2cible #3degat #4hprestant #5nom #6stage
# async def guildboss(ctx):
#     r = requests.post(
#         alex._url(), json=Consulterguildboss)
#     log = recupguilboss(r.text)
#     for logs in log:
#         await ctx.send("`[{}] ({}) {} a infligé {} a {} ({}). Hp restant : {} `".format(logs[1], dateheure(logs[0]), logs[5], logs[3], logs[6], logs[2], logs[4]))


@bot.command()
async def b(ctx):
    tabjoueurs = listguild(Dic_user)
    print(alex._url())
    r = requests.post(alex._url(), json=Consulterguildboss)
    log = bombesrestantes(r.text, tabjoueurs)
    if log[0] > 0:
        await ctx.send("```\nIl reste {} bombes\nBombes restantes : {}```".format(log[0], log[1]))
    else:
        await ctx.send("`Toutes les bombes ont été utilisés`")


@bot.command()
async def a(ctx):
    tabjoueursatt = listguildattaque(Dic_user)
    r = requests.post(alex._url(), json=Consulterguildboss)
    log = attaquesrestantes(r.text, tabjoueursatt,
                            len(tabjoueursatt))
    total = log[0]
    log = log[1]
    text = "```\n"
    if total > 0:
        text = text+"Il reste {} attaques au total :\n".format(total)
        for logs in log:
            try:
                text = text+"  - {} : {}\n".format(logs[0], logs[1])
            except:
                pass
        text = text+"```"
        await ctx.send(text)
    else:
        await ctx.send("`Toutes les attaques ont été effectués aujourd'hui, bravo a tous`")


@bot.command()
async def buildclash(ctx):
    if ClashDispo():
        r = requests.post(
            alex._url2(), json=PLAYER_2)
        powers = recupduelpower(r.text)
        r = requests.post(alex._url2(), json=recupennemyguild)
        enemies_names = listguild(guildmakedic(r.text, 0))
        i = 0
        tabclash = []
        while i < Nbmembres:
            tabclash.append([enemies_names[i], powers[i+Nbmembres][0],
                             powers[i+Nbmembres][1], powers[i+Nbmembres][2]])
            i += 1
        sheet = service.spreadsheets()
        request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range="Bot LOG!A2", valueInputOption="USER_ENTERED", body={"values": tabclash})
        request.execute()
        await ctx.send("`Succès, je te laisse publier les tableaux.`")
    else:
        await ctx.send("`Aucun clash en cours, merci d'attendre vendredi 16h`")


@bot.command()
async def saison(ctx):
    sheet = service.spreadsheets()
    datas = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                               range="Scores assiduités!D28:E29").execute()
    datas = datas['values']
    text = "```\nBilan des attaques et bombes manquantes depuis le debut de la saison : (Hors jour actuel)\n   -{} : {}\n   -{} : {}```".format(
        datas[0][0], datas[0][1], datas[1][0], datas[1][1])
    await ctx.send(text)


@bot.command()
async def classement(ctx):
    sheet = service.spreadsheets()
    datas = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                               range="Scores assiduités!K28:L47").execute()
    datas = datas["values"]
    text = "```\n Classement d'assiduité de la guilde :\n\n"
    i = 1
    for data in datas:
        text = text+" - #{} {} : {} points\n".format(i, data[0], data[1])
        i += 1
    text = text+"\nTaper !regles pour connaitre les critères d'attributions des points```"
    await ctx.send(text)


@bot.command()
async def regles(ctx):
    text = "```\n Voici comment sont attribué les points pour le classement d'assiduité :\n\n"
    text = text + \
        "  - Attaques : +50 points pour une attaque.\n(Bonus+20 si pendant un boost)\n\n"
    text = text + \
        "  - Bombes : +25 points pour une bombe.\n(Bonus+10 si utilisée en fin de vie d'un boss ou d'un cristal)\n\n"
    text = text + \
        "  - Boost : +50 points pour les deux boosts (+25 chacun).\n(Bonus+20 (+10 chacun) si appliqué pendant votre créneau de boost, à plus ou moins 15 minutes)\n\n"
    text = text+"Remarque : Le score de Boost desequilibre forcement les scores, soyez assidus jusqua la fin !```"
    await ctx.send(text)


ConsulterChatGuild = chats("guildchat")

ConsulterChatClash = chats("guildchallengechat")

r = requests.post(
    alex._url2(), json=PLAYER_2)

id_clash = recuperer_clashID_ennemyguildID(r.text)[0]
id_clash1 = "{}_team1".format(id_clash)
id_clash2 = "{}_team2".format(id_clash)

ConsulterAttaquesClashTeam2 = chats(id_clash)

ConsulterAttaquesClashTeam1 = chats(id_clash1)

ConsulterAttaquesClash = chats(id_clash2)

ConsulterBoostsDonates = chats("guild")

Consulterguildboss = chats("guildboss")

ennemyguild_id = recuperer_clashID_ennemyguildID(r.text)[1]

recupennemyguild = {
    "builtInMultiConfigVersion": buildmulti,
    "installId": install,
    "playerEvent": {
        "createdOn": str(int(time.time()*1000)),
        "gameConfigVersion": gameversion,
        "multiConfigVersion": multiconfigversion,
        "playerEventData": {
            "guildId": ennemyguild_id
        },
        "playerEventType": "VIEW_GUILD_2",
        "universeVersion": universe
    }
}

# result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#                             range="Feuille 1!A1:G13").execute()

# values = result.get('values', [])
# print(values)


# # aoa = listguild(guildmakedicandtab(r.text))
# # print(len(aoa))


# wks = sh.worksheet("Feuille 1")
# print(wks.acelle('A1').value)

# r = requests.post(
#     alex._url2(), json=PLAYER_2)
# print(recuperer_clashID_ennemyguildID(r.text))

# HALFAR >> VIOLET//SMANIR >> VERT + VIOLET
bot.run("******************************************")
