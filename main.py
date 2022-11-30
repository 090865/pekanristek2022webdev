from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel
from typing import Optional,List, Dict
from database import SessionLocal
import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Item(BaseModel):
    itempemasukan: str
    pemasukan: int
    itempengeluaran: str
    pengeluaran: int


    class Config:
        orm_mode=True

db=SessionLocal()
@app.get("/items", response_model=List[Item], status_code=200)
def get_all_item():
    items=db.query(models.Item).all()
    return items


@app.get("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def get_an_item(item_id:str):
    item=db.query(models.Item).filter(models.Item.itempemasukan==item_id).first()
    return item


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_an_item(item:Item):
    db_item=db.query(models.Item).filter(models.Item.itempengeluaran==item.itempengeluaran).first()

    if db_item is not None:
        raise HTTPException(status_code=400, detail="Item already exists")
    
    new_item=models.Item(
        itempemasukan=item.itempemasukan,
        pemasukan=item.pemasukan,
        itempengeluaran=item.itempengeluaran,
        pengeluaran=item.pengeluaran
    )
    db.add(new_item)
    db.commit()
    return new_item

    

@app.put("/edit/{item_id}",response_model=Item, status_code=status.HTTP_200_OK)
def update_an_item(item:Item, item_id:str):
    item_to_update=db.query(models.Item).filter(models.Item.itempemasukan==item_id).first()
    item_to_update.itempemasukan=item.itempemasukan
    item_to_update.pemasukan=item.pemasukan
    item_to_update.itempengeluaran=item.itempengeluaran
    item_to_update.pengeluaran=item.pengeluaran
    db.commit()
    return item_to_update


@app.delete("/item/{item_id}")
def delete_item(item_id:str):
    item_to_delete=db.query(models.Item).filter(models.Item.itempemasukan==item_id).first()
    if item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details="Resource Not Found")
    db.delete(item_to_delete)
    db.commit()
    return item_to_delete