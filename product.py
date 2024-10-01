class Product():
    def __init__(self, product_id: str, name: str,  expiration_date: str,
                    used_for: list[str], calibration_date: list[str],
                    product_doc: file_path, calibration_doc: list[file_path],
                    sent: bool = False, info: str ="") -> None:
        self.product_id = product_id
        self.name = name
        self.expiration_date = expiration_date
        self.used_for = used_for
        self.calibration_date = calibration_date
        self.product_doc = product_doc
        self.calibration_doc = calibration_doc
        self.sent = sent
        self.info = info

    def check_expiration_date (self, expiration_date: str) -> bool:
        try:
            if expiration_date != "":
                datetime.strptime(expiration_date, '%d-%m-%Y')
        except Exception as e:
            self.logg(f"Tried to load Log with no valid date format. \n {e}",
                      __file__,
                      inspect.currentframe().f_lineno)
            log_text.insert('1.0',"Date format not valid. Try dd-mm-yyyy")

    def check_path (self, file_path: path) -> bool:
        if file_path:
            return True
        else:
            return False

