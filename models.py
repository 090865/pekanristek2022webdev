from database import Base
from sqlalchemy import Integer, Column,Text, String

class Item(Base):
    __tablename__="items"
    itempemasukan=Column(String, primary_key=True)
    pemasukan=Column(Integer, primary_key=True)
    itempengeluaran=Column(String, primary_key=True)
    pengeluaran=Column(Integer, primary_key=True)

    def __repr__(self):
        return f"item pengeluaran={self.pengeluaran} pengeluaran={self.pengeluaran} item pengeluaran{self.itempengeluaran} pengeluaran={self.pengeluaran}"