import io

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from contextlib import redirect_stdout
from api.ceci.tokenizer import *
from api.ceci.cfg import *
from api.ceci.evaluate import *

application = Flask(__name__, static_folder="client/build/static", template_folder="client/build")
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'

def preprocess(line):
  line = line.replace("(", " ( ")
  line = line.replace(")", " ) ")
  line = line.replace("-", " - ")
  line = line.replace(",", " , ")
  line = line.replace(";", " ; ")
  line = line.replace("\"", " \" ")
  return line

@application.route("/")
def main():
    return render_template('index.html')

@application.route("/run-code", methods=['POST'])
@cross_origin()
def run_code():
    payload = request.json["program"]
    program = []
    for line in payload.split('\n'):
      line = preprocess(line)
      for word in line.split():
        program.append(word)

    try:
        tokenized = tokenize(program)
        parsetree = ParseTree(tokenized)
        parsed = parsetree.build()
        evaluator = Evaluator(parsed)
        f = io.StringIO()
        with redirect_stdout(f):
            evaluator.evaluate_tree()
        out = f.getvalue()
    except ReturnValue as r:
        return jsonify({
            'output': out,
            'return': r.value,
        })
    except Exception as e:
        return jsonify({
            'error': e.message
        })
    return jsonify({
        'output': out
    })

if __name__ == "__main__":
    application.debug=True
    application.run()