import requests
import re
from ticker_rules import rules
from database import user
import time

token = "5545323927:AAH0Ry9v88G9bMj8TMl53wuae8CkAQRqOtY"

print("start")

def get_change(current, previous):
    if current == previous:
        return 100.0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0

def send_msg(msg, message_id, chat_id):
    base_url1 = "https://api.telegram.org/bot"+token

    parameters = {
        "chat_id" : chat_id,
        "text" : msg,
        "reply_to_message_id" : message_id
    }

    requests.get(base_url1 + "/sendMessage", data = parameters)

while True:
    try:
        base_url = "https://api.telegram.org/bot"+token+"/getUpdates?offset=-1"
        resp = requests.get(base_url)
        resp = resp.json()
        msg = resp['result'][0]['channel_post']['text']
        message_id = resp['result'][0]['channel_post']['message_id']
        chat_id = resp['result'][0]['channel_post']['sender_chat']['id']
        date = resp['result'][0]['channel_post']['date']

        count = user.findacc(collection="acc", Owenr=str(chat_id))
        if count >= 0:
            coin = ""
            res = msg.split()
            listy = re.findall("\d+\.\d+", str(msg))
            if len(listy) >= 4:
                listy.sort()
                for r in res:
                    cleanString = re.sub('\W+','', r).upper()
                    if re.search("USDT", cleanString):
                        for t in rules:
                            if cleanString == t:
                                coin = cleanString
                        break
                    else:
                        cleanString = cleanString+"USDT"
                        for t in rules:
                            if cleanString == t:
                                coin = cleanString

            data = user.findsignals(collection="signal", Owenr=str(chat_id), coin=coin)
            if data == 0:
                data = user.addsignals(collection="signal", Owenr=str(chat_id), coin=coin, entry1=listy[1], entry2=listy[2], target1=listy[3], target2=listy[4], target3=listy[5], target4=listy[6], stop=listy[0], chat=str(chat_id), message_id=str(message_id))
    except :
        pass
            

    data = user.findsignals1(collection="signal")
    if data[1]>0:
            for k in data:
                try:
                    for d in k:
                        try:
                            coin = d["coin"]
                            stop = d["stop"]
                            entry1 = d["entry1"]
                            entry2 = d["entry2"]
                            target1 = d["target1"]
                            target2 = d["target2"]
                            target3 = d["target3"]
                            target4 = d["target4"]
                            message_id = d["message_id"]

                            key = "https://api.binance.com/api/v3/ticker/price?symbol="+str(coin)
                            data = requests.get(key)
                            data = data.json()
                            priceNow = float(data['price'])
                            check = 0

                            # STOP LOSE
                            try:
                                if priceNow >  float(stop):
                                    pass
                                elif priceNow <=  float(stop):
                                    send_msg("STOP LOSE", message_id, chat_id)
                                    user.editsignals(collection="signal", Owenr=str(chat_id), coin=coin, newInfo="false", target="stop-entry1-entry2-target1-target2-target3-target4")
                            except :
                                pass

                            # ENTRY POINT
                            try:
                                if priceNow >=  float(entry1) and priceNow <=  float(entry2): 
                                    msg = "BETWEEN ENTRY 1 AND ENTRY 2"
                                    send_msg(msg, message_id, chat_id)
                                    user.editsignals(collection="signal", Owenr=str(chat_id), coin=coin, newInfo="false", target="entry1-entry2")
                            except :
                                pass

                            # TARGET 1
                            try:
                                if priceNow >=  float(target1) and priceNow <  float(target2): 
                                    msg = "TARGET 1"
                                    send_msg(msg, message_id, chat_id)
                                    user.editsignals(collection="signal", Owenr=str(chat_id), coin=coin, newInfo="false", target="entry1-entry2-target1")
                            except:
                                pass

                            # TARGET 2
                            try:
                                if priceNow >=  float(target2) and priceNow <  float(target3): 
                                    
                                    msg = "TARGET 2"
                                    send_msg(msg, message_id, chat_id)
                                    user.editsignals(collection="signal", Owenr=str(chat_id), coin=coin, newInfo="false", target="entry1-entry2-target1-target2")
                            except:
                                pass

                            # TARGET 3
                            try:
                                if priceNow >=  float(target3) and priceNow <  float(target4): 
                                    msg = "TARGET 3"
                                    send_msg(msg, message_id, chat_id)
                                    user.editsignals(collection="signal", Owenr=str(chat_id), coin=coin, newInfo="false", target="entry1-entry2-target1-target2-target3")
                            except:
                                pass

                            # TARGET 4
                            try:
                                if priceNow >=  float(target4): 
                                    msg = "TARGET 4"
                                    send_msg(msg, message_id, chat_id)
                                    user.editsignals(collection="signal", Owenr=str(chat_id), coin=coin, newInfo="false", target="entry1-entry2-target1-target2-target3-target4-stop")
                            except:
                                pass
                            
                            time.sleep(10)
            
                        except:
                            pass
                except:
                    pass