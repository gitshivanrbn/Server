import websockets
import asyncio

class Communicatewithbank:

    def __init__(self):
        self = self

    #client side communicatie naar de bank toe.
    async def communicatewithbank():
        async with websockets.connect('ws://192.168.2.157:7777') as websocket:
            responseID = {'response': 'ayylmao'}
            ID = json.dumps(responseID)
            await websocket.send(ID)
            print(f">{ID}")
            clientresponse = await websocket.recv()
            print(clientresponse)

    asyncio.get_event_loop().run_until_complete(communicatewithbank())

