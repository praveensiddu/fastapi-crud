from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

# In-memory database
items = {}

# Data model
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool

# --------------------------
# POST - Create item
# --------------------------

@app.get("/items/")
def get_items():
    return items

@app.post("/items/")
def create_item(item: Item):
    if item.name in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item.name] = item
    return {"message": "Item created", "item": item}

# --------------------------
# PUT - Full update item
# --------------------------
@app.put("/items/{item_name}")
def update_item(item_name: str, item: Item):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_name] = item
    return {"message": "Item replaced", "item": item}

# --------------------------
# PATCH - Partial update
# --------------------------
@app.patch("/items/{item_name}")
def partial_update_item(item_name: str, updates: dict):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in updates.items():
        if hasattr(items[item_name], key):
            setattr(items[item_name], key, value)
    return {"message": "Item updated", "item": items[item_name]}

# --------------------------
# DELETE - Remove item
# --------------------------
@app.delete("/items/{item_name}")
def delete_item(item_name: str):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = items.pop(item_name)
    return {"message": "Item deleted", "item": deleted_item}


# code starts executing from the main function
if __name__ == "__main__":
    # uvicorn provides the webserver functionality like apache server
    # reload=True tells unicorm to reload the python script if it changes.
    uvicorn.run("fastapi-crud:app", host="127.0.0.1", port=8000, reload=True)