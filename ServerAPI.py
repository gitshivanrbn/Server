import asyncio
import websockets
import MySQLdb
import json
import signal
from threading import Thread
import time
from ServerLibrary import ServerLibrary

api = ServerLibrary()
centralbankaddress = 'ws://145.137.90.185:6666'
bankID = 'SUPAVL'
storedcommands = []
receivedanswers = []

async def run(websocket,path):
    try:
        incoming_message = await websocket.recv()
        try:
            print('received a message:',incoming_message)
            print(len(incoming_message))
            json_message = json.loads(incoming_message)
            json_message['Amount'] = int(json_message['Amount'])
            print(json_message['Amount'])
            json_message['IDRecBank'] = json_message['IBAN'][0:2] +json_message['IBAN'][4:8]
            print(json_message['IBAN'])
            json_message['IDSenBank'] = bankID

            #de kaart checken
            if (json_message['Func'] == 'checkcard'):
                if (len(json_message['IBAN']) == 14):
                    print(json_message['IBAN'])
                    API_response = json.loads(api.checkcard(json_message))
                    if(API_response['response'] == True):
                        print(API_response)
                        await websocket.send(json.dumps(API_response))
                    else:
                        print('Consumer function is being called')
                        storecommand(json.dumps(json_message))
                        await asyncio.sleep(0.06)
                        if(len(receivedanswers) != 0):
                            answer = getreceivedanswer()
                            print(answer)
                            await websocket.send(json.dumps({'response': answer}))
                else:
                    print('IBAN length is invalid!')
                    response =  {'response' : 'IBAN is invalid'}
                    await websocket.send(json.dumps(response))

            #de PIN checken.
            elif(json_message['Func'] == 'pinCheck'):
                API_response = json.loads(api.checkPIN(json_message))
                if(API_response['response'] == True):
                    print(API_response)
                    await websocket.send(json.dumps(API_response))
                else:
                    print('consumer function is being called')
                    storecommand(json.dumps(json_message))
                    await asyncio.sleep(0.06)
                    if(len(receivedanswers) != 0):
                        answer = getreceivedanswer()
                        print(answer)
                        await websocket.send(json.dumps({'response': answer}))

            #GET BELANCE!!!!!!!!!!!!!                
            elif(json_message['Func'] == 'getbalance'):
                API_response = json.loads(api.getbalance(json_message))
                print(API_response)
                if(API_response['response'] != False):
                    await websocket.send(json.dumps(API_response))
                else:
                    print('consumer function is being called')
                    storecommand(json.dumps(json_message))
                    await asyncio.sleep(0.06)
                    if(len(receivedanswers) != 0):
                        answer = getreceivedanswer()
                        print(answer)
                        await websocket.send(json.dumps({'response': answer}))


            #WITHDRAW!!!!!!!!!!!!!
            elif(json_message['Func'] == 'withdraw'):
                API_response = json.loads(api.withdraw(json_message))
                print('test')
                if(API_response['response'] == True):
                    await websocket.send(json.dumps(API_response))
                else:
                    print('consumer function is being called')
                    storecommand(json.dumps(json_message))
                    await asyncio.sleep(0.05)
                    if(len(receivedanswers) != 0):
                        answer = getreceivedanswer()
                        print(answer)
                        await websocket.send(json.dumps({'response': answer}))
            
            else:
                print('command not found')
                response = {'response' : False}
                await websocket.send(json.dumps(response))

        #excepties van de json opvangen...
        except:
            print('error loading json, maybe its a wrong format?')
            response = {'response': 'false'}
            await websocket.send(json.dumps(response))
    except:
        print('something went wrong')


#AF!
#de master-thread die registreert en in een while True loop staat
async def register_master():
    try:
        async with websockets.connect(centralbankaddress) as ws_master:
            print('sending master request...')
            master = ['register','master',bankID]
            await ws_master.send(json.dumps(master))
            masterresponse = await ws_master.recv()
            if (masterresponse == 'true'):
                print('confirmed master registration')     
                while(True):
                    await asyncio.sleep(0.01)
                    if(len(storedcommands) != 0):
                        command = getcommand()
                        print('command')
                        print(command)
                        print(len(str(command)))
                        await ws_master.send(command)
                        master_answer = await ws_master.recv()
                        print('master received an answer')
                        storereceivedanswer(master_answer)

                        

    except ValueError:
        print('error connecting to central bank as master')


#AF!
#de slave-thread die in een while true loop staat
async def register_slave():
    try:
        async with websockets.connect(centralbankaddress) as ws_slave:
            print('sending slave request....')
            slave = ['register','slave',bankID]
            await ws_slave.send(json.dumps(slave))
            slaveresponse = await ws_slave.recv()
            if (slaveresponse == 'true'):
                print('confirmed slave registration')
                while(True):
                    slave_message = await ws_slave.recv()
                    print('received a slave message')
                    print('slave_message is:', slave_message)
                    slave_json = slave_message[2:len(slave_message) - 2]
                    slave_json = slave_json.replace("'",'"')
                    slave_json = json.loads(slave_json)
                    slave_json['IDRecBank'] = slave_json['IDRecBank'].lower()
                    if(slave_json['IDRecBank'] == 'supavl' || slave_json['IDRecBank'] == 'pavl'):
                        print('receiving slave message.')
                        if(slave_json['Func'] == 'checkcard'):
                            print('checking card remotely')
                            response = json.loads(api.checkcard(slave_json))
                            await ws_slave.send(json.dumps(response['response']))
                        elif(slave_json['Func'] == 'pinCheck'):
                            print('checking pin remotely...')
                            response = json.loads(api.checkPIN(slave_json))
                            await ws_slave.send(json.dumps(response['response']))

                        elif(slave_json['Func'] == 'withdraw'):
                            print('withdrawing remotely')
                            response = json.loads(api.withdraw(slave_json))
                            print(response)
                            await ws_slave.send(json.dumps(response['response']))
                    else:
                        print('bank code not identified')
                        await ws_slave.send(json.dumps('False'))
            else:
                        response = False
                        await ws_slave.send(json.dumps(response))

    except:
        print('error in slave_connection')



#producer functie tussen de server-master connectie

#functie om de berichten op te slaan
def storecommand(json_message):
    storedcommands.append(json_message)

def storereceivedanswer(receivedanswer):
    receivedanswers.append(receivedanswer)


#functie om berichten op te halen
def getcommand():
    command = json.loads(storedcommands.pop())
    buildedstring = '["'
    buildedstring += (command['IDRecBank'])
    buildedstring += '" , '
    buildedstring += '"'
    buildedstring += str(command)

    buildedstring += '"]'
    return buildedstring

def getreceivedanswer():
    receivedanswer = receivedanswers.pop()
    return receivedanswer

#start de server
print('Starting server')
start_server = websockets.serve(run,'145.24.222.179',8888)
#voert de taken uit.
print('client running...')
print('Setting up on-screen log')
print('On-screen log OK-to-go')
asyncio.get_event_loop().run_until_complete(start_server)
#master-slave registration
asyncio.run_coroutine_threadsafe(register_slave(),asyncio.get_event_loop())
asyncio.get_event_loop().run_until_complete(register_master())

#eindigt nooit met runnen
print('running forever....')
asyncio.get_event_loop().run_forever()



