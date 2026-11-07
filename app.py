"""FarmFresh — small, fictional Flask catalog used for software-QA exercises."""
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# In-memory demo data only. No real orders, inventory updates, or payment collection.
products = [
    {"id": 1, "name": "Organic Apples", "description": "Fresh and crispy apples from local orchards.", "price": 2.99, "origin": "Washington State", "category": "Fruits"},
    {"id": 2, "name": "Free-range Eggs", "description": "Eggs from happy, free-roaming chickens.", "price": 4.50, "origin": "Local Farm", "category": "Dairy"},
    {"id": 3, "name": "Grass-fed Beef", "description": "Premium beef from grass-fed cattle.", "price": 12.99, "origin": "Midwest Pastures", "category": "Meat"},
    {"id": 4, "name": "Artisanal Cheese", "description": "Hand-crafted cheese from traditional recipes.", "price": 8.75, "origin": "Wisconsin Dairy", "category": "Dairy"},
]


@app.get("/")
def home():
    return render_template("home.html", title="Home", content="Welcome to FarmFresh Tester!")


@app.get("/about")
def about():
    return render_template("about.html", title="About")


@app.get("/products")
def product_list():
    categories = sorted({product["category"] for product in products})
    return render_template("products.html", title="Products", categories=categories)


@app.get("/api/products")
def api_products():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    if len(search) > 100 or len(category) > 40:
        return jsonify({"error": "Search or category is too long"}), 400

    filtered = [
        item for item in products
        if (not search or search.casefold() in (item["name"] + " " + item["description"]).casefold())
        and (not category or item["category"].casefold() == category.casefold())
    ]
    return jsonify(filtered)


@app.get("/api/products/<int:product_id>")
def api_product_detail(product_id):
    item = next((item for item in products if item["id"] == product_id), None)
    if item is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(item)


@app.get("/product/<int:product_id>")
def product_detail(product_id):
    item = next((item for item in products if item["id"] == product_id), None)
    if item is None:
        return render_template("not_found.html", title="Not Found"), 404
    return render_template("productdetail.html", title=item["name"], product=item)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=False)
