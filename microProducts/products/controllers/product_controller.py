from flask import Blueprint, jsonify, request
from products.models.product_model import Product

product_controller = Blueprint('product_controller', __name__)

@product_controller.route('/api/products', methods=['GET'])
def get_all_products():
    products = Product.get_all()
    return jsonify(products)

@product_controller.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.get_by_id(product_id)
    if product:
        return jsonify(product)
    return jsonify({'message': 'Producto no encontrado'}), 404

@product_controller.route('/api/products/update_stock', methods=['POST'])
def update_stock():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    
    if not product_id or not quantity:
        return jsonify({'message': 'Datos incompletos'}), 400

    if Product.update_stock(product_id, quantity):
        return jsonify({'message': 'Stock actualizado exitosamente'}), 200
    else:
        return jsonify({'message': 'Error al actualizar el stock o stock insuficiente'}), 400
