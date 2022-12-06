import requests
import pandas
from datetime import datetime
import json


API = "GmEPb1B.bfqJLIhcGAsH9fTJevTglhFpCoZyAAAdhp"
start = "2022-01-01"
end = "2022-12-31"
ressourcentyp = "plenarprotokoll-text"
zuordnung = "BT"
oldCursor = ""
Dates_Text = {}
results = pandas.DataFrame()
URL = f"https://search.dip.bundestag.de/api/v1/{ressourcentyp}?f.zuordnung={zuordnung}&f.datum.start={start}&f.datum.end={end}&apikey={API}"


def main():
    print("getting data.....")
    getData()


def getData():
    global oldCursor
    global Dates_Text


    if oldCursor == "":
        response = requests.get(URL).json()
    else:
        URL_CURSOR = f"&cursor={oldCursor}"
        print("")
        print(URL + URL_CURSOR)
        response = requests.get(URL + URL_CURSOR).json()


        newCursor = response["cursor"].replace("+", "%2B")
        newCursor = newCursor.replace("/", "%2F")

        for document in response["documents"]:

            datum = datetime.strptime(document["datum"], "%Y-%m-%d").strftime("%Y-%m")
            if("text" in document):
            if datum not in Dates_Text:
    
                Dates_Text[datum] = document["text"]
            else:
                Dates_Text[datum] += document["text"]

        print("old cursor:" + oldCursor)
        print("new cursor:" + newCursor)
        if oldCursor != newCursor:
            oldCursor = newCursor
            getData()

    json.dump(Dates_Text, open("Dates_Text.json", "w"))


if __name__ == "__main__":
    main()
