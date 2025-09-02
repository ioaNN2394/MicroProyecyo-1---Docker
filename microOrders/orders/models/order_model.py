from db.db import get_db_connection

class Order:
    @staticmethod
    def create(user_name, user_email, total):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO orders (userName, userEmail, saleTotal) VALUES (%s, %s, %s)",
                           (user_name, user_email, total))
            new_order_id = cursor.lastrowid  # <-- Obtener el ID de la nueva orden
        conn.commit()
        conn.close()
        return new_order_id  # <-- Devolver el ID

    @staticmethod
    def add_item(order_id, product_id, quantity, price):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                           (order_id, product_id, quantity, price))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        # Primero, obtenemos todas las órdenes del usuario
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM orders WHERE userName = %s ORDER BY date DESC", (username,))
            orders = cursor.fetchall()
        
        # Ahora, para cada orden, obtenemos sus items
        for order in orders:
            with conn.cursor() as cursor:
                # Usamos un JOIN para obtener el nombre del producto
                sql = """
                    SELECT p.name, oi.quantity, oi.price 
                    FROM order_items oi 
                    JOIN products p ON oi.product_id = p.id 
                    WHERE oi.order_id = %s
                """
                cursor.execute(sql, (order['id'],))
                items = cursor.fetchall()
                order['items'] = items # Añadimos la lista de items a la orden

                # Convertimos el Decimal a float para que JSON lo serialice bien
                if 'saleTotal' in order and order['saleTotal'] is not None:
                    order['saleTotal'] = float(order['saleTotal'])

        conn.close()
        return orders
