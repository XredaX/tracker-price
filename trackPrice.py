import requests
import re
from ticker_rules import rules
from database import user
from dateutil.relativedelta import relativedelta
from datetime import datetime
token = "5545323927:AAH0Ry9v88G9bMj8TMl53wuae8CkAQRqOtY"
print("start")
def getDuration(then, now, interval = "default"):

    duration = now - then # For build-in functions
    duration_in_s = duration.total_seconds() 
    
    def years():
      return divmod(duration_in_s, 31536000) # Seconds in a year=31536000.

    def days(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 86400) # Seconds in a day = 86400

    def hours(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 3600) # Seconds in an hour = 3600

    def minutes(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 60) # Seconds in a minute = 60

    def seconds(seconds = None):
      if seconds != None:
        return divmod(seconds, 1)
      return duration_in_s

    def totalDuration():
        y = years()
        d = days(y[1]) # Use remainder to calculate next variable
        h = hours(d[1])
        m = minutes(h[1])
        s = seconds(m[1])

        return "🕐 المدة الزمنية: {} أيام, {} ساعات, {} دقائق,  {} ثواني".format(int(d[0]), int(h[0]), int(m[0]), int(s[0]))

    return {
        'years': int(years()[0]),
        'days': int(days()[0]),
        'hours': int(hours()[0]),
        'minutes': int(minutes()[0]),
        'seconds': int(seconds()),
        'default': totalDuration()
    }[interval]
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
        date = datetime.fromtimestamp(date)
        date = date.strftime("%Y-%m-%d %H:%M:%S")
        date1 = date
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
            if data[1] == 0:
                user.addsignals(collection="signal", Owenr=str(chat_id), coin=coin, entry1=listy[1], entry2=listy[2], target1=listy[3], target2=listy[4], target3=listy[5], target4=listy[6], stop=listy[0], chat=str(chat_id), message_id=str(message_id), date1=date1)
            else:
                for d in data:
                    date = str(d["date"])
                    end = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                    end = end + relativedelta(days=1)
                    end = end.date()
                    date_now = datetime.now()
                    date_now = date_now.date()
                    if str(end) == str(date_now):
                        user.deletesignals(collection="signal", Owenr=str(chat_id), coin=coin)
                        user.addsignals(collection="signal", Owenr=str(chat_id), coin=coin, entry1=listy[1], entry2=listy[2], target1=listy[3], target2=listy[4], target3=listy[5], target4=listy[6], stop=listy[0], chat=str(chat_id), message_id=str(message_id), date1=date1)
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
                            date = str(d["date"])
                            end = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                            end = end + relativedelta(days=1)
                            end = end.date()
                            date_now = datetime.now()
                            date_now = date_now.date()
                            if str(end) == str(date_now):
                                user.deletesignals(collection="signal", Owenr=str(chat_id), coin=coin)
                            else:
                                key = "https://api.binance.com/api/v3/ticker/price?symbol="+str(coin)
                                data = requests.get(key)
                                data = data.json()
                                priceNow = float(data['price'])
                                # STOP LOSE
                                try:
                                    if priceNow >  float(stop):
                                        pass
                                    elif priceNow <=  float(stop):          
                                        now = datetime.now()
                                        datem = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                                        then = datetime(int(datem.year), int(datem.month), int(datem.day), int(datem.hour), int(datem.minute), int(datem.second))
                                        date = getDuration(then, now)
                                        per = get_change(float(entry1), float(stop))
                                        per = round(per, 2)
                                        send_msg("#"+str(coin)+"\n\n⛔️ ضربت ستوب لوز - نعوضها لكم ان شاء الله\n\n🩸 نسبة الخسارة : %"+str(per)+" -\n\n"+str(date), message_id, chat_id)
                                        user.editsignals(collection="signal", Owenr=str(chat_id), coin=coin, newInfo="false", target="stop-entry1-entry2-target1-target2-target3-target4")
                                except :
                                    pass
                                # ENTRY POINT
                                try:
                                    if priceNow >=  float(entry1) and priceNow <=  float(entry2): 
                                        now = datetime.now()
                                        datem = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                                        then = datetime(int(datem.year), int(datem.month), int(datem.day), int(datem.hour), int(datem.minute), int(datem.second))
                                        date = getDuration(then, now)
                                        send_msg("#"+str(coin)+"\n\n💎 دخلت لمنطقة الشراء ("+str(entry1)+" - "+str(entry2)+")\n\n"+str(date), message_id, chat_id)
                                        user.editsignals(collection="signal", Owenr=str(chat_id), coin=coin, newInfo="false", target="entry1-entry2")
                                except :
                                    pass
                                # TARGET 1
                                try:
                                    if str(entry1) != "false" and str(entry2) != "false": 
                                        if priceNow >=  float(target1): 
                                            now = datetime.now()
                                            datem = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                                            then = datetime(int(datem.year), int(datem.month), int(datem.day), int(datem.hour), int(datem.minute), int(datem.second))
                                            date = getDuration(then, now)
                                            per = get_change(float(target1), float(entry1))
                                            per = round(per, 2)
                                            send_msg("#"+str(coin)+"\n\n💎 ضربت الهذف الأول ("+str(target1)+")\n\n✅ نسبة الربح : "+str(per)+"%\n\n"+str(date), message_id, chat_id)
                                            user.editsignals(collection="signal", Owenr=str(chat_id), coin=coin, newInfo="false", target="entry1-entry2-target1")
                                    elif str(entry1) == "false" and str(entry2) == "false":
                                        send_msg("#"+str(coin)+"\n\n❌ ملغية ضربت الهذف قبل ما تدخل لمنطقة الشراء", message_id, chat_id)
                                        user.editsignals(collection="signal", Owenr=str(chat_id), coin=coin, newInfo="true", target="stop-entry1-entry2-target1-target2-target3-target4")
                                except:
                                    pass
                                # TARGET 2
                                try:
                                    if priceNow >=  float(target2): 
                                        now = datetime.now()
                                        datem = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                                        then = datetime(int(datem.year), int(datem.month), int(datem.day), int(datem.hour), int(datem.minute), int(datem.second))
                                        date = getDuration(then, now)
                                        per = get_change(float(target2), float(entry1))
                                        per = round(per, 2)
                                        send_msg("#"+str(coin)+"\n\n💎 ضربت الهذف الثاني ("+str(target2)+")\n\n✅ نسبة الربح : "+str(per)+"%\n\n"+str(date), message_id, chat_id)
                                        user.editsignals(collection="signal", Owenr=str(chat_id), coin=coin, newInfo="false", target="entry1-entry2-target1-target2")
                                except:
                                    pass
                                # TARGET 3
                                try:
                                    if priceNow >=  float(target3): 
                                        now = datetime.now()
                                        datem = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                                        then = datetime(int(datem.year), int(datem.month), int(datem.day), int(datem.hour), int(datem.minute), int(datem.second))
                                        date = getDuration(then, now)
                                        per = get_change(float(target3), float(entry1))
                                        per = round(per, 2)
                                        send_msg("#"+str(coin)+"\n\n💎 ضربت الهذف التالث ("+str(target3)+")\n\n✅ نسبة الربح : "+str(per)+"%\n\n"+str(date), message_id, chat_id)
                                        user.editsignals(collection="signal", Owenr=str(chat_id), coin=coin, newInfo="false", target="entry1-entry2-target1-target2-target3")
                                except:
                                    pass
                                # TARGET 4
                                try:
                                    if priceNow >=  float(target4): 
                                        now = datetime.now()
                                        datem = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                                        then = datetime(int(datem.year), int(datem.month), int(datem.day), int(datem.hour), int(datem.minute), int(datem.second))
                                        date = getDuration(then, now)
                                        per = get_change(float(target4), float(entry1))
                                        per = round(per, 2)
                                        send_msg("#"+str(coin)+"\n\n💎 ضربت الهذف الرابع ("+str(target4)+")\n\n✅ نسبة الربح : "+str(per)+"%\n\n"+str(date), message_id, chat_id)
                                        user.editsignals(collection="signal", Owenr=str(chat_id), coin=coin, newInfo="false", target="entry1-entry2-target1-target2-target3-target4-stop")
                                except:
                                    pass
                        except:
                            pass
                except:
                    pass
