from flask import Flask, abort, redirect, render_template, request, url_for


app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "Увлажняющий крем", "brand": "LUMI", "category": "care", "price": 1290, "position": "18% 74%", "description": "Легкий крем с пантенолом и скваланом для ежедневного ухода."},
    {"id": 2, "name": "Сыворотка с ниацинамидом", "brand": "PURE LAB", "category": "care", "price": 1490, "position": "49% 52%", "description": "Сыворотка выравнивает тон и помогает поддерживать защитный барьер кожи."},
    {"id": 3, "name": "Гель для умывания", "brand": "MELLOW", "category": "care", "price": 890, "position": "70% 28%", "description": "Мягкое очищение без ощущения сухости и стянутости."},
    {"id": 4, "name": "Кремовые румяна", "brand": "GLOW NOTE", "category": "makeup", "price": 1190, "position": "76% 68%", "description": "Полупрозрачный оттенок легко растушевывается и дает естественный финиш."},
    {"id": 5, "name": "Бальзам для губ", "brand": "LUMI", "category": "makeup", "price": 690, "position": "88% 82%", "description": "Питательный бальзам с легким розовым оттенком."},
    {"id": 6, "name": "Тоник с розовой водой", "brand": "PURE LAB", "category": "care", "price": 990, "position": "20% 36%", "description": "Освежающий тоник завершает очищение и подготавливает кожу к уходу."},
]


@app.route("/")
def index():
    return render_template("index.html", products=PRODUCTS[:4])


@app.route("/catalog")
def catalog():
    category = request.args.get("category", "all")
    items = PRODUCTS if category == "all" else [p for p in PRODUCTS if p["category"] == category]
    return render_template("catalog.html", products=items, category=category)


@app.route("/product/<int:product_id>")
def product(product_id):
    item = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if item is None:
        abort(404)
    return render_template("product.html", product=item)


@app.route("/review", methods=["GET", "POST"])
def review():
    errors = []
    values = {"name": "", "product_id": "", "rating": "", "comment": ""}
    if request.method == "POST":
        values = {key: request.form.get(key, "").strip() for key in values}
        if len(values["name"]) < 2:
            errors.append("Укажите имя не короче двух символов.")
        if not values["product_id"].isdigit():
            errors.append("Выберите товар из списка.")
        if values["rating"] not in {"1", "2", "3", "4", "5"}:
            errors.append("Поставьте оценку от 1 до 5.")
        if len(values["comment"]) < 10:
            errors.append("Комментарий должен содержать не менее 10 символов.")
        if not errors:
            item = next((p for p in PRODUCTS if p["id"] == int(values["product_id"])), None)
            if item is None:
                errors.append("Выбранный товар не найден.")
            else:
                return redirect(url_for("review_result", name=values["name"], product=item["name"], rating=values["rating"], comment=values["comment"]))
    return render_template("review_form.html", products=PRODUCTS, errors=errors, values=values)


@app.route("/review/result")
def review_result():
    return render_template(
        "review_result.html",
        name=request.args.get("name", "Гость"),
        product=request.args.get("product", "Товар"),
        rating=request.args.get("rating", "5"),
        comment=request.args.get("comment", "Спасибо за продукт!"),
    )


if __name__ == "__main__":
    app.run(debug=True)
