from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

products = [
    {"id": 1, "name": "Organic Apples", "description": "Fresh and crispy apples from local orchards.", "price": 2.99, "origin": "Washington State", "category": "Fruits"},
    {"id": 2, "name": "Free-range Eggs", "description": "Eggs from happy, free-roaming chickens.", "price": 4.50, "origin": "Local Farm", "category": "Dairy"},
    {"id": 3, "name": "Grass-fed Beef", "description": "Premium beef from grass-fed cattle.", "price": 12.99, "origin": "Midwest Pastures", "category": "Meat"},
    {"id": 4, "name": "Artisanal Cheese", "description": "Hand-crafted cheese from traditional recipes.", "price": 8.75, "origin": "Wisconsin Dairy", "category": "Dairy"}
]

@app.route('/')
def home():
    return render_template('home.html', title="Home", content="Welcome to FarmFresh Tester!")

@app.route('/products')
def product_list():
    categories = set(product['category'] for product in products)
    return render_template('products.html', title="Our Products", products=products, categories=categories)

@app.route('/api/products')
def api_products():
    search = request.args.get('search', '').lower()
    category = request.args.get('category', '')
    filtered_products = [p for p in products if (search in p['name'].lower() or search in p['description'].lower()) 
                         and (not category or p['category'] == category)]
    return jsonify(filtered_products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return render_template('product_detail.html', title=product['name'], product=product)
    return "Product not found", 404

if __name__ == '__main__':
    app.run(debug=True)