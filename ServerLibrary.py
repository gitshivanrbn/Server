import json
import asyncio 
import MySQLdb

class ServerLibrary:

    def __init__(self):
        print(self)

    @staticmethod
    def checkcard(jsonmessage):
            cnxID = MySQLdb.connect(user='bank',password='wX9438',host='localhost',database='bank')
            cursorID = cnxID.cursor()
            receivedID = jsonmessage['IBAN']
            rowcountID = cursorID.execute("SELECT Pasje_ID FROM Pasjes WHERE Pasje_ID =%s",(receivedID,))
            cnxID.close()
            if (rowcountID > 0):
                return True

            else:
                return False

    @staticmethod
    def checkPIN(jsonmessage):
        #CHECKEN VOOR DE PIN
        cnxpin = MySQLdb.connect(user='bank',password='wX9438',host='localhost',database='bank')
        cursorpin = cnxpin.cursor()
        receivedpin = jsonmessage['PIN']
        receivedID = jsonmessage['IBAN']
        rowcount = cursorpin.execute("SELECT PIN FROM Pasjes  WHERE PIN = %s AND Pasje_ID = %s",(receivedpin,receivedID,))
        cnxpin.close
        if (rowcount > 0):
            return True
        else:
            return False

    @staticmethod
    def getbalance(jsonmessage):
        #Get balance
        cnxbalance = MySQLdb.connect(user='bank',password='wX9438',host='localhost',database='bank')
        cursorbalance = cnxbalance.cursor()
        balancepin = jsonmessage['PIN']
        balanceID = jsonmessage['IBAN']
        rowcount = cursorbalance.execute("SELECT Saldo FROM Pasjes WHERE PIN = %s AND Pasje_ID = %s",(balancepin,balanceID))
        cnxbalance.close
        if (rowcount > 0):
            rowbalance = cursorbalance.fetchone()
            print(rowbalance)
            responsebalance = {'response': rowbalance[0]}
            jsonbalance = json.dumps(responsebalance)
            return jsonbalance
        else:
            print('Error, data could not be found')
            return False

    @staticmethod
    def withdraw(jsonmessage):
        try:
            cnxwithdraw = MySQLdb.connect(user='bank',password='wX9438',host='localhost',database='bank')
            cursorwithdraw = cnxwithdraw.cursor()
            withdraw = jsonmessage['Amount']
            withdrawpin = jsonmessage['PIN']
            withdrawID = jsonmessage['IBAN']
            cursorwithdraw.execute("UPDATE Pasjes SET Saldo = Saldo - %s WHERE PIN = %s AND Pasje_ID = %s",(withdraw,withdrawpin,withdrawID,))
            cnxwithdraw.commit()
            print('withdrew',withdraw)
            cnxwithdraw.close
            return True
        except:
            print('error or couldnt find selected statement')
            return False
