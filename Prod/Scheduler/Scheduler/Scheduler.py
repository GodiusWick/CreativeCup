import time
import schedule
from extract_image import extract_image
import os
from dotenv import load_dotenv
import requests
from db import db
import base64
from PIL import Image


# Initialisation 
dotenv_path = os.path.join('./','.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

dbCon = db.db('rosatom', 'myp3a.noip.me', '', 'rosatom', '5432')
resp = [
    {
        "coordinates":[[[57.726288,-20.389003],[57.726288,-20.368929],[57.7562,-20.368929],[57.7562,-20.389003],[57.726288,-20.389003]]],
	    "resolution": 20,
	    "time_interval": ['2020-08-11', '2020-08-11']
    },
    {
		"coordinates":[[[57.726288,-20.389003],[57.726288,-20.368929],[57.7562,-20.368929],[57.7562,-20.389003],[57.726288,-20.389003]]],
		"resolution": 20,
		"date": ['2020-08-11', '2020-08-11']
	},
	{
		"coordinates":[[[87.891569,69.444207],[87.891569,69.4674],[87.96298,69.4674],[87.96298,69.444207],[87.891569,69.444207]]],
		"resolution": 20,
		"date": ['2020-05-31', '2020-05-31']
	},
	{
		"coordinates":[[[39.103088,21.365809],[39.103088,21.447317],[39.187374,21.447317],[39.187374,21.365809],[39.103088,21.365809]]],
		"resolution": 20,
		"date": ['2019-10-14', '2019-10-14']
	},
	{
		"coordinates":[[[57.72809,-20.445592],[57.72809,-20.423393],[57.757273,-20.423393],[57.757273,-20.445592],[57.72809,-20.445592]]],
		"resolution": 20,
		"date": ['2020-08-01', '2020-08-01']
	},
	{
		"coordinates":[[[-38.596129,-3.698834],[-38.596129,-3.677549],[-38.579607,-3.677549],[-38.579607,-3.698834],[-38.596129,-3.698834]]],
		"resolution": 20,
		"date": ['2019-09-01', '2019-09-01']
	},
	{
		"coordinates":[[[87.901354,69.453035],[87.901354,69.469296],[87.954483,69.469296],[87.954483,69.453035],[87.901354,69.453035]]],
		"resolution": 20,
		"date": ['2020-06-01', '2020-06-01']
	},
	{
		"coordinates":[[[57.767487,-20.349053],[57.767487,-20.330503],[57.788343,-20.330503],[57.788343,-20.349053],[57.767487,-20.349053]]],
		"resolution": 20,
		"date": ['2020-08-11','2020-08-11']
	},
	{
		"coordinates": [[[-9.108009,39.637158],[-9.072475,39.637158],[-9.072475,39.603969],[-9.108009,39.603969],[-9.108009,39.637158]]],
		"resolution": 20,
		"date": ['2018-10-27','2018-10-27']
	},
	{
		"coordinates":[[[15.88563,37.903676],[15.853229,37.903676],[15.853229,37.926563],[15.88563,37.926563],[15.88563,37.903676]]],
		"resolution": 20,
		"date": ['2020-04-04','2020-04-04']
	},
	{
		"coordinates":[[[34.399137,31.528653],[34.424758,31.528653],[34.424758,31.505056],[34.399137,31.505056],[34.399137,31.528653]]],
		"resolution": 20,
		"date": ['2018-04-06','2018-04-06']
	}
]




# Initialisation Import
def InitImport():
    dbCon = db.db('rosatom', 'myp3a.noip.me', '', 'rosatom', '5432')
    uuidImport = dbCon.StartImport()
    resp = dbCon.GetReestr()
    for s in resp:
        r = requests.post("http://192.168.43.181:49160/StartDefine", json={'coordinates':s['coordinates'], 'resolution':s['resolution'], 'time_interval':s['time_interval']}).json()
        image_bytes = r['rgb']

        image_bytes = image_bytes.encode()
        image_bytes = base64.b64decode(image_bytes)
        Image.frombytes(data=image_bytes, size=r['size'], mode='RGB').save("g.png")
        try:
            resp = extract_image.CheckImage(MarR["gz"])
            uuidImage = dbCon.AddImage('Test', 'Now()')
            dbCon.EndImport(uuidImport, uuidImage)
        except:
            dbCon.ChangeImportStatusError(imports[i])

# Time

schedule.every(3).minutes.do(InitImport)

while(True):
    schedule.run_pending()
    time.sleep(1)