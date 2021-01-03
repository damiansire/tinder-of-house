from flask import Flask
from flask import jsonify
from flask_cors import CORS, cross_origin
import bdDao;

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/api/v1/getAllHouse/', methods=['GET'])
@cross_origin()
def get_all_houses():
	all_house = bdDao.get_all_house()
	return jsonify(all_house)

app.run(debug=True, port=5550)

