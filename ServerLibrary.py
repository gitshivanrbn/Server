import json
import asyncio 
import MySQLdb

class ServerLibrary:

    def __init__(self):
        print(self)

    @staticmethod
    def fetchNUID(jsonmessage):
            cnxID = MySQLdb.connect(user='bank',password='wX9438',host='localhost',database='bank')
            cursorID = cnxID.cursor()
            receivedID = jsonmessage['IBAN']
            rowcountID = cursorID.execute("SELECT Pasje_ID FROM Pasjes WHERE Pasje_ID =%s",(receivedID,))
            cnxID.close()
            if (rowcountID > 0):
                rowID = cursorID.fetchone()
                print(rowID)
                responseID = {'response': rowID[0]}
                ID = json.dumps(responseID)
                print(ID)
                print('returned message succesfully')
                return ID

            else:
                print('Error, data could not be found')
                responseID = {'response': 'false'}
                errorID = json.dumps(responseID)
                print(errorID)
                print('returned error message to client')
                return errorID

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
            rowpin = cursorpin.fetchone()
            print('fetched pin:')
            print(rowpin)
            responsepin = {'response': str(rowpin[0])}
            pin = json.dumps(responsepin)
            return pin
        else:
            print('Error, data could not be found')
            responsepin = {'response': 'false'}
            errorpin = json.dumps(responsepin)
            return errorpin

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
            responsebalance = {'response': 'false'}
            errorbalance = json.dumps(responsebalance)
            return errorbalance

    @staticmethod
    def withdraw(jsonmessage):
        cnxwithdraw = MySQLdb.connect(user='bank',password='wX9438',host='localhost',database='bank')
        cursorwithdraw = cnxwithdraw.cursor()
        withdraw = jsonmessage['Amount']
        withdrawpin = jsonmessage['PIN']
        withdrawID = jsonmessage['IBAN']
        cursorwithdraw.execute("UPDATE Pasjes SET Saldo = Saldo - %s WHERE PIN = %s AND Pasje_ID = %s",(withdraw,withdrawpin,withdrawID,))
        cnxwithdraw.commit()
        print('withdrew',withdraw)
        rowcount = cursorwithdraw.execute("SELECT Saldo FROM Pasjes WHERE PIN = %s AND Pasje_ID = %s",(withdrawpin,withdrawID))
        cnxwithdraw.close
        if (rowcount > 0):
            rowwithdraw = cursorwithdraw.fetchone()
            print(rowwithdraw)
            responsewithdraw = {'response': rowwithdraw[0]}
            withdrawjson = json.dumps(responsewithdraw)
            return withdrawjson
        else:
            print('Error, data could not be found')
            responsewithdraw = {'response': 'false'}
            errorwithdraw = json.dumps(responsewithdraw)
            return errorwithdraw
