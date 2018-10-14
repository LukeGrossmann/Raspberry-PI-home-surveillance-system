import picamera
from azure.storage.blob import BlockBlobService
import pyodbc
import json
camera = picamera.PiCamera()
camera.capture('/home/pi/Desktop/test1.jpg')
block_blob_service = BlockBlobService('piblobstorage','RH//pydmoOQOkrojSkQnsr/9Y9T5XnHnx43iZMI3ORMscjzQo2ndcLxQXTqyaRX0nECJpOjnPfnb1OQL5NrOqg==')
block_blob_service.create_blob_from_path('picontainer','test1.jpg', '/home/pi/Desktop/test1.jpg')
blob_url = block_blob_service.make_blob_url('picontainer','test1.jpg')


server = 'pisqlserver.database.windows.net'
db = 'pisqldb'
uid = 'piadmin'
pw = 'Pipassword135$'
cnn_string = 'DRIVER=FreeTDS;SERVER='+server+';PORT=1433;DATABASE='+db+';UID='+uid+';PWD='+pw+';TDS_Version=8.0;'

cnn = pyodbc.connect(cnn_string)
cursor = cnn.cursor()

query = "delete from image_table; insert into image_table (description, url) values ('{}','{}')".format('test', blob_url)
cursor.execute(query)
cnn.commit()



import cognitive_face as CF
SUBSCRIPTION_KEY = 'ed143aa5a120426885e46145787be669'
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'
PERSON_GROUP_ID = 'known-persons2'
CF.BaseUrl.set(BASE_URL)
CF.Key.set(SUBSCRIPTION_KEY)


response = CF.face.detect('/home/pi/Desktop/test1.jpg')
face_ids = [d['faceId'] for d in response]
print(face_ids)

identified_faces = CF.face.identify(face_ids, PERSON_GROUP_ID)
print(identified_faces)

person = identified_faces[0]['candidates'][0]['personId']

cnn = pyodbc.connect(cnn_string)
cursor = cnn.cursor()

query = "select * from persons where thekey ='"+ person +"'"
print(query)
result = cursor.execute(query)
for a in result:
  print(a)