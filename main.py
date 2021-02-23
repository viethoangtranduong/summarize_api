from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from nltk.tokenize import word_tokenize, sent_tokenize
from summarizer_textrank_model import summarizer_textrank_get

app = Flask(__name__)
api = Api(app)

Text_put_args = reqparse.RequestParser()
Text_put_args.add_argument("text_url", type = str, help = "text_url needed", required = False)
Text_put_args.add_argument("text_in", type = str, help = "text_in needed", required = True)
Text_put_args.add_argument("len_out", type = int, help = "len_out needed", required = False)
Text_put_args.add_argument("text_method", type = str, help = "text_method needed", required = False)


class Summarize(Resource):
    @app.route('/')
    def index():
        return "<h1>Welcome to our summarize server!</h1>"
        
    def put(self, running):
        if running != "running":
            return {"text_out": "method not exist", "len_out": 0, "method": f"Error: value at {running}"}, 405

        args = Text_put_args.parse_args()
        # Text = Text_model(id = Text_id, text_in = args['text_in'], views = args['views'], likes = args['likes'])
        
        # result = {"url": args["text_url"], "text_in": args['text_in']}
        result = {}
        try: 
            output = summarizer_textrank_get(args["text_url"], args['text_in'], args["len_out"])

            result["text_out"] = output["sentences"]
            result["len_out"] = output['summary_num_sentences']
            result["method"] = output["method"]
            result["response"] = 200
        except:
            result["response"] = 404
            result["text_out"] = "Error"
            result["len_out"] = 0
            result["method"] = "Error"

        resp = jsonify(result)
        resp.status_code = result['response']
        
        return resp
        
    
# registering resources
api.add_resource(Summarize, "/<string:running>")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001, debug=True)