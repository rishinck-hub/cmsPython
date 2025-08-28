from typing import List, Optional
from models.MedicineStock import MedicineStock
from dao.MedicineStockDao import MedicineStockDaoService
from db.db_connection import DBConnection

class MedicineStockDaoDb(MedicineStockDaoService):
    # SQL Query Templates
    DISPLAY_ALL = "SELECT * FROM medicinestock where medicinestockid is not null"
    INSERT_STOCK = (
        "INSERT INTO medicinestock "
        "(stockhand, reorderlevel, purchase, issuance, medicineid, createddate) "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )
    FIND_BY_ID = "SELECT * FROM medicinestock WHERE medicinestockid = %s"
    UPDATE_STOCK = (
        "UPDATE medicinestock SET stockhand = %s, reorderlevel = %s, purchase = %s, issuance = %s WHERE medicinestockid = %s"
    )
    DISABLE_STOCK = "UPDATE medicinestock SET isactive = 'N' WHERE medicinestockid = %s"
    SEARCH_STOCK = (
        "SELECT * FROM medicine_stock "
        "WHERE batchnumber LIKE %s OR medicineid LIKE %s"
    )

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def insert(self, stock: MedicineStock) -> bool:
        cursor = self.conn.cursor()
        try:
            # Corrected insertion: Ensure correct number of parameters are passed
            cursor.execute(self.INSERT_STOCK, (
                
                stock.stockhand,
                stock.reorderlevel,
                stock.purchase,
                stock.issuance,
                stock.medicineid,
                stock.createddate
            ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print(f"Insert error: {e}")
            return False
        finally:
            cursor.close()

    def display_all_stock(self) -> List[MedicineStock]:
        stocks = []
        cursor = self.conn.cursor(dictionary=True)
        try:
            cursor.execute(self.DISPLAY_ALL)
            for row in cursor.fetchall():
                stocks.append(MedicineStock(
                    medicinestockid=row["medicinestockid"],
                    stockhand=row["stockhand"],
                    reorderlevel=row["reorderlevel"],
                    purchase=row["purchase"],
                    issuance=row["issuance"],
                    medicineid=row["medicineid"],
                    createddate=row["createddate"]
                ))
        except Exception as e:
            print(f"Fetch error: {e}")
        finally:
            cursor.close()
        return stocks

    def find_by_id(self, stockid: int) -> Optional[MedicineStock]:
        cursor = self.conn.cursor(dictionary=True)
        try:
            cursor.execute(self.FIND_BY_ID, (stockid,))
            row = cursor.fetchone()
            if row:
                return MedicineStock(
                    medicinestockid=row["medicinestockid"],
                    stockhand=row["stockhand"],
                    reorderlevel=row["reorderlevel"],
                    purchase=row["purchase"],
                    issuance=row["issuance"],
                    medicineid=row["medicineid"],
                    createddate=row["createddate"]
                )
        except Exception as e:
            print(f"Find by ID error: {e}")
        finally:
            cursor.close()
        return None

    def update_stock(self, stock: MedicineStock, stockid: int) -> bool:
        cursor = self.conn.cursor()
        try:
            cursor.execute(self.UPDATE_STOCK, (
                stock.stockhand,
                stock.reorderlevel,
                stock.purchase,
                stock.issuance,
                stockid
            ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print(f"Update error: {e}")
            return False
        finally:
            cursor.close()

    def disable(self, stockid: int) -> bool:
        cursor = self.conn.cursor()
        try:
            cursor.execute(self.DISABLE_STOCK, (stockid,))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print(f"Disable error: {e}")
            return False
        finally:
            cursor.close()

    def search(self, query: str) -> List[MedicineStock]:
        stocks, cursor = [], self.conn.cursor(dictionary=True)
        try:
            pattern = f"%{query}%"
            cursor.execute(self.SEARCH_STOCK, (pattern, pattern))
            for row in cursor.fetchall():
                stocks.append(MedicineStock(
                    stockid=row["stockid"],
                    medicineid=row["medicineid"],
                    quantity=row["quantity"],
                    batchnumber=row["batchnumber"],
                    stockdate=row["stockdate"],
                    expirydate=row["expirydate"]
                ))
        except Exception as e:
            print(f"Search error: {e}")
        finally:
            cursor.close()
        return stocks
