#!/usr/bin/env python3
import json
import os
import threading
import time
from queue import Queue

import argparse
import requests
from urllib.parse import unquote
import traceback


ACTIVITY_URL = "https://steamcommunity.com/market/itemordersactivity"\
               "?item_nameid={item_id}&country=RU&language=english&currency=1&&two_factor=0&norender=1"
SEARCH_URL = "https://steamcommunity.com/search/SearchCommunityAjax?text={name}&filter=users&sessionid=b6b624bed152a86b49301d54&steamid_user=76561199215205576&page=1"

def get_activities(item_id):
    return requests.get(ACTIVITY_URL.format(item_id=item_id)).json()["activity"]

def get_steam_id(owner):
    res = requests.get(SEARCH_URL.format(name=owner), headers= { 
    	'cookie': 'timezoneOffset=14400,0; _ga=GA1.2.377957344.1637946950; steamMachineAuth76561199153349208=93E8DB24E1D578459EFBF222CB01C4B8EBC5378D; steamMachineAuth76561199049608346=C83D667FF8AEC21EB87F1D5FED852BC56B907689; steamMachineAuth76561199144030348=252A41652388E504AB79E10EFE83D7943B43F9DF; steamMachineAuth76561199214627720=ABB2E211596C4770AD24B022F8DE86B80FD45BE0; steamMachineAuth76561199074868323=6FCC3A278D239F4665367B0A30CC4D90E490E0F4; steamMachineAuth76561199022570097=33A0946666F73307D79BDD208261EBBAA6106D36; steamMachineAuth76561199053473318=0DF75F647A80F805C143AF3894B999A2400E6CA3; steamMachineAuth76561198880581738=09B2AC2F80080B4E3DF4C70F680EF1950A34B4A6; steamMachineAuth76561198956712976=3DBD5E545A2FF6352BD71631603560AB88EE714B; steamMachineAuth76561198978681072=C094065EFE23AE3FA6ADB27DED4FC4E72A37E133; steamMachineAuth76561198838042002=F2D18D6C3219250D86748106627001338733FDF0; steamMachineAuth76561199020935842=8D10E83963D84058EA6856290E6CD61C50572B22; steamMachineAuth76561198372387195=DA635E5571A9F7345611502103EB66BB96FB91E9; steamMachineAuth76561199113962662=D3E8C357A9316A36B69AC71DA7C6850D2DC8877D; steamMachineAuth76561198892380806=CAA55C755FA6F614F3D8F20E36D665190ED435A0; steamMachineAuth76561198984694336=7C688C70BC642611F89C1F121C989F271B317134; steamMachineAuth76561199023538102=ECA1AC2A027E014B315E0566D55A8553B38B30F7; steamMachineAuth76561199214092093=0018245804498B39641DD67231E7E0E8BD4C2DD3; steamMachineAuth76561199116505980=1CC77026AB9DDF4723DFCF6E7625F9F413778BA7; steamMachineAuth76561199214171729=068FCC3FC9B0745E1D8F4451487572CB7249D8AF; steamMachineAuth76561198819637990=6DEB7E03535F95628CE4974CD91EA1D6B555249C; steamMachineAuth76561199215357953=D1265C140728B17527E78501721DB39BCAD29BAD; steamMachineAuth76561198801845242=9D65C50D0D40286CD53EA54D80C493D740B2DAE7; steamMachineAuth76561198276801827=6E60B030A8B4445196E9972BC313A1B1C43A0D43; steamMachineAuth76561199214626758=3C5172191CCB85785122D54D04D8E3D7B14F9F37; steamMachineAuth76561199057423707=940451618DA9A6003A9DFD076F67CB9DAC5D00B8; steamMachineAuth76561199214420960=EE8F40799943B8186561DB33309BEDA9987DB295; steamMachineAuth76561198107234953=E7765A08FB9CA2690C8AB92D59708FB7D458AF30; steamMachineAuth76561199214217732=EE8E1A6AC473E20B6C50DB1E39AAED8489C70954; steamMachineAuth76561199124775244=29996D7162649510921E2723C7E411B951B892CB; steamMachineAuth76561198829269526=22C7910C63C86D6D7FEAC90A2A10FF90CE2FCB52; steamMachineAuth76561199213924628=BEE7A212017AB2700AA667255F5C51BF465E13D7; steamMachineAuth76561198824387342=57E1D464529BC7060E827B615B784DFB08312A3A; steamMachineAuth76561199214986641=799920515FD63F3350A7F417055DC28D39D39E1E; steamMachineAuth76561199215866989=799E1B72E40304102668E2657392D4FF5D541D4F; steamMachineAuth76561199216151512=B8D7E7412C1BC7230625ED7153DFDBEB09B022ED; steamMachineAuth76561199215205576=D6555C00E4BE7C62B4A12741E15B11DBBE2D48C3; steamMachineAuth76561199020438485=F64E314B9CF9192933E86573661253E9A2AFFF8D; steamMachineAuth76561199242391074=D10A687A4C6254187F3468502ACE5ECAC9F5BEEA; extproviders_252490=; steamMachineAuth76561198109165919=1B90F85F3FF6B53D905A1015C5A0268F55B4B6BB; steamMachineAuth76561199214108991=94F1A359449BEE3B3A2017366FDA21ACD297A3D8; steamMachineAuth76561199032098489=1F2869701ECA24129E0A4F34CBF079AEBB6624D6; steamMachineAuth76561199164339669=1502BC7CEE9BF21E088FFB095D75CD93D5998572; steamMachineAuth76561199022173381=693A503D8E8A1E5FCED2486E9B287EF4DAA9498D; steamMachineAuth76561199027158445=D57809638D534601935B7002C6A14698217F436F; steamCurrencyId=1; steamMachineAuth76561199129532092=FDD3417EA9EF0E1C77AE8F682254B9F2BFDA9DDE; steamMachineAuth76561198908840939=327CBF664D07EB0421FC2723740611B9D777EA17; steamMachineAuth76561199091540574=FF39946949A8C00BCE33351B9BC9038157FF07C2; steamMachineAuth76561199023832823=3BA39D4AAA5FC7286065855F359FB3C565B76477; steamMachineAuth76561199044490136=E4B33530D6EE5752B1D4F34EE42EC5D49B83214A; steamMachineAuth76561199094942316=382ADB2BF107B14955772B4E008D1DD4CE2905F2; steamMachineAuth76561199027692949=74FD064161F46B23BA329928EFC8AFB26A23347D; steamMachineAuth76561199047148990=A667221814094C7AE2C1CC72B73BFAE80CB53FDC; extproviders_730=steamanalyst; recentlyVisitedAppHubs=12210,1782210,440,976730,730,578080; steamMachineAuth76561199040131700=B2D7AC371ED93755639BED1BB927416A50C9E4B7; steamMachineAuth76561199137254676=E397341626EDA8746ABB174DB007BB3CCF5F5476; steamMachineAuth76561198130304491=F1F4C72C2B1E7A4E7C5BBC35A6E71044311C0ECE; steamMachineAuth76561197986590031=6F8C5A6B74F298090B3ABB0ED186177F447C75E4; steamMachineAuth76561199027056810=BBAF374ED98EEE2CF50ED97F8A2B9048D50CEEBF; steamMachineAuth76561199024533539=25533F1353A8E171F3C7B91F297B156E07061F6A; steamMachineAuth76561199077270090=0E8F3E111BEA3D728C048C77D9FEBAED7D9C6ED2; Steam_Language=english; browserid=2700499904571368369; _gid=GA1.2.146767406.1670160843; strInventoryLastContext=730_2; sessionid=b6b624bed152a86b49301d54; steamCountry=GE|8d642378c96620ea31e663140f600dfa; steamLoginSecure=76561199215205576||eyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MENEMF8yMUI5NzQ2Ql9GNjE5MSIsICJzdWIiOiAiNzY1NjExOTkyMTUyMDU1NzYiLCAiYXVkIjogWyAid2ViIiBdLCAiZXhwIjogMTY3MDU5MDEzNCwgIm5iZiI6IDE2NjE4NjM0MDIsICJpYXQiOiAxNjcwNTAzNDAyLCAianRpIjogIjBDRDBfMjFCOTc0NkNfMDgxMDQiLCAib2F0IjogMTY3MDUwMzQwMiwgInJ0X2V4cCI6IDE2ODg1NDg3NzgsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICIyMTIuNTguMTAyLjEzMSIsICJpcF9jb25maXJtZXIiOiAiMjEyLjU4LjEwMi4xMzEiIH0.HIsd8FotJIjAo2v7Nh4qrutVrXldEb6QSGJ-9vZu5z6RiYtUo0T6LaIer3JzWpht8bLmjtArtfU480MFCq5xBA; webTradeEligibility={"allowed":1,"allowed_at_time":0,"steamguard_required_days":15,"new_device_cooldown_days":0,"time_checked":1670506752}',
		'sec-ch-ua-mobile':'?0',
		'sec-ch-ua-platform':"Windows",
		'sec-fetch-dest':'empty',
		'sec-fetch-mode':'cors',
		'sec-fetch-site':'same-origin',
    }).json()['html']
    index = res.find('profiles');
    if index == -1:
    	return 'no'
    pre = index + 9
    last = pre + 17
    return res[pre:last]

