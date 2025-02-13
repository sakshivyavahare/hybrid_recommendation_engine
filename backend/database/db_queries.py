from database.db_connection import get_pg_connection, close_pg_connection

# Fetch user details
def get_user_by_id(user_id):
    conn = get_pg_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
            user = cur.fetchone()
        return user
    except Exception as e:
        print("Error fetching user:", e)
        return None
    finally:
        close_pg_connection(conn)

# Fetch product details
def get_product_by_id(product_id):
    conn = get_pg_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM products WHERE product_id = %s;", (product_id,))
            product = cur.fetchone()
        return product
    except Exception as e:
        print("Error fetching product:", e)
        return None
    finally:
        close_pg_connection(conn)

# Log user interactions (clicks, purchases, etc.)
def log_interaction(user_id, product_id, interaction_type):
    conn = get_pg_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO interactions (user_id, product_id, {interaction_type})
                VALUES (%s, %s, 1)
                ON CONFLICT (user_id, product_id) 
                DO UPDATE SET {interaction_type} = interactions.{interaction_type} + 1;
            """.format(interaction_type=interaction_type), (user_id, product_id))
        conn.commit()
    except Exception as e:
        print("Error logging interaction:", e)
    finally:
        close_pg_connection(conn)
