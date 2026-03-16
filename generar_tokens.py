"""
generar_tokens.py
Genera tokens únicos para todos los pedidos que no tienen uno válido.
Ejecutar UNA SOLA VEZ, luego borrar el archivo.

Uso:
    python generar_tokens.py
"""

import uuid
import psycopg2
import psycopg2.extras

conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="Mortadela705",
    database="sena_food",
    port="5432"
)

try:
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        # Obtener todos los pedidos
        cursor.execute("SELECT id FROM pedidos ORDER BY id")
        pedidos = cursor.fetchall()

    for p in pedidos:
        pedido_id = p["id"]
        token = "TK-" + uuid.uuid4().hex[:6].upper()

        with conn.cursor() as cursor:
            # Eliminar token anterior si existe
            cursor.execute("DELETE FROM tokens_pedido WHERE pedido_id = %s", (pedido_id,))
            # Insertar token nuevo
            cursor.execute("""
                INSERT INTO tokens_pedido (pedido_id, token, estado, fecha_generacion)
                VALUES (%s, %s, 'activo', NOW())
            """, (pedido_id, token))
            # Actualizar campo token en pedidos
            cursor.execute("UPDATE pedidos SET token = %s WHERE id = %s", (token, pedido_id))

        conn.commit()
        print(f"✅ Pedido {pedido_id} → Token: {token}")

    print(f"\n✅ {len(pedidos)} tokens generados correctamente.")

except Exception as e:
    conn.rollback()
    print(f"❌ Error: {e}")
finally:
    conn.close()