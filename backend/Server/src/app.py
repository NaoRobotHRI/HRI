import flask
from flask import Flask, request
from quiz_manager import QuizManager
import os
import argparse

# main Flask app
app = Flask(__name__)

# HRI quiz manager
manager = None


@app.route('/')
def index():
    return 'index'

@app.route('/get_question', methods=['POST', 'GET'])
def get_question():
    if 'idx' in request.args:
        idx = request.args.get('idx')
    else:
        idx = None
    idx_text = f' idx={idx}' if idx != None else ''
    print(f'backend got get_question request!{idx_text}')
    return create_response(manager.get_question(idx))


@app.route('/submit_answer', methods=['POST', 'GET'])
def submit_answer():
    answer = request.args.get('answer')
    print(f'backend got submit_answer request! answer={answer}')
    return create_response(manager.submit_answer(answer))


@app.route('/get_hint', methods=['POST', 'GET'])
def get_hint():
    print('backend got get_hint request!')
    return create_response(manager.get_hint())

def create_response(msg):
    msg = flask.jsonify(msg)
    resp = flask.make_response(msg)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def flask_main():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', manager.backend_port)))

def manager_main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--no_brain', default=False, action='store_true')
    args = parser.parse_args()

    global manager
    manager = QuizManager(brain=not args.no_brain)

def main():
    manager_main()
    flask_main()


if __name__ == '__main__':
    main()
