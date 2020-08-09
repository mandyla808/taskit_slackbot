from flask import Flask, request, Response
import Taskit
import config
import json

app = Flask(__name__)
toDoList = Taskit.toDoList()


@app.route("/slack/test", methods=['POST'])
def TrainStation():
    #TODO: Set auth to check request is coming from slack
    token = request.form.get('token')
    message = request.form.get('text')
    user_name = request.form.get('user_id')
    data = {
        "text": Taskit.Handler(toDoList, user_name, message),
        "response_type": 'in_channel'
    }
    return Response(response=json.dumps(data), status=200, mimetype="application/json")


@app.route("/test", methods=['GET'])
def HelloWorld():
    return "Everything OK!"


if __name__ == '__main__':
    app.run(port = 80)
