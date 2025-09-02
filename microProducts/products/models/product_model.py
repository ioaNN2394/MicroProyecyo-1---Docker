from db.db import get_db_connection

class Product:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM products")
            result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def get_by_id(product_id):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def update_stock(product_id, quantity_to_reduce):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Primero, asegurarse de que hay stock suficiente
            cursor.execute("SELECT quantity FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            if product and product['quantity'] >= quantity_to_reduce:
                cursor.execute("UPDATE products SET quantity = quantity - %s WHERE id = %s", (quantity_to_reduce, product_id))
                conn.commit()
                conn.close()
                return True
        conn.close()
        return False
