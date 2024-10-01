import mysql.connector
import time
import os
from mysql.connector import errorcode
from datetime import datetime
from datetime import date
from datetime import timedelta
from log import Log
from credentials import credentials

class Database (Log):
    def __init__(self) -> None:
        super().__init__()
        self.today: str = datetime.now().strftime("%d_%m_%y")
        self.config: dict[str, str] = credentials

    def create_connection(self, host: str, user:str,
                          password: str, database: str, port: str) -> mysql.connector.connect:
        connection = None
        try:
            #print(f"{user=}__{password=}__{host=}__{database=}__{port=}")
            connection = mysql.connector.connect(
                user = user,
                password = password,
                host = host,
                database = database,
                port = port
            )
            print("Connection to MySQL DB successful")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        return connection

    def connect_to_mysql(self, config, attempts=3, delay=2) -> mysql.connector.connect :
        attempt = 1
        # Implement a reconnection routine
        while attempt < attempts + 1:
            try:
                return self.create_connection(**config)
            except (mysql.connector.Error, IOError) as err:
                if (attempts is attempt):
                    # Attempts to reconnect failed; returning None
                    self.logger.info("Failed to connect, exiting without a connection: %s", err)
                    return None
                self.logger.info(
                    "Connection failed: %s. Retrying (%d/%d)...",
                    err,
                    attempt,
                    attempts-1,
                )
                # progressive reconnect delay
                time.sleep(delay ** attempt)
                attempt += 1
        return None

    def create_database(self, cursor, db_name: str):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def create_table(self, cursor, table: str, val_names: list[str],
                     val_types: list[str])-> None:#, val_contents: list[str])
        TABLES = {}
        TABLES['employees'] = (
            "CREATE TABLE `employees` ("
            "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
            "  `birth_date` date NOT NULL,"
            "  `first_name` varchar(14) NOT NULL,"
            "  `last_name` varchar(16) NOT NULL,"
            "  `gender` enum('M','F') NOT NULL,"
            "  `hire_date` date NOT NULL,"
            "  PRIMARY KEY (`emp_no`)"
            ") ENGINE=InnoDB")

        TABLES['departments'] = (
            "CREATE TABLE `departments` ("
            "  `dept_no` char(4) NOT NULL,"
            "  `dept_name` varchar(40) NOT NULL,"
            "  PRIMARY KEY (`dept_no`), UNIQUE KEY `dept_name` (`dept_name`)"
            ") ENGINE=InnoDB")

        TABLES['salaries'] = (
            "CREATE TABLE `salaries` ("
            "  `emp_no` int(11) NOT NULL,"
            "  `salary` int(11) NOT NULL,"
            "  `from_date` date NOT NULL,"
            "  `to_date` date NOT NULL,"
            "  PRIMARY KEY (`emp_no`,`from_date`), KEY `emp_no` (`emp_no`),"
            "  CONSTRAINT `salaries_ibfk_1` FOREIGN KEY (`emp_no`) "
            "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
            ") ENGINE=InnoDB")

        TABLES['dept_emp'] = (
            "CREATE TABLE `dept_emp` ("
            "  `emp_no` int(11) NOT NULL,"
            "  `dept_no` char(4) NOT NULL,"
            "  `from_date` date NOT NULL,"
            "  `to_date` date NOT NULL,"
            "  PRIMARY KEY (`emp_no`,`dept_no`), KEY `emp_no` (`emp_no`),"
            "  KEY `dept_no` (`dept_no`),"
            "  CONSTRAINT `dept_emp_ibfk_1` FOREIGN KEY (`emp_no`) "
            "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
            "  CONSTRAINT `dept_emp_ibfk_2` FOREIGN KEY (`dept_no`) "
            "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
            ") ENGINE=InnoDB")

        TABLES['dept_manager'] = (
            "  CREATE TABLE `dept_manager` ("
            "  `emp_no` int(11) NOT NULL,"
            "  `dept_no` char(4) NOT NULL,"
            "  `from_date` date NOT NULL,"
            "  `to_date` date NOT NULL,"
            "  PRIMARY KEY (`emp_no`,`dept_no`),"
            "  KEY `emp_no` (`emp_no`),"
            "  KEY `dept_no` (`dept_no`),"
            "  CONSTRAINT `dept_manager_ibfk_1` FOREIGN KEY (`emp_no`) "
            "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
            "  CONSTRAINT `dept_manager_ibfk_2` FOREIGN KEY (`dept_no`) "
            "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
            ") ENGINE=InnoDB")

        TABLES['titles'] = (
            "CREATE TABLE `titles` ("
            "  `emp_no` int(11) NOT NULL,"
            "  `title` varchar(50) NOT NULL,"
            "  `from_date` date NOT NULL,"
            "  `to_date` date DEFAULT NULL,"
            "  PRIMARY KEY (`emp_no`,`title`,`from_date`), KEY `emp_no` (`emp_no`),"
            "  CONSTRAINT `titles_ibfk_1` FOREIGN KEY (`emp_no`)"
            "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
            ") ENGINE=InnoDB")

        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

    def add_employee(self, cnx, cursor,
                     first_name, last_name, hire_date, gender, birth_date) -> None:
        add_employee = ("INSERT INTO employees "
               "(first_name, last_name, hire_date, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")
        data_employee = (first_name, last_name, hire_date, gender, birth_date)

        # Insert new employee
        cursor.execute(add_employee, data_employee)
        emp_no = cursor.lastrowid

        # Make sure data is committed to the database
        cnx.commit()

    def add_salary(self, cnx, cursor,
                    emp_no: str, salary: int, from_date: date, to_date: date) -> None:
        add_salary = ("INSERT INTO salaries "
              "(emp_no, salary, from_date, to_date) "
              "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")
        # Insert salary information
        data_salary = {
        'emp_no': emp_no,
        'salary': salary,
        'from_date': from_date,
        'to_date': to_date,
        }
        # Insert new salary
        cursor.execute(add_salary, data_salary)
        # Make sure data is committed to the database
        cnx.commit()

    def describe_table(self, table: str) -> None:
        show_table_query: str = f"DESCRIBE {table}"
        connection = self.connect_to_mysql(self.config)
        with connection.cursor() as cursor:
            cursor.execute(show_table_query)
            # Fetch rows from last executed query
            result = cursor.fetchall()
            for row in result:
                print(row)

    def delete_table(self, table: str) -> None:
        drop_table_query = f"DROP TABLE {table}"
        connection = self.connect_to_mysql(self.config)
        with connection.cursor() as cursor:
            cursor.execute(drop_table_query)

    def select_table(self, cursor, table: str) -> None:
        query: str = (
            "SELECT * "
            f"FROM {table}"
        )
        cursor.execute(query)
        for (a) in cursor:
            print(a)

    def select_exact_data(self, table: str, columns: list[str],
                          value_col: str, value: any) -> None:
        select_query: str = """
            SELECT """
        for column in columns:
            select_query += f"""{column} """
            if column != columns[-1]:
                select_query += ","
        select_query += f"""FROM {table}
                        WHERE {value_col} = {value}"""

        connection = self.connect_to_mysql(self.config)
        if connection and connection.is_connected():
            with connection.cursor() as cursor:
                cursor.execute(select_query)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            connection.close()
        else:
            print("Could not connect")

    def check_date(self, days: int, sent: bool) -> bool:
        today = date.today()
        if today >= (today - timedelta (days)) and not sent:
            return True
        #elif today >= (today - timedelta (days)) and sent:
            #answer: bool = self.ask_to_send()
            #return answer
        else:
            return False
        #check_sent_mail(product_contact, product_cc, product_from, product_msg)

    def update_expiration_date(self, new_date: str) -> None:
        try:
            if new_date != "":
                datetime.strptime(new_date, '%d-%m-%Y')
        except Exception as e:
            self.logger(f"Tried to load Log with no valid date format. \n {e}")

    def check_db(self, product_id: str = None, name: str = None, expiration_date: str = None,
                used_for: list[str] = None, calibration_date: list[str] = None,
                product_doc: os.path = None, calibration_doc: list[os.path] = None,
                sent: bool = False, info: str = None) -> bool:
        table = "test_table"
        found: bool = False
        if product_id:
            self.select_table(table, [product_id])
        elif name:
            self.select_table(table, [name])
        elif expiration_date:
            self.select_table(table, [expiration_date])
        elif used_for:
            self.select_table(table, [used_for])
        elif calibration_date:
            self.select_table(table, [calibration_date])
        elif product_doc:
            self.select_table(table, [product_doc])
        elif calibration_doc:
            self.select_table(table, [calibration_doc])
        elif sent:
            self.select_table(table, [sent])
        elif info:
            self.select_table(table, [info])
        else:
            print("No value introduced")

    def add_product(self, product_id: str, name: str, expiration_date: str,
                    used_for: list[str], calibration_date: list[str], product_doc: os.path,
                    calibration_doc: list[os.path], sent: bool = False) -> None:
        if product_id and name:
            valid_entry: bool = self.check_db(product_id, name)
            if valid_entry and expiration_date and len(used_for)>0 and len(calibration_date)>0:
                pass
                #add product to DB
            else:
                pass
                #tag text: ID already exists on DB, please, check input data
        else:
            pass
            #tag text: ID or NAME are empty, please, check input data

    def main(self):
        table = "test_calibration"
        val_names = ["name",  "expiration_date", "used_for",
                    "calibration_date", "product_doc", "calibration_doc"]
        val_types = ["VARCHAR",  "DATE", "VARCHAR",
                    "DATE", "VARCHAR", "VARCHAR"]
        cnx: mysql.connector.connect  = self.connect_to_mysql(self.config)
        cursor = cnx.cursor()
        self.create_table(cursor, table, val_names, val_types)


        tomorrow = datetime.now().date() + timedelta(days=1)
        #self.add_employee(cnx, cursor, 'Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))
        #self.add_salary(cnx, cursor, cursor.lastrowid, 50000, tomorrow, date(9999, 1, 1))
        self.select_table(cursor, "employees")
        cursor.close()
        cnx.close()
        self.delete_table(table)



if __name__ == '__main__':
    main_process = Database()
    main_process.main()
