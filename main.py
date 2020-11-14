from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from nltk.tokenize import word_tokenize, sent_tokenize
from summarizer_bert_model import summarizer_bert_get

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class Text_model(db.Model):
    text_id = db.Column(db.Integer, primary_key = True)
    text_url = db.Column(db.String, nullable = True)
    text_in = db.Column(db.String, nullable = False)
    text_out = db.Column(db.String, nullable = False)
    len_out = db.Column(db.Integer, nullable = False)
    text_method = db.Column(db.String, nullable = False)

    def __repr__(self):
        return f"Text(text_in={self.text_in}, text_out={self.text_out}, text_method={self.text_method})" 

# db.create_all() # run_once

Text_put_args = reqparse.RequestParser()
Text_put_args.add_argument("text_url", type = str, help = "text_url needed", required = False)
Text_put_args.add_argument("text_in", type = str, help = "text_in needed", required = True)
Text_put_args.add_argument("len_out", type = str, help = "len_out needed", required = False)
Text_put_args.add_argument("text_method", type = str, help = "text_method needed", required = False)

Text_update_args = reqparse.RequestParser()
Text_update_args.add_argument("text_in", type = str, help = "text_in needed")
# Text_update_args.add_argument("views", type = int, help = "Views needed")
# Text_update_args.add_argument("likes", type = int, help = "Likes needed")

resource_fields = {
    "text_id": fields.Integer,
    "text_in": fields.String,
    "text_url": fields.String,
    "len_out": fields.Integer,
    'text_out': fields.String,
    "text_method": fields.String
}


# app

class HelloWorld(Resource):
    @marshal_with(resource_fields)
    def get(self, Text_id):
        result = Text_model.query.filter_by(id = Text_id).first()
        if not result:
            abort(404, message = "No such id")
        return result

    @marshal_with(resource_fields)
    def put(self, Text_id):
        args = Text_put_args.parse_args()
        result = Text_model.query.filter_by(text_id = Text_id).first()
        if result:
            abort(409, message = "Text id existed")
        # Text = Text_model(id = Text_id, text_in = args['text_in'], views = args['views'], likes = args['likes'])
        output = summarizer_bert_get(args["text_url"], args['text_in'], args["len_out"])

        # print("Hoho", args["text_in"])
        Text = Text_model(text_id = Text_id, text_url = args["text_url"], text_in = args['text_in'],  
                         text_out = output["sentences"], len_out = output['summary_num_sentences'], 
                         text_method = output["method"])

        # print("haha", Text)
        db.session.add(Text)
        db.session.commit()
        return Text, 201

    @marshal_with(resource_fields)
    def patch(self, Text_id):
        args = Text_update_args.parse_args()
        result = Text_model.query.filter_by(text_id = Text_id).first()
        if not result:
            abort(404, message = "No such id, cannot update")
        
        if args["text_in"]:
            result.text_in = args['text_in']
        if args["text_out"]:
            result.text_out = args['text_out']
        # if args['views']:
        #     result.views = args['views']
        # if args['likes']:
        #     result.likes = args['likes']
        db.session.commit()

        return result
        

        

    def delete(self, Text_id):
        abort_if_Text_id_not_existed(Text_id)
        del Texts[Text_id]
        return "Done", 204


    
# registering resources
api.add_resource(HelloWorld, "/<int:Text_id>")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)