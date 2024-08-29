from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to FarmFresh Tester!"

@app.route('/reports/<path:path>')
def send_report(path):
    return send_from_directory('reports', path)

if __name__ == '__main__':
    app.run(debug=True)
