from typing import List, Optional
from models.Medicine import Medicine
from dao.MedicineDao import MedicineDaoService
from db.db_connection import DBConnection

class MedicineDaoDb(MedicineDaoService):
    # SQL Query Templates
    DISPLAY_ALL = "SELECT * FROM medicines"
    #DISPLAY_ALL = "SELECT medicineid,medicinename,DATE_FORMAT(manufacturedate, '%d-%m-%Y') AS manufacturedate,DATE_FORMAT(expirydate, '%d-%m-%Y') AS expirydate,unitquantiy,unitid,unitprice,medicinecategoryid FROM medicines";
    INSERT_MEDICINE = (
        "INSERT INTO medicines "
        "(medicinename, manufacturedate, expirydate, unitquantiy, unitid, unitprice, medicinecategoryid) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    )
    FIND_BY_ID = "SELECT * FROM medicines WHERE medicineid = %s"
    UPDATE_MEDICINE = (
        "UPDATE medicines SET medicinename=%s, unitprice=%s WHERE medicineid=%s"
    )
    DISABLE_MEDICINE = "UPDATE medicines SET isactive='N' WHERE medicineid=%s"
    SEARCH_MEDICINE = (
        "SELECT * FROM medicines "
        "WHERE medicinename LIKE %s OR categoryid LIKE %s"
    )
    APPLY_GST_PROC = "CALL apply_gst_to_medicine(%s, %s, @success_flag)"
    SELECT_GST_FLAG = "SELECT @success_flag"

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def insert(self, med: Medicine) -> bool:
        cursor = self.conn.cursor()
        try:
            # Corrected insertion: Ensure correct number of parameters are passed
            cursor.execute(self.INSERT_MEDICINE, (
                med.medicinename,           
                med.manufacturedate,       
                med.expirydate,            
                med.unitquantiy,           
                med.unitid,                 
                med.unitprice,              
                med.medicinecategoryid      
            ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print(f"Insert error: {e}")
            return False
        finally:
            cursor.close()

    def display_all(self) -> List[Medicine]:
        meds = []
        cursor = self.conn.cursor(dictionary=True)
        try:
            cursor.execute(self.DISPLAY_ALL)
            for row in cursor.fetchall():
                meds.append(Medicine(
                    medicineid=row["medicineid"],
                    medicinename=row["medicinename"],
                    manufacturedate=row["manufacturedate"],
                    expirydate=row["expirydate"],
                    unitquantiy=row["unitquantiy"],
                    unitid=row["unitid"],
                    unitprice=row["unitprice"],
                    medicinecategoryid=row["medicinecategoryid"],
            ))
        except Exception as e:
            print(f"Fetch error: {e}")
        finally:
            cursor.close()
        return meds

    def find_by_id(self, medicineid: int) -> Optional[Medicine]:
        cursor = self.conn.cursor(dict)
        try:
            cursor.execute(self.FIND_BY_ID, (medicineid,))
            row = cursor.fetchone()
            if row:
                return Medicine(
                    medicineid=row["medicineid"],
                    medicinename=row["medicinename"],
                     manufacturedate=row["manufacturedate"],
                     expirydate=row["expirydate"],
                     unitquantiy=row["unitquantiy"],
                     unitid=row["unitid"],
                     unitprice=row["unitprice"],
                    
                    
                    medicinecategoryid=row["medicinecategoryid"],
                )
        except Exception as e:
            print(f"Find by ID error: {e}")
        finally:
            cursor.close()
        return None

    def update(self, med: Medicine, medicineid: int) -> bool:
        cursor = self.conn.cursor()
        try:
            cursor.execute(self.UPDATE_MEDICINE, (
                med.medicinename,  # Access property directly
                med.unitprice,
                medicineid,
            ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print(f"Update error: {e}")
            return False
        finally:
            cursor.close()

    def disable(self, medicineid: int) -> bool:
        cursor = self.conn.cursor()
        try:
            cursor.execute(self.DISABLE_MEDICINE, (medicineid,))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print(f"Disable error: {e}")
            return False
        finally:
            cursor.close()

    def search(self, query: str) -> List[Medicine]:
        meds, cursor = [], self.conn.cursor(dict)
        try:
            pattern = f"%{query}%"
            cursor.execute(self.SEARCH_MEDICINE, (pattern, pattern))
            for row in cursor.fetchall():
                meds.append(Medicine(
                    medicineid=row["medicineid"],
                    medicinename=row["medicinename"],
                     manufacturedate=row["manufacturedate"],
                     expirydate=row["expirydate"],
                    unitquantiy=row["unitquantiy"],
                     unitid=row["unitid"],
                     unitprice=row["unitprice"],
                    
                    
                    medicinecategoryid=row["medicinecategoryid"],
                ))
        except Exception as e:
            print(f"Search error: {e}")
        finally:
            cursor.close()
        return meds

    def apply_gst(self, medicineid: int, gst_percent: float) -> bool:
        cursor = self.conn.cursor()
        try:
            cursor.execute(self.APPLY_GST_PROC, (medicineid, gst_percent))
            cursor.execute(self.SELECT_GST_FLAG)
            flag = cursor.fetchone().get("@success_flag") if cursor.rowcount else None
            self.conn.commit()
            return bool(flag)
        except Exception as e:
            print(f"GST SP error: {e}")
            return False
        finally:
            cursor.close()
