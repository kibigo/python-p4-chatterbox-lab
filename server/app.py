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

@app.route('/messages', methods = ['GET', 'POST'])
def messages():

    if request.method == 'GET':

        messages = [message.to_dict() for message in Message.query.order_by(Message.created_at).all()]

        response = make_response(
            jsonify(messages),
            200
        )

        return response

    elif request.method == 'POST':

        new_data = request.get_json()

        new_message = Message(
            body = new_data["body"],
            username = new_data["username"]
        )

        db.session.add(new_message)
        db.session.commit()

        new_message_dict = new_message.to_dict()

        response = make_response(
            jsonify(new_message_dict),
            201
        )
        return response


@app.route('/messages/<int:id>', methods = ['DELETE', 'PATCH'])
def messages_by_id(id):

    messages = Message.query.filter_by(id = id).first()

    if request.method == 'PATCH':
        
        new_data = request.get_json()

        for item in new_data:
            setattr(messages, item, new_data[item])

        db.session.add(messages)
        db.session.commit()

        messages_dict = messages.to_dict()

        response = make_response(
            jsonify(messages_dict),
            200
        )

        return response
    
    elif request.method == 'DELETE':

        db.session.delete(messages)
        db.session.commit()

        response_message = {
            "message":"Deleted successfully"
        }

        response = make_response(
            jsonify(response_message),
            200
        )
        return response



if __name__ == '__main__':
    app.run(port=5555)
