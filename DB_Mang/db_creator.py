'''CREATE TABLE IF NOT EXISTS DIRECCIONES 
    (FOLIO INT PRIMARY KEY NOT NULL, 
    CALLE CHAR(50) NOT NULL, ----> 'Real 300'
    ADEUDO INT, -----> 320
    ACTIVO CHAR(50), ------> '2023-03-10'
    CONVENIO INT, ---------> 0 | 1 (Boolean)
    COSTO INT --------> 320
    );'''


'''CREATE TABLE IF NOT EXISTS PAGOS
    (ID INT PRIMARY KEY NOT NULL,
    FOLIO INT   -----> DIRECCIONES.FOLIO
    PAGO INT, -----> 640
    FECHA CHAR(50), -----> '2023-02-16'
    );'''


import sqlite3

conn = sqlite3.connect('C:/Tez/Pay_Man_FdeA/main/DB.db')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS DIRECCIONES;")
cur.execute("DROP TABLE IF EXISTS PAGOS;")

cur.execute('''CREATE TABLE DIRECCIONES 
    (DIR_ID INTEGER PRIMARY KEY, 
    CALLE TEXT NOT NULL,
    COSTO INTEGER,
    BALANCE INTEGER 
    );''')

cur.execute('''CREATE TABLE PAGOS
    (PAY_ID INTEGER PRIMARY KEY,
    DIR_ID INTEGER NOT NULL, 
    PAGO INTEGER,
    FECHA TEXT,
    FOREIGN KEY (DIR_ID) 
        REFERENCES DIRECCIONES (DIR_ID)
    );''')

cur.execute("INSERT INTO DIRECCIONES (CALLE, COSTO, BALANCE) VALUES ('Real 300', 320, 0);")

cur.execute("INSERT INTO DIRECCIONES (CALLE, COSTO, BALANCE) VALUES ('Alta 132', 320, -320);")

cur.execute("INSERT INTO DIRECCIONES (CALLE, COSTO, BALANCE) VALUES ('Linda 001', 300, 0);")

cur.execute("INSERT INTO DIRECCIONES (CALLE, COSTO, BALANCE) VALUES ('Dulce 002', 320, -640);")

cur.execute("INSERT INTO DIRECCIONES (CALLE, COSTO, BALANCE) VALUES ('Azul 003', 320, 0);")

cur.execute("INSERT INTO PAGOS (DIR_ID, PAGO, FECHA) VALUES (1, 320, '2023-02-10');")

cur.execute("INSERT INTO PAGOS (DIR_ID, PAGO, FECHA) VALUES (2, 320, '2023-01-10');")

cur.execute("INSERT INTO PAGOS (DIR_ID, PAGO, FECHA) VALUES (3, 600, '2023-02-10');")

cur.execute("INSERT INTO PAGOS (DIR_ID, PAGO, FECHA) VALUES (4, 320, '2022-12-10');")

cur.execute("INSERT INTO PAGOS (DIR_ID, PAGO, FECHA) VALUES (5, 320, '2023-02-10');")

cur.execute("INSERT INTO PAGOS (DIR_ID, PAGO, FECHA) VALUES (1, 320, '2023-01-10');")

cur.execute("INSERT INTO PAGOS (DIR_ID, PAGO, FECHA) VALUES (2, 320, '2022-10-10');")

cur.execute("INSERT INTO PAGOS (DIR_ID, PAGO, FECHA) VALUES (3, 300, '2023-01-10');")

cur.execute("INSERT INTO PAGOS (DIR_ID, PAGO, FECHA) VALUES (4, 320, '2022-11-10');")

cur.execute("INSERT INTO PAGOS (DIR_ID, PAGO, FECHA) VALUES (5, 320, '2023-01-10');")

conn.commit()
cur.close()
conn.close()