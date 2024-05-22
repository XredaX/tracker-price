import pymongo

passd = "password"
named = "nameofDB"

client = pymongo.MongoClient("mongodb+srv://test:"+passd+"@cluster1.9glic.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database(named)

class user():
    def findacc(collection, Owenr):
        collection = db[collection]
        acc = {"Owenr":Owenr}
        count = collection.count_documents(acc)
        return count

    def findsignals(collection, Owenr, coin):
        collection = db[collection]
        signal = {"Owenr":Owenr, "coin":coin}
        data = collection.find(signal)
        count = collection.count_documents(signal)
        return data, count

    def findsignals1(collection):
        collection = db[collection]
        data = collection.find({})
        count = collection.count_documents({})
        return data, count

    def addsignals(collection, Owenr, coin, entry1, entry2, target1, target2, target3, target4, stop, chat, message_id, date1):
        collection = db[collection]
        signals = {"Owenr":Owenr, "coin":coin, "entry1":entry1, "entry2":entry2, "target1":target1, "target2":target2, "target3":target3, "target4":target4, "stop":stop, "chat":chat, "message_id":message_id, "date":date1}
        collection.insert_one(signals)

    def deletesignals(collection, Owenr, coin):
        collection = db[collection]
        signal = {"Owenr":Owenr, "coin":coin}
        collection.delete_one(signal)

    def editsignals(collection, Owenr, coin, newInfo, target):
        collection = db[collection]
        signal = {"Owenr":Owenr, "coin":coin}
        target1 = target.split("-")
        for t in target1:
            new = {"$set":{t:newInfo}}
            collection.update_one(signal, new)
