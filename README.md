# sari-sari-sandbox

Sari-sari Sandbox 1.0

# Features
1.0
1. 250 retail store products
2. 3 retail store layouts
3. Shelf labels, price tags, and expiry dates
3. Self-checkout counter with barcode scanning capability
4. API to navigate and interact with the environment
5. Hand animations when gripping and poking

# To control agent through terminal:

1. Open the folder containing ClientSide.py in terminal
2. Open Python Shell and import ClientSide
3. Open bin/sss.exe
4. Run ClientSide functions in Python

e.g.

	python
	import ClientSide as a
	a.TransformAgent((0,0,0.02),(0,0,0))
	a.RequestScreenshot()

# ClientSide Documentation
This module provides functions to send various commands to a WebSocket server and handle the responses.

Functions:
	
	TransformAgent((translateX, translateY, translateZ), (degreesX, degreesY, degreesZ)):
		Transforms the agent by the specified translation and rotation with respect to the camera transform.
	
	TransformHands((leftTranslateX, leftTranslateY, leftTranslateZ), (leftDegreesX, leftDegreesY, leftDegreesZ), (rightTranslateX, rightTranslateY, rightTranslateZ), (rightDegreesX, rightDegreesY, rightDegreesZ)):
		Transforms the agent hands by the specified translation and rotation with respect to their corresponding transforms.
	
	ToggleLeftGrip():
		Toggles the grip of the left hand. Will successfully toggle from false to true if an XR Grab Interactable object collides with the left hand.
	
	ToggleRightGrip():
		Toggles the grip of the right hand. Will successfully toggle from false to true if an XR Grab Interactable object collides with the right hand.

	ToggleLeftPoke():
		Toggles the poke animation of the left hand.

	ToggleRightPoke():
		Toggles the poke animation of the right hand.
	
	RequestScreenshot():
		Requests a screenshot and saves the received image as "ClientScreenshot.png" in the same directory as this module.

	Reset():
		Resets the environment to its initial state with randomized grocery product placement.
