import json
from utils.api import Api

from flask import Flask, request, jsonify
app = Flask(__name__)



def init_project():
    global config
    with open("resources/config.json") as file:
        config = json.load(file)
    api = Api(config)


@app.route("/start", methods=["GET"])
def start():
    init_project()
    return jsonify({
        "status":"started"
    })






if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
