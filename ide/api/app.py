import io

from flask import Flask, render_template, request, jsonify
from contextlib import redirect_stdout
from ceci.tokenizer import *
from ceci.cfg import *
from ceci.evaluate import *

app = Flask(__name__, static_folder="../client/build/static", template_folder="../client/build")

def preprocess(line):
  line = line.replace("(", " ( ")
  line = line.replace(")", " ) ")
  line = line.replace("-", " - ")
  line = line.replace(",", " , ")
  line = line.replace(";", " ; ")
  line = line.replace("\"", " \" ")
  return line

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/run-code", methods=['POST'])
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
    except (EvaluateException, ParseException, TokenException) as e:
        return jsonify({
            'error': e.message
        })
    return jsonify({
        'output': out
    })


print('Starting Flask!')

app.debug=True
app.run(host='0.0.0.0')