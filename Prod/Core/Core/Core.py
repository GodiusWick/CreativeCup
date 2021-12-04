from flask import Flask
from Quotes import Quote

app = Flask(__name__)
q = Quote.Quote()

# postRegionInfo send all information about region to client
@app.route('/getRegionInfo', methods=['POST'])
def post_region():
    resp = q.PostRegionInfo()
    return resp

# post_changestatus where is unknown situation at the region
@app.route('/changeStatus', methods=['POST'])
def post_changeStatus():
    return q.PostChangeStatus()

# post_imports returns all imports by filters
@app.route('/getImports', methods=['POST'])
def post_imports():
    return q.PostImports()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=49161,debug=True)