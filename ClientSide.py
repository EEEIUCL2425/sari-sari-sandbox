import asyncio
import websockets
import json

async def SendCommand(command, uri):
    async with websockets.connect(uri, max_size=None) as websocket:
        await websocket.send(json.dumps(command))
        if command["command"] == "RequestScreenshot":
            imageBytes = await websocket.recv()
            with open("ClientScreenshot.png", "wb") as file:
                file.write(imageBytes)
            print("Screenshot received and saved as ClientScreenshot.png")
        else:
            response = await websocket.recv()
            print(response)

async def FetchData(uri):
    async with websockets.connect(uri, max_size=None) as websocket:
        response = await websocket.recv()
        return response

def TransformAgent(translation, rotation, uri="ws://localhost:8080/commands"):
    asyncio.get_event_loop().run_until_complete(SendCommand({
        "command": "TransformAgent",
        "translation": translation,
        "rotation": rotation
    }, uri))
    print("Client Side: Agent moved by", translation, rotation)

def TransformHands(leftTranslation, leftRotation, rightTranslation, rightRotation, uri="ws://localhost:8080/commands"):
    asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "TransformHands",
        "leftTranslation": leftTranslation,
        "leftRotation": leftRotation,
        "rightTranslation": rightTranslation,
        "rightRotation": rightRotation
    }, uri))
    print("Client Side: Hands transformed")

def ToggleLeftGrip(uri="ws://localhost:8080/commands"):
    asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "ToggleLeftGrip"
    }, uri))
    print("Client Side: Toggle Left Grip")

def ToggleRightGrip(uri="ws://localhost:8080/commands"):
    asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "ToggleRightGrip"
    }, uri))
    print("Client Side: Toggle Right Grip")

def RequestScreenshot(uri="ws://localhost:8080/commands"):
    asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "RequestScreenshot"
    }, uri))
    print("Client Side: Screenshot requested.")