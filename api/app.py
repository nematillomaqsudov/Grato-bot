from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)


# ===== MODELS =====
class Item(BaseModel):
    user_id: int
    item: str


class Order(BaseModel):
    user_id: int


# ===== ADD =====
@app.post("/cart/add")
def add(item: Item):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO cart (user_id, item) VALUES (%s, %s)",
        (item.user_id, item.item)
    )

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "ok"}


# ===== REMOVE =====
@app.post("/cart/remove")
def remove(item: Item):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM cart
        WHERE id = (
            SELECT id FROM cart
            WHERE user_id=%s AND item=%s
            LIMIT 1
        )
    """, (item.user_id, item.item))

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "ok"}


# ===== GET CART =====
@app.get("/cart/{user_id}")
def get_cart(user_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT item FROM cart WHERE user_id=%s",
        (user_id,)
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [r[0] for r in rows]


# ===== ORDER =====
@app.post("/order")
def order(order: Order):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT item FROM cart WHERE user_id=%s",
        (order.user_id,)
    )

    items = [r[0] for r in cur.fetchall()]

    cur.execute(
        "DELETE FROM cart WHERE user_id=%s",
        (order.user_id,)
    )

    conn.commit()
    cur.close()
    conn.close()

    return {
        "status": "ordered",
        "items": items
    }
