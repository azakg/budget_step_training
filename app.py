from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "First page"

@app.route("/hello/<name>")
def hello(name):
    return f"Hello, {name}!"

@app.route("/square/<int:n>")
def square(n: int):
    return f"{n}^2 = {n*n}"

if __name__ == '__main__':
    app.run(debug=True)