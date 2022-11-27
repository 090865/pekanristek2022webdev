from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel
from typing import Optional,List, Dict
from database import SessionLocal
import models


app = FastAPI()




class Item(BaseModel):
    itempemasukan: int
    pemasukan: int
    itempengeluaran: int
    pengeluaran: int


    class Config:
        orm_mode=True

db=SessionLocal()
@app.get("/items", response_model=List[Item], status_code=200)
def get_all_item():
    items=db.query(models.Item).all()
    return items


@app.get("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def get_an_item(item_id:int):
    item=db.query(models.Item).filter(models.Item.itempemasukan==item_id).first()
    return item


@app.put("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_an_item(item:Item):
    new_item=models.Item(
        itempemasukan=item.itempemasukan,
        pemasukan=item.pemasukan,
        itempengeluaran=item.itempengeluaran,
        pengeluaran=item.pengeluaran
    )
    db_item=db.query(models.Item).filter(item.itempemasukan==new_item.itempemasukan)

    if db_item is not None:
        raise HTTPException(status_code=400, detail="Item already exists")
    
    db.add(new_item)
    db.commit()
    return new_item

@app.put("/edit/{item_id}",response_model=Item, status_code=status.HTTP_200_OK)
def update_an_item(item_id=int, item=Item):
    item_to_update=db.query(models.Item).filter(models.Item.itempemasukan==item_id).first()

    item_to_update.itempemasukan=Item.itempemasukan   
    item_to_update.pemasukan=Item.pemasukan
    item_to_update.itempengeluaran=Item.itempengeluaran
    item_to_update.pengeluaran=Item.pengeluaran
    db.commit()
    return item_to_update


@app.delete("/item/{item_id}")
def delete_item(item_id:int):
    pass