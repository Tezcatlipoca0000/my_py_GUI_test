import sqlite3
import Constants
from datetime import date

def addr_search(addr):
    conn = sqlite3.connect(Constants.DB_ROUTE)
    cur = conn.cursor()

    cur.execute("SELECT * FROM DIRECCIONES WHERE CALLE = ?;", (addr,) )
    x = cur.fetchall()
    conn.commit()
    conn.close()
    return x

def pay_search(id):
    conn = sqlite3.connect(Constants.DB_ROUTE)
    cur = conn.cursor()

    cur.execute("SELECT * FROM PAGOS WHERE DIR_ID = ?;", (id,) )
    x = cur.fetchall()
    conn.commit()
    conn.close()
    return x

def has_agree(amount):
    if amount < Constants.Costo:
        return True
    else:
        return False
    

def last_pay(id):
    id_hist = pay_search(id)
    pay_hist = [t[-1] for t in id_hist]
    pay_hist.sort()
    day = pay_hist[-1]
    pay = [t[-2] for t in id_hist if day in t]
    return (pay[0], day)
    
def push_pay(id, amount, debt):
    pass

def charge_month():
    conn = sqlite3.connect(Constants.DB_ROUTE)
    cur = conn.cursor()

    cur.execute("UPDATE DIRECCIONES SET BALANCE = BALANCE - COSTO;")
    conn.commit()
    conn.close()
    print('Cargo del mes aplicado exitosamente a todos los registros.')
    
def chk_db():
    if date.today().day >= 10:
        if not Constants.DB_CHARGED:
            charge_month()

            with open('./Constants.py', 'r') as fh:
                lines = fh.readlines()

            with open('./Constants.py', 'w') as fh:
                for line in lines:
                    if 'DB_CH' in line:
                        line = line.replace('False', 'True')
                    fh.write(line)

    if date.today().day < 10:
        with open('./Constants.py', 'r') as fh:
            lines = fh.readlines()

        with open('./Constants.py', 'w') as fh:
            for line in lines:
                if 'DB_CH' in line:
                    line = line.replace('True', 'False')
                fh.write(line)

def deposit_pay(*args):
    (id, amount, balance) = args[0]

    conn = sqlite3.connect(Constants.DB_ROUTE)
    cur = conn.cursor()

    cur.execute( "INSERT INTO PAGOS(DIR_ID, PAGO, FECHA) VALUES(?, ?, ?);", (id, amount, str(date.today())) )
    cur.execute( "UPDATE DIRECCIONES SET BALANCE = ? WHERE DIR_ID = ?;", (balance.replace('$', ''), id) )

    cur.close()
    conn.commit()
    conn.close()

    if cur.rowcount > 0:
        return True
    else:
        return False
