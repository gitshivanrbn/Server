import json
import asyncio 
import MySQLdb

class ServerLibrary:

    def __init__(self):
        print(self)

    @staticmethod
    def checkcard(jsonmessage):
            cnxID = MySQLdb.connect(user='nope',password='nope',host='localhost',database='nope')
            cursorID = cnxID.cursor()
            receivedID = jsonmessage['IBAN']
            rowcountID = cursorID.execute("SELECT Pasje_ID FROM Pasjes WHERE Pasje_ID =%s",(receivedID,))
            cnxID.close()
            if (rowcountID > 0):
                response = {'response' : True}
                return json.dumps(response)

            else:
                print('couldnt find card')
                response = {'response': False}
                return json.dumps(response)

    @staticmethod
    def checkPIN(jsonmessage):
        #CHECKEN VOOR DE PIN
        cnxpin = MySQLdb.connect(user='nope',password='nope',host='localhost',database='nope')
        cursorpin = cnxpin.cursor()
        receivedpin = jsonmessage['PIN']
        receivedID = jsonmessage['IBAN']
        rowcount = cursorpin.execute("SELECT PIN FROM Pasjes  WHERE PIN = %s AND Pasje_ID = %s",(receivedpin,receivedID,))
        cnxpin.close
        if (rowcount > 0):
            response = {'response' : True}
            return json.dumps(response)
        else:
            print('couldnt find PIN')
            response = {'response' : False}
            return json.dumps(response)

    @staticmethod
    def getbalance(jsonmessage):
        #Get balance
        cnxbalance = MySQLdb.connect(user='nope',password='nope',host='localhost',database='nope')
        cursorbalance = cnxbalance.cursor()
        balancepin = jsonmessage['PIN']
        balanceID = jsonmessage['IBAN']
        rowcount = cursorbalance.execute("SELECT Saldo FROM Pasjes WHERE PIN = %s AND Pasje_ID = %s",(balancepin,balanceID))
        cnxbalance.close
        if (rowcount > 0):
            rowbalance = cursorbalance.fetchone()
            print(rowbalance)
            responsebalance = {'response': rowbalance[0]}
            return json.dumps(responsebalance)
        else:
            print('Error, data could not be found')
            response = {'response' : False}
            return json.dumps(response)

    @staticmethod
    def withdraw(jsonmessage):
        try:
            cnxwithdraw = MySQLdb.connect(user='nope',password='nope',host='localhost',database='nope')
            cursorwithdraw = cnxwithdraw.cursor()
            withdraw = jsonmessage['Amount']
            withdrawpin = jsonmessage['PIN']
            withdrawID = jsonmessage['IBAN']
            rowcountwithdraw= cursorwithdraw.execute("SELECT Saldo FROM Pasjes WHERE PIN = %s AND Pasje_ID = %s",(withdrawpin,withdrawID,))
            if (rowcountwithdraw > 0):
                selected_amount = cursorwithdraw.fetchone()[0]
                if (int(selected_amount) > int(withdraw)):
                    cursorwithdraw.execute("UPDATE Pasjes SET Saldo = Saldo - %s WHERE PIN = %s AND Pasje_ID = %s",(withdraw,withdrawpin,withdrawID,))
                    cnxwithdraw.commit()
                    print('withdrew',withdraw)
                    cnxwithdraw.close
                    response = {'response': True}
                    return json.dumps(response)
            else:
                cnxwithdraw.close
                response = {'response': False}
                return json.dumps(response)
        except:
            print('error or couldnt find selected statement or amount is too low')
            response = { 'response' : False}
            return response
