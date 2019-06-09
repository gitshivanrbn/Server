import asyncio
import websockets
import MySQLdb
import json
import signal
from threading import Thread
import time
from ServerLibrary import ServerLibrary

api = ServerLibrary()
centralbankaddress = 'ws://86.94.69.254:6666'
bankID = 'supavl'
async def run(websocket,path):
    try:
        incoming_message = await websocket.recv()
        try:
            print('received a message:',incoming_message)
            json_message = json.loads(incoming_message)

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
                else:
                    print('IBAN length is invalid!')
                    response =  {'response' : 'IBAN is invalid'}
                    await websocket.send(json.dumps(response))

            #de PIN checken.
            elif(json_message['Func'] == 'checkPIN'):
                API_response = json.loads(api.checkPIN(json_message))
                if(API_response['response'] == True):
                    print(API_response)
                    await websocket.send(json.dumps(API_response))
                else:
                    print('consumer function is being called')

            elif(json_message['Func'] == 'getbalance'):
                API_response = json.loads(api.getbalance(json_message))
                print(API_response)
                if(API_response['response'] != False):
                    await websocket.send(json.dumps(API_response))
                else:
                    print('consumer function is being called')

            elif(json_message['Func'] == 'withdraw'):
                API_response = json.loads(api.withdraw(json_message))
                if(API_response['response'] == True):
                    await websocket.send(json.dumps(API_response))
                else:
                    await websocket.send(json.dumps(False))


        #excepties van de json opvangen...
        except:
            print('error loading json, maybe its a wrong format?')
            response = {'response': 'false'}
            await websocket.send(json.dumps(response))
    except:
        print('something went wrong')


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
                    await asyncio.sleep(5)

    except ValueError:
        print('error connecting to central bank as master')

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
                    slave_json = json.loads(slave_message)
                    print(slave_json)
                    await ws_slave.send(json.dumps('False'))
        except:
            print('Error connecting to central bank as slave')

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



