import base64
from PIL import Image
import io
from db import db

# CheckImage send image to neuronAPI for analysis 
def CheckImage(gzBytes):
    return SendImages(gzBytes)

# SaveImage store photo in right folder on the server
def SaveImage(uuidImage, region, timestamp, bytestring):

    bytestring = bytestring.encode()

    f = base64.b64decode(bytestring)

    with open("/"+region+"/" + timestamp + "/" + uuidImage + ".jpg", 'wb') as imagefile:
        imagefile.write(f)

    imagefile.close()


# SendImages send gz to Neuron for update
def SendImages(bytestring):
    db.StartImport()
    r = requests.post("http://127.0.0.1:5000/launchNeuron/", json={"ArchiveBytes":bytestring})
    json_response = r.json()

    return json_response

