from DB import DB
import jwt
from flask import request

class Quote():
    db = DB.DB()

    # PostRegionInfo returns full information about region
    def PostRegionInfo(self):
        try:
            filters = {
                'uuidImport':request.json['uuidImport']
                }
            
            quote = self.db.GetRegionInfo(filters['uuidImport'])

            resp = dict()

            print(quote)

            resp['uuid'] = quote[0]
            resp['src'] = quote[1]
            resp['region'] = quote[2]
            resp['status'] = quote[4]
            resp['lon'] = quote[5]
            resp['lan'] = quote[6]
            resp['timestamp'] = quote[7]

            return resp, 200

        except:
            resp = dict()
            return resp, 400

    # PostChangeStatus change region's condition to bad or good by client request
    def PostChangeStatus(self):
        try:
            filters = {
                'uuidImport':request.json['uuidImport'],
                'status': request.json['status']
                }

            self.db.ChangeStatus(filters['uuidImport'], filters['status'])

            return dict(), 200
        except:
            return dict(), 400
    
    # PostImports send information about imports to client
    def PostImports(self):
        try:
            filters = {
                'status':request.json['status']
                }

            Imports = self.db.GetImportsByFilters(filters['status'])
            resp = dict()
            i = 0
            for s in Imports:
                resp[i] = dict()
                resp[i]['uuid'] = s[0]
                resp[i]['status'] = s[1]
                resp[i]['timestart'] = s[2]
                resp[i]['timeupdate'] = s[3]
                resp[i]['timeend'] = s[4]
                resp[i]['region'] = s[5]
                resp[i]['log'] = s[6]
                resp[i]['lan'] = s[7]
                resp[i]['id_image'] = s[8]
                i+=1

            return resp, 200

        except:
            return dict(), 400