from flask import Flask, request, make_response
import json
from dbhelpers import run_statement
from apihelpers import check_endpoint_info
import dbcreds

app = Flask(__name__)

@app.post('/api/pokemon')
def post_pokemon():
    is_valid = check_endpoint_info(request.json, ['name','image_url','description'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = run_statement('CALL create_pokemon(?,?,?)',
    [request.json.get('name'),request.json.get('description'),request.json.get('image_url')])

    if(type(results) == list):
        return make_response(json.dumps(results[0][0], default=str), 200)
    else:
        return make_response(json.dumps('Sorry, there has been an error', default=str), 500)

@app.get('/api/pokemon')
def get_pokemon():
    results = run_statement('CALL get_pokemon()')
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps('Sorry, there has been an error', default=str), 500)

if(dbcreds.production_mode == True):
    print("Running in Production Mode")
    import bjoern # type: ignore
    bjoern.run(app, "0.0.0.0", 5134)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")
    app.run(debug=True)