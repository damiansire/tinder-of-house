from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
import bdDao;

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/v1/houses/initial', methods=['GET'])
@cross_origin()
def get_initial_houses():
	initial_houses = bdDao.get_initial_house()
	print(initial_houses)
	return jsonify(initial_houses)

@app.route('/api/v1/houses/new', methods=['GET'])
@cross_origin()
def get_new_houses():
	new_house = bdDao.get_new_house()
	return jsonify(new_house)

@app.route('/api/v1/houses/selection', methods=['POST'])
@cross_origin()
def select_houses():
	print(request.json)	
	bdDao.save_action_to_house(request.json)
	return jsonify("hola")


app.run(debug=True, port=5550)

