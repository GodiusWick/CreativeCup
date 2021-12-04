import psycopg2

class DB():
    con = None

    # Initialisation
    def __init__(self):
        self.Reconnect()
        print("Database opened succesfully")

    def Reconnect(self):
        self.con = psycopg2.connect(
        database="rosatom",
        user="rosatom",
        host="myp3a.noip.me",
        port="5432"
        )

    # GetUser returns full information about user
    def GetUser(self, login):
        self.Reconnect()
        cursor = self.con.cursor(buffered=True)
        cursor.execute("SELECT password FROM users WHERE login = '" + login + "'")
        raws = cursor.fetchall()

        return raws[0]["password"]

    # GetRegionInfo returns nessesery 
    def GetRegionInfo(self, uuidImport):
        self.Reconnect()
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM images WHERE uuid = (SELECT id_image FROM imports WHERE uuid = '"+ uuidImport +"' LIMIT 1) LIMIT 1")
        raws = cursor.fetchall()

        return raws[0]

    # ChangeStatus change status of pollution by client
    def ChangeStatus(self, uuidImport, status):
        self.Reconnect()
        cursor = self.con.cursor()

        cursor.execute("UPDATE imports SET status = " + status + " WHERE uuid = '" + uuidImport + "'")
        cursor.execute("UPDATE images SET status = " + status + " WHERE uuid = (SELECT uuid FROM images WHERE images.uuid = (SELECT id_image FROM imports WHERE uuid = '"+ uuidImport +"' LIMIT 1) LIMIT 1)")
        self.con.commit()
        return dict()

    # GetImportsByFilters return information about imports, using client filters
    def GetImportsByFilters(self, status):
        self.Reconnect()
        cursor = self.con.cursor()

        if (status == ""):
            cursor.execute("SELECT im.uuid, im.status, im.timestart, im.timeupdate, im.timeend, ima.region, ima.lon, ima.lan, im.id_image FROM imports AS im INNER JOIN images AS ima ON im.id_image = ima.uuid")
            resp = cursor.fetchall()
            return resp
        else:
            cursor.execute("SELECT im.uuid, im.status, im.timestart, im.timeupdate, im.timeend, ima.region, ima.lon, ima.lan, im.id_image FROM imports AS im INNER JOIN images AS ima ON im.id_image = ima.uuid WHERE im.status = " + status)
            resp = cursor.fetchall()
            return resp