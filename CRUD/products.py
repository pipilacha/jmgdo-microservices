from flask import Flask, jsonify, request
import json
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask("Product Server")
CORS(app)

swagger_bp = get_swaggerui_blueprint(
    '/products/docs',  # the path where the docs will be
    'http://127.0.0.1:5000/static/swagger.json',  # where the swagger file is served
    config={'app_name': "Products microservice"}  # Name of the swagger
)

app.register_blueprint(swagger_bp)

PRODUCTS = [
    {'id': 143, 'name': 'Notebook', 'price': 5.49},
    {'id': 144, 'name': 'Black pen', 'price': 1.99},
]


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/products", methods=['POST'])
def save_products():
    print(request.get_data())
    body = request.get_json()

    for p in body:
        print("p", p)
        PRODUCTS.append(p)
    return {"message": f'Added {len(body)} products'}, 201


@app.route("/products", methods=['GET'])
def get_products():
    return jsonify(PRODUCTS)


@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    id = int(id)
    product = [x for x in PRODUCTS if x["id"] == id][0]
    return jsonify(product)


@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    id = int(id)
    updated_product = json.loads(request.data)
    product = [x for x in PRODUCTS if x["id"] == id][0]
    for key, value in updated_product.items():
        product[key] = value
    return '', 204


@app.route('/products/<id>', methods=['DELETE'])
def remove_product(id):
    id = int(id)
    product = [x for x in PRODUCTS if x["id"] == id][0]
    PRODUCTS.remove(product)

    return '', 204


if __name__ == "__main__":
    app.run(debug=True)

# flask --app server run --debug

"""
curl -X 'GET' \                             this tells curl to use get method
'http://127.0.0.1:5000/products' \          the url
-H 'accept: application/json \              this sets headers in the request

in powershell: since curl just call Invoke-WebRquest not real curl

curl.exe -X 'GET' `
>> 'http://127.0.0.1:5000/products' `
>> -H 'accept: application/json'

"""

app.run(port=5000,debug=True)
