from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def index():
    # передаём переменные в шаблон
    title = "Мой первый Flask + Bootstrap"
    return render_template("index.html", title=title)

@app.route("/sum")
def sum_ab():
    a = request.args.get("a", type=float, default=0)
    b = request.args.get("b", type=float, default=0)
    result = a + b
    # покажем результат на той же странице (или отдельной)
    return render_template(
        "index.html",
        title="Суммируем числа",
        a=a, b=b, result=result
    )

if __name__ == "__main__":
    print(app.url_map)  # полезно видеть зарегистрированные маршруты
    app.run(debug=True)
