import pandas as pd 
import re

media_url = {
        "ABCNews": "ABC",
        "arstechnica.com": "Arstechnica",
        "Atlantic": "TheAtlantic",
        "BaltimoreSun": "BaltimoreSun",
        "bbc": "BBC",
        "apnews": "AP",
        "Benzinga": "NA",
        "Blaze": "TheBlaze",
        "Bloomberg": "Bloomberg",
        "bostonglobe": "BostonGlobe",
        "Breitbart": "Breitbart",
        "Insider": "BusinessInsider",
        "Bustle": "Bustle",
        "Buzzfeed": "Buzzfeed",
        "BuffaloNews": "BuffaloNews",
        "CBSNews": "CBS",
        "cbs": "CBS",
        "ChicagoTribune": "ChicagoTribune",
        "CSMonitor": "ChristianScienceMonitor",
        "CNBC": "CNBC",
        "CNN": "CNN",
        "Conversation": "Conversation",
        "DailyBeast": "DailyBeast",
        "DailyCaller": "DailyCaller",
        "DailyDot": "DailyDot",
        "DailyKos": "DailyKos",
        "dailymail": "DailyMail",        
        "daily_mail": "DailyMail",
        "daily_wire": "DailyWire",
        "DallasNews": "DallasNews",
    "engadget": "engadget",
    "Fortune": "Fortune",
    "FoxNews": "Fox",
    "gq.com": "GQ",
    "Guardian": "Guardian",
    "houstonchronicle": "houstonchronicle",
    "Hoy Chicago": "NA",
    "HuffPo": "HuffingtonPost",
    "HuffingtonPo": "HuffingtonPost",    
    "Infowars": "InfoWars",
    "Intercept": "Intercept",
    "Jezebel": "Jezebel",
    "LATimes": "LATimes",
    "Mashable": "Mashable",
    "MiamiHerald": "MiamiHerald",
    "MSNBC": "MSNBC",
    "MilwaukeeJournal": "MilwaukeeJournalSentinel",
    "MotherJones": "MotherJones",
    "NationalReview": "NationalReview",
    "NBC": "NBC",
    "NYPost": "NYPost",
    "NYTimes": "NYTimes",
    "NewYorker": "NewYorker",
    "Newsday": "Newsday",
    "Newsmax": "Newsmax",
    "Newsweek": "Newsweek",
    "NPR": "NPR",
    "Oan": "OANN",
    "PEOPLE.com": "People",
    "PJMedia": "PJMedia",
    "Politico": "Politico",
    "polygon.com": "polygon",
    "ProPublica": "ProPublica",
    "Pbs": "Pbs",
    "Quartz": "Quartz",
    "RawStory": "RawStory",
    "Recode": "Recode",
    "Reason.com": "Reason",
    "reuters": "Reuters",
    "Red Herring": "NA",
    "RedState": "RedState",
    "Refinery29": "Refinery29",
    "Reuters": "Reuters",
    "RollingStone": "RollingStone",
    "rttnews": "RTnews",
    "Salon": "Salon",
    "MercuryNews": "SanJoseMercuryNews",
    "Mirror": "DailyMirror",
    "SeattleTimes": "SeattleTimes",
    "sentinelsource.com": "NA",
    "SFChronicle": "SFChronicle",
    "Slate": "Slate",
    "StarTribune": "StarTribune",
    "TampaBayTimes": "TampaBayTimes",
    "TechCrunch": "TechCrunch",
    "techradar.com": "techradar",
    "Nation": "TheNation",
    "NewReplublic": "NewReplublic",
    "telegrpah": "TheDailyTelegraph",
    "sportico": "Sportico",
    "statnews": "StatNews",
    "TheWeek": "TheWeek",
    "theroot.com": "TheRoot",
    "theringer": "TheRinger",
    "Time.com": "Time",
    "today" : "Today",
    "Truthout": "Truthout",
    "USAToday": "USAToday",
    "VanityFair": "VanityFair",
    "Verge": "TheVerge",
    "vulture": "Vulture",
    "VICE": "VICE",
    "Vox": "Vox",
    "wapo": "WashingtonPost",
    "WashingtonPost": "WashingtonPost",
    "usnews": "USNews",
    "wired": "Wired",
    "wsj": "WallStJournal",
    "www.fox": "Fox",
    "hollywood": "HollywoodReporter",
    "zdnet": "ZDNet",
    "jacobin": "Jacobin",
    "yahoo": "YahooNews",
    "nymag": "NYMag",
    "qz": "Quartz",
    "variety": "Variety",
    "aljazeera": "aljazeera",
    "aol": "AOL",
    "economist": "Economist",
    "espn": "ESPN",
    "axios": "Axios",
    "cnet": "cnet",
    "rt.com": "RussiaToday",
    "seattle_times": "SeattleTimes",
    "substack": "substack",
    "deadline": "deadline",
    "bloomberg": "bloomberg",
    "nation": "thenation",
    "kotaku": "kotaku",
    "lifehacker": "lifehacker",
    "suntimes": "suntimes",
    "thetimes": "thetimes",
    "gallup": "gallup",
    "gizmodo": "gizmodo",
    "indiwire": "indiewire",
    "the-sun": "the sun",
    "scmp": "scmp",
    "minnpost": "minnpost",
    "military": "military times",
    "thelily": "Washington Post",
    "thedrive": "the drive",
    "examiner": "washington examiner",
    "Mic": "Mic",
    "telegraph": "telegraph",
    "vibe": "vibe"
    
}

def f(row):
    #print(row)
    for key in media_url.keys():
        key_search = key.lower()
        row['url'] = str(row['url'])
        #print(row['url'])
        m = re.search(key_search, row['url'])
        if m is not None:
            return media_url[key]
    return row['url']


def get_multiple(row):
    if row['url'] == "NYTimes":
        return 1.2
    elif row['url'] == "WashingtonPost":
        return 1.15
    elif row['url'] == "NewYorker":
        return 1.125
    elif row['url'] == "LATimes":
        return 1.05
    elif row['url'] == "BBC":
        return 1.1
    elif row['url'] == "WallStJournal":
        return 1.1
    elif row['url'] == "Bloomberg":
        return 1.05
    else:
        return 1

    

media_data = pd.read_csv("journo_followers4.csv", lineterminator='\n', encoding ='utf-8')


media_data["url"] = media_data.apply(f, axis=1)
multiplier = media_data.apply(get_multiple, axis=1)

media_data.insert(4, "multiplier", multiplier, True)


media_data.to_csv(path_or_buf="journo_followers4b.csv", index = False)
