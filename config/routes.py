from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import asyncio
from dotenv import load_dotenv
import os
import sys
sys.path.append('../')
from app.module import execute
from config import Localization

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": os.environ.get("FRONT_API_URL")}})

@app.route("/")
def index():
	return "Welcome to ASEticle."

@app.route('/api/execute', methods=['GET'])
def execute_route():
	if request.args.get('params') is not None:
		params = request.args.get('params')
	else:
		return jsonify({"error": Localization.get('config.routes.bad_request')}), 400

	params = {
		"params": [
			{
				"url": "https://ieeexplore.ieee.org/abstract/document/9908590/",
				"relevant_no": 3
			},
			{
				"url": "https://ieeexplore.ieee.org/document/7725637/",
				"relevant_no": 4
			}
		]
	}

	result = asyncio.run(execute(params))

	response = make_response(jsonify(result))
	response.headers["Access-Control-Allow-Origin"] = "*"
	response.headers["Access-Control-Allow-Headers"] = "X-Requested-With, Origin, X-Csrftoken, Content-Type, Accept"

	return response

if __name__ == "__main__":
	app.run(port=8080, debug=True)