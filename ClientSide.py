import os
import asyncio
import websockets
import json
import re
from typing import (
    Tuple,
    Dict,
    Any
)

async def SendCommand(command: Dict[str, Any], uri: str):
    async with websockets.connect(uri, max_size=None) as websocket:
        await websocket.send(json.dumps(command))
        if command["command"] == "RequestScreenshot" or command["command"] == "RequestAnnotation":
            image_bytes = await websocket.recv()
            return {'image': image_bytes}
        else:
            response = await websocket.recv()
            return response

def TransformAgent(translation: Tuple[float],
                   rotation: Tuple[float],
                   uri: str = "ws://localhost:8080/commands") -> Dict[str, Tuple[float]]:
    result = asyncio.get_event_loop().run_until_complete(SendCommand({
        "command": "TransformAgent",
        "translation": translation,
        "rotation": rotation
    }, uri))

    extracted_state = re.findall(r'\((.*?)\)', result, re.DOTALL)
    assert len(extracted_state) == 2, "Expected 2 Tuple[float], got " + str(len(extracted_state))
    agent_state = {
        'translation': tuple(map(float, extracted_state[0].split(', '))),
        'rotation': tuple(map(float, extracted_state[1].split(', ')))
    }
    return agent_state

def TransformHands(leftTranslation: Tuple[float],
                   leftRotation: Tuple[float],
                   rightTranslation: Tuple[float],
                   rightRotation: Tuple[float],
                   uri: str = "ws://localhost:8080/commands"):
    result = asyncio.get_event_loop().run_until_complete(SendCommand({
        "command": "TransformHands",
        "leftTranslation": leftTranslation,
        "leftRotation": leftRotation,
        "rightTranslation": rightTranslation,
        "rightRotation": rightRotation
    }, uri))
    
    extracted_state = re.findall(r'\((.*?)\)', result, re.DOTALL)
    assert len(extracted_state) == 4, "Expected 4 Tuple[float], got " + str(len(extracted_state))
    current_state = {
        'leftTranslation': tuple(map(float, extracted_state[0].split(', '))),
        'leftRotation': tuple(map(float, extracted_state[1].split(', '))),
        'rightTranslation': tuple(map(float, extracted_state[2].split(', '))),
        'rightRotation': tuple(map(float, extracted_state[3].split(', ')))
    }
    return current_state

def ToggleLeftGrip(uri: str="ws://localhost:8080/commands"):
    result = asyncio.get_event_loop().run_until_complete(SendCommand({
        "command": "ToggleLeftGrip"
    }, uri))

    if "True" in result:    return True
    return False

def ToggleRightGrip(uri="ws://localhost:8080/commands"):
    result = asyncio.get_event_loop().run_until_complete(SendCommand({
        "command": "ToggleRightGrip"
    }, uri))

    if "True" in result:    return True
    return False

def RequestScreenshot(uri: str="ws://localhost:8080/commands"):
    result = asyncio.get_event_loop().run_until_complete(SendCommand({
        "command": "RequestScreenshot",
    }, uri))
    return result

def Reset(uri: str="ws://localhost:8080/commands"):
    asyncio.get_event_loop().run_until_complete(SendCommand({
        "command": "ResetEnvironment"
    }, uri))

def RequestAnnotation(uri: str="ws://localhost:8080/commands"):
    result = asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "RequestAnnotation"
    }, uri))
    return result

def RequestJson(uri: str="ws://localhost:8080/commands"):
    result = asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "RequestJson"
    }, uri))
    return result


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
_REQUEST_ANNOTATION_ = lambda: RequestAnnotation()
_REQUEST_JSON_ = lambda: RequestJson()