from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():

    messages = []
    for message in Message.query.all():
        message_dict = {
            "id":message.id,
            "body": message.body,
            "username": message.username,
        }
        messages.append(message_dict)
    
    response = make_response(jsonify(messages), 200) 
    return response   

@app.route('/messages/<int:id>')
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    message_dict = message.to_dict()
    message_dict = {
        "id": message.id, 
        "body": message.body,
        "username": message.username,
    }

    response= make_response(jsonify(message_dict), 200)

    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/messages_order')
def get_messages():
    ordered_messages = Message.query.order_by(Message.created_at.asc()).all()

    messages = []
    for message in ordered_messages:
        message_dict = {
            "id":message.id,
            "body": message.body,
            "username": message.username,
            "created_at": message.created_at,
        }
        messages.append(message_dict)
    
    response = make_response(jsonify(messages), 200) 
    return response   

@app.route('/messages', methods=['GET','POST'])
def add_new_message():

    if request.method == 'GET':
        messages = []
        for message in Message.query.all():
            message_dict = message.to_dict()
            messages.append(message_dict)

        response = make_response(
            jsonify(messages),
            200
        )

        return response   

    elif request.method == 'POST' :
        response_body = {}
        response = make_response(response_body, 201)
        return response


if __name__ == '__main__':
    app.run(port=5558)
