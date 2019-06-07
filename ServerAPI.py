import asyncio
import websockets
import MySQLdb
import json
import signal
import _thread
import time
from ServerLibrary import ServerLibrary

api = ServerLibrary()
centralbankaddress = 'ws://145.137.90.185:6666'
bankID = 'SUPAVL'
async def run(websocket,path):
    try:
        incoming_message = await websocket.recv()
        print('hi hi hi')
        try:
            print('received a message:',incoming_message)
            json_message = json.loads(incoming_message)

            if (json_message['Func'] == 'checkcard'):
                if (len(json_message['IBAN']) == 14):
                    API_response = api.checkcard(json_message)
                    if(API_response == True):
                        print(API_response)
                        await websocket.send('True')
                    else:
                        print('Consumer function is being called')
                else:
                    print('IBAN length is invalid!')
                    response =  {'response' : 'IBAN is invalid'}
                    await websocket.send(json.dumps(response))


        #excepties van de json opvangen...
        except:
            print('error loading json, maybe its a wrong format?')
            response = {'response': 'false'}
            await websocket.send(json.dumps(response))
    except:
        print('something went wrong')

async def register():
    try:
        async with websockets.connect(centralbankaddress) as ws_master:
            print('sending master request...')
            master = ['register','master',bankID]
            await ws_master.send(json.dumps(master))
            masterresponse = await ws_master.recv()
            if (masterresponse == 'true'):
                print('confirmed master registration')
                async with websockets.connect(centralbankaddress) as ws_slave:
                    print('sending slave request....')
                    slave = ['register','slave',bankID]
                    await ws_slave.send(json.dumps(slave))
                    slaveresponse = await ws_slave.recv()
                    if (slaveresponse == 'true'):
                        print('confirmed slave registration')
                        depo = ['ussr','deposit',6666,9999,20]
                        while(True):
                            await ws_master.send(json.dumps(depo))


    except ValueError:
        print('error connecting to central bank')
            


#start de server
print('Starting server')
start_server = websockets.serve(run,'145.24.222.179',8888)
#voert de taken uit.
print('client running...')
print('Setting up on-screen log')
print('On-screen log OK-to-go')
asyncio.get_event_loop().run_until_complete(start_server)
#master-slave registration
asyncio.get_event_loop().run_until_complete(register())

#eindigt nooit met runnen
print('running forever....')
asyncio.get_event_loop().run_forever()



