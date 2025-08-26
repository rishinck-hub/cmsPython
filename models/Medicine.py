from datetime import date
from services.MedicineService import MedicineService  # Import the service above

class Medicine:
    """A class representing a medicine product with accompanying validation."""

    def __init__(
        self,
        medicineid=None,
        medicinename="unknown",
        manufacturedate=None,  # Accept as string for parsing
        expirydate=None,       # Accept as string for parsing
        unitquantiy=0,
        unitid=None,
        unitprice=None,
        medicinecategoryid=None,
    ):
        self.__medicineid = medicineid
        self.medicinename = medicinename  # Calls the setter with validation
        self.__unitprice = unitprice
        self.__unitquantiy = unitquantiy
        self.__unitid = unitid
        self.__medicinecategoryid = medicinecategoryid

        # Parse and validate dates
        today = date.today()
        if manufacturedate:
           # mfg = MedicineService.parse_date_str(manufacturedate)
            mfg = manufacturedate
            self.__manufacturedate = MedicineService.validate_manufacturedate(mfg)
        else:
            self.__manufacturedate = today

        if expirydate:
            #exp = MedicineService.parse_date_str(expirydate)
            exp = expirydate
            self.__expirydate = MedicineService.validate_expirydate(exp, self.__manufacturedate)
        else:
            self.__expirydate = today

        

    # Property: medicine_id
    @property
    def medicine_id(self):
        return self.__medicineid

    @medicine_id.setter
    def medicine_id(self, value):
        self.__medicineid = value

    # Property: medicinename
    @property
    def medicinename(self):
        return self.__medicinename

    @medicinename.setter
    def medicinename(self, value):
        validated_name = MedicineService.validate_medicinename(value)
        self.__medicinename = validated_name

    # Property: unit_price
    @property
    def unit_price(self):
        return self.__unitprice

    @unit_price.setter
    def unit_price(self, value):
        self.__unitprice = value

    # Property: unit_quantity
    @property
    def unit_quantity(self):
        return self.__unitquantiy

    @unit_quantity.setter
    def unit_quantity(self, value):
        self.__unitquantiy = value

    # Property: unit_id
    @property
    def unit_id(self):
        return self.__unitid

    @unit_id.setter
    def unit_id(self, value):
        self.__unitid = value

    # Property: medicine_category_id
    @property
    def medicine_category_id(self):
        return self.__medicinecategoryid

    @medicine_category_id.setter
    def medicine_category_id(self, value):
        self.__medicinecategoryid = value

    # Property: manufacture_date
    @property
    def manufacture_date(self):
        return self.__manufacturedate

    @manufacture_date.setter
    def manufacture_date(self, date_str):
        #mfg = MedicineService.parse_date_str(date_str)
        mfg = MedicineService.parse_date_str(date_str)
        self.__manufacturedate = MedicineService.validate_manufacturedate(mfg)

    # Property: expiry_date
    @property
    def expiry_date(self):
        return self.__expirydate

    @expiry_date.setter
    def expiry_date(self, date_str):
        exp = MedicineService.parse_date_str(date_str)
        self.__expirydate = MedicineService.validate_expirydate(exp, self.__manufacturedate)

    # Property: is_active
    
    
    def __str__(self):
        return (
            f"MedicineID: {self.__medicineid:<5} | "
            f"Name: {self.__medicinename:<20} | "
            f"UnitQty: {self.__unitquantiy:<3} | "
            f"UnitID: {self.__unitid:<5} | "
            f"UnitPrice: {self.__unitprice:<8} | "
            f"CategoryID: {self.__medicinecategoryid:<5} | "
            f"Manufacture: {self.__manufacturedate} | "
            f"Expiry: {self.__expirydate} | "
        )