def worker(queue):
    global request_count, keyerror_count, unexpected_error_count
    while True:
        listing_id, listing_link = queue.get()
        try:
            for activity in get_activities(listing_id):
                if activity["type"] == "BuyOrderCancel" or activity["type"] == "BuyOrderMulti":
                    continue
                owner = activity["persona_seller"] or activity["persona_buyer"]
                getSteamId = get_steam_id(owner)
                print(getSteamId)
            request_count += 1
            time.sleep(0.03)
        except KeyError:
            keyerror_count += 1
        except:
            unexpected_error_count += 1
            traceback.print_exc()
        queue.put((listing_id, listing_link))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--threadCount", type=int, default=80)     # here i set 2 threads default

    args = parser.parse_args()
    print(args.threadCount)

    with open('listings.json', 'r') as f:
        listings = json.load(f)

    queue = Queue()

    request_count = 0
    keyerror_count = 0
    unexpected_error_count = 0


    for listing_id, listing_link in listings.items():
        queue.put((listing_link, listing_id))

    for _ in range(args.threadCount):
        threading.Thread(target=worker, args=(queue,)).start()


    ## i don't know the purpose of the below while loop, but u can uncomment after all above works fine
    # while True:
    #     print(f"{request_count} request. {keyerror_count} keyerror. {unexpected_error_count} unexpected error")
    #     request_count = 0
    #     keyerror_count = 0
    #     unexpected_error_count = 0
    #     time.sleep(60) 