import asyncio
import websockets
import json

baseuri = "ws://localhost:8080/commands"

async def SendCommand(command, uri):
    async with websockets.connect(uri, max_size=None) as websocket:
        await websocket.send(json.dumps(command))
        if command["command"] == "RequestScreenshot" or command["command"] == "RequestAnnotation":
            imageBytes = await websocket.recv()
            with open(command["command"]+"ClientScreenshot.png", "wb") as file:
                file.write(imageBytes)
            print("Screenshot received and saved as ClientScreenshot.png")
        else:
            response = await websocket.recv()
            print(response)

async def FetchData(uri):
    async with websockets.connect(uri, max_size=None) as websocket:
        response = await websocket.recv()
        return response

def TransformAgent(translation, rotation, uri=baseuri):
    asyncio.get_event_loop().run_until_complete(SendCommand({
        "command": "TransformAgent",
        "translation": translation,
        "rotation": rotation
    }, uri))
    print("Client Side: Agent moved by", translation, rotation)

def TransformHands(leftTranslation, leftRotation, rightTranslation, rightRotation, uri=baseuri):
    asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "TransformHands",
        "leftTranslation": leftTranslation,
        "leftRotation": leftRotation,
        "rightTranslation": rightTranslation,
        "rightRotation": rightRotation
    }, uri))
    print("Client Side: Hands transformed")

def ToggleLeftGrip(uri=baseuri):
    asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "ToggleLeftGrip"
    }, uri))
    print("Client Side: Toggle Left Grip")

def ToggleRightGrip(uri=baseuri):
    asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "ToggleRightGrip"
    }, uri))
    print("Client Side: Toggle Right Grip")

def ToggleLeftPoke(uri=baseuri):
    asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "ToggleLeftPoke"
    }, uri))
    print("Client Side: Toggle Left Poke")

def ToggleRightPoke(uri=baseuri):
    asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "ToggleRightPoke"
    }, uri))
    print("Client Side: Toggle Right Poke")

def RequestScreenshot(uri=baseuri):
    asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "RequestScreenshot"
    }, uri))
    print("Client Side: Screenshot requested.")

def Reset(uri=baseuri):
    asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "ResetEnvironment"
    }, uri))
    print("Client Side: Screenshot requested.")

# def RequestAnnotation(uri="ws://localhost:8080/commands"):
#     asyncio.get_event_loop().run_until_complete(SendCommand(
#         {
#         "command": "RequestAnnotation"
#     }, uri))
#     print("Client Side: Annotation requested.")

# def RequestJson(uri=baseuri):
#     asyncio.get_event_loop().run_until_complete(SendCommand(
#         {
#         "command": "RequestJson"
#     }, uri))
#     print("Client Side: Json requested.")

# def RequestData():
#     RequestScreenshot()
#     RequestAnnotation()
#     RequestJson()


## controls
_MOVE_FWD_ = lambda: TransformAgent((0, 0, 0.1), (0, 0, 0))
_MOVE_BCK_ = lambda: TransformAgent((0, 0, -0.1), (0, 0, 0))
_MOVE_LEFT_ = lambda: TransformAgent((-0.1, 0, 0), (0, 0, 0))
_MOVE_RIGHT_ = lambda: TransformAgent((0.1, 0, 0), (0, 0, 0))
_PAN_LEFT_ = lambda: TransformAgent((0, 0, 0), (0, -2.5, 0))
_PAN_RIGHT_ = lambda: TransformAgent((0, 0, 0), (0, 2.5, 0))
_PAN_UP_ = lambda: TransformAgent((0, 0, 0), (-2.5, 0, 0))
_PAN_DOWN_ = lambda: TransformAgent((0, 0, 0), (2.5, 0, 0))
_GRIP_LEFT_ = lambda: ToggleLeftGrip()
_GRIP_RIGHT_ = lambda: ToggleRightGrip()
_XTNFWD_LEFT_ = lambda: TransformHands((0, 0, 0.025), (0, 0, 0), (0, 0, 0), (0, 0, 0))
_PLLBCK_LEFT_ = lambda: TransformHands((0, 0, -0.025), (0, 0, 0), (0, 0, 0), (0, 0, 0))
_XTNFWD_RIGHT_ = lambda: TransformHands((0, 0, 0), (0, 0, 0), (0, 0, 0.025), (0, 0, 0))
_PLLBCK_RIGHT_ = lambda: TransformHands((0, 0, 0), (0, 0, 0), (0, 0, -0.025), (0, 0, 0))
_RSE_LEFT_ = lambda: TransformHands((0, 0.025, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0))
_LWR_LEFT_ = lambda: TransformHands((0, -0.025, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0))
_RSE_RIGHT_ = lambda: TransformHands((0, 0, 0), (0, 0, 0), (0, 0.025, 0), (0, 0, 0))
_LWR_RIGHT_ = lambda: TransformHands((0, 0, 0), (0, 0, 0), (0, -0.025, 0), (0, 0, 0))
_RESET_ = lambda: Reset()
_REQUEST_SCREENSHOT_ = lambda: RequestScreenshot()
# _REQUEST_ANNOTATION_ = lambda: RequestAnnotation()
# _REQUEST_JSON_ = lambda: RequestJson()