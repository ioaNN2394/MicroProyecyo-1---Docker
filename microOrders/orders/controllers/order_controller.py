from flask import Blueprint, jsonify, request
from orders.models.order_model import Order
import requests
from utils import get_service_url  # <-- 1. Importar la nueva función

order_controller = Blueprint('order_controller', __name__)

# 2. Eliminar la variable de entorno PRODUCT_SERVICE_URL
# PRODUCT_SERVICE_URL = os.environ.get('PRODUCT_SERVICE_URL', 'http://localhost:5002')

@order_controller.route('/api/orders', methods=['GET'])
# ... (get_all_orders y get_order no cambian)
def get_all_orders():
    orders = Order.get_all()
    return jsonify(orders)

@order_controller.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.get_by_id(order_id)
    if order:
        return jsonify(order)
    return jsonify({'message': 'Orden no encontrada'}), 404

@order_controller.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    user_name = data.get('user_name')
    user_email = data.get('user_email')
    products = data.get('products')

    if not user_name or not user_email or not products:
        return jsonify({'message': 'Datos inválidos'}), 400

    product_service_url = get_service_url('products')
    if not product_service_url:
        return jsonify({'message': 'Servicio de productos no disponible'}), 503

    total_venta = 0
    product_details = [] # Guardaremos los detalles de los productos aquí

    for item in products:
        product_id = item.get('id')
        quantity = item.get('quantity')
        
        try:
            response = requests.get(f"{product_service_url}/api/products/{product_id}")
            if response.status_code == 200:
                product_data = response.json()
                if product_data['quantity'] < quantity:
                    return jsonify({'message': f"Stock insuficiente para {product_data['name']}"}), 400
                
                price = product_data['price']
                total_venta += price * quantity
                product_details.append({'id': product_id, 'quantity': quantity, 'price': price})
            else:
                return jsonify({'message': f"Producto con ID {product_id} no encontrado"}), 404
        except requests.exceptions.RequestException:
            return jsonify({'message': 'Error al conectar con el servicio de productos'}), 500
    
    # --- Lógica de creación de la orden ---
    # 1. Crear la entrada principal en la tabla 'orders'
    new_order_id = Order.create(user_name, user_email, total_venta)
    
    # 2. Añadir cada producto a la tabla 'order_items'
    for product in product_details:
        Order.add_item(new_order_id, product['id'], product['quantity'], product['price'])
        # 3. Actualizar el stock (lo movemos aquí para mayor seguridad)
        try:
            update_payload = {'product_id': product['id'], 'quantity': product['quantity']}
            requests.post(f"{product_service_url}/api/products/update_stock", json=update_payload)
        except requests.exceptions.RequestException:
            # En un sistema real, aquí habría que revertir la orden (transacción)
            return jsonify({'message': 'Error crítico al actualizar el stock'}), 500

    return jsonify({'message': 'Orden creada exitosamente', 'total': total_venta}), 201

@order_controller.route('/api/orders/user/<string:username>', methods=['GET'])
def get_orders_by_user(username):
    orders = Order.get_by_username(username)
    return jsonify(orders)
