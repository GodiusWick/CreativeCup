import psycopg2
import json

class db():

    conn = None
    
    # Initialisation DB
    def __init__(self, dbName, Host, Port, User, Password):
        self.conn = psycopg2.connect(dbname=dbName, user=User, password = Password, host=Host, port=Port)

    #ChangeImportStatusError write into DB about failed import
    def ChangeImportStatusError(self, import_id, status_id):
        cursor = conn.cursor()
        rows = cursor.execute("UPDATE imports SET status = 2 WHERE uuid = '" + import_id + "'")

    # StartImport register import, which scheduler start
    def StartImport(self):
        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO imports (status, timestart, timeupdate) VALUES(1, Now(), Now())")
        self.conn.commit();

        cursor.execute("SELECT uuid FROM imports ORDER BY timestart ASC")
        rows = cursor.fetchall()

        return rows[0][0]
    
    # AddImage save results of neuron work
    def AddImage(self, region, statusID, timestamp, lon, lan):
        cursor = self.conn.cursor()
        rows = cursor.execute("INSERT INTO images (src, region, status, lon, lan, dateofget)"+
                              +" VALUES ('"+ region +"/"+ timestamp +"', "+ region +" ,"+ statusID +", "+ lon +", "+ lan +")")

        return rows[0]["uuid"]

    # EndImport update import status, in dependence of neuron work result
    def EndImport(self, uuid, uuidImage, status):
        cursor = self.conn.cursor()
        rows = cursor.execute("UPDATE imports SET status = ", status + ", id_image = '"+ uuidImage +"' WHERE uuid = '" + uuid + "'")

    def GetReestr(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM reestr")
        resp = cursor.fetchall()
        return resp