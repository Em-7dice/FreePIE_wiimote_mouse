import thread, time

"""WestleyTwain's Mouse Scrpit 					v:1.3.0
Requires WiiMotionPlus. All buttons can be remapped and most (if not all) fine tuning can be done in the first 2 sections.
Features: 
	Hold B to move the cursor, Left click = A, Right click = +, Mid click = Home
	Hold - and point up and down to scroll
	Hold 1 and twist like a volume knob to change the volume
This scrpit is in part an amalgamation of others' scripts and bits of code I added to or changed.
Any and all thank-yous are listed blow. Special thanks to MeteorFalling 2 for the stable cursor!
"""

#~~~Button Customization~~~#

global MoveButton
MoveButton   = WiimoteButtons.B
global ScrollButton
ScrollButton = WiimoteButtons.Minus
global VolumeButton
VolumeButton = WiimoteButtons.One
global MouseLeft
MouseLeft    = WiimoteButtons.A
global MouseMiddle
MouseMiddle  = WiimoteButtons.Home
global MouseRight
MouseRight   = WiimoteButtons.Plus

#~~~Speeds and Fine Tuning~~~#

global CursorSpeed
CursorSpeed   = 16		# Default is 16
global ScrollSpeed
ScrollSpeed   = 16		# Default is 16
global VolumeDegrees
VolumeDegrees = 3 		# Every x degrees, the volume button is pressed. Higher = quicker, Lower = Finer Tuning. Default is 3

#~~~MotionPlus Update~~~#

def motionplus_update():
	yawSpeed = (wiimote[0].motionplus.yaw_down) 
	pitchSpeed = (wiimote[0].motionplus.pitch_left)
	roll_Pos = filters.deadband((wiimote[0].ahrs.roll), 0.15)
   
	#~~~Cursor: thank you MeteorFalling2 for the basis of this section~~~#	
	if wiimote[0].buttons.button_down(MoveButton): 
		mouse.deltaX = yawSpeed/-CursorSpeed ## add a negative to the CursorSpeed if using non-TR version.
		mouse.deltaY = pitchSpeed/CursorSpeed ## remove the negative if using non-TR version.
		
	#~~~Pointer Scrolling: thank you MeteorFalling2 for the basis of this section~~~#	
	if wiimote[0].buttons.button_down(ScrollButton):
		mouse.wheel = pitchSpeed/ScrollSpeed
	
	#~~~Volume Knob: thank you AndersMalmgren for showing an example of the stopWatch function~~~#	
	VButton = wiimote[0].buttons.button_down(VolBut)
	global pastCutoff
	global rollInit
	global rollCurr
	
	if filters.stopWatch(wiimote[0].buttons.button_down(VolBut), 50):
		pastCutoff = True
	if not VButton:
		pastCutoff = False
		rollInit = 0
		rollCurr = 0
	
	if VButton != pastCutoff:
		rollInit = roll_Pos
	
	if pastCutoff:
		rollCurr = roll_Pos
		if   rollCurr >=  volDeg + rollInit:
			keyboard.setKeyDown(Key.VolumeDown)
			rollInit = rollCurr
		elif rollCurr <= -volDeg + rollInit:
			keyboard.setKeyDown(Key.VolumeUp)
			rollInit = rollCurr
		else:
			keyboard.setKeyUp(Key.VolumeUp)
			keyboard.setKeyUp(Key.VolumeDown)

#~~~Mouse Buttons: Thanks again, MeteorFalling2. The last two lines were my first lines of Python.~~~#

def update_mouse_butts():
	mouse.leftButton = wiimote[0].buttons.button_down(MouseLeft)
	mouse.rightButton = wiimote[0].buttons.button_down(MouseRight)
	mouse.middleButton = wiimote[0].buttons.button_down(MouseMiddle)

#~~~If Starting~~~#

if starting:
	system.setThreadTiming(TimingTypes.HighresSystemTimer)
	system.threadExecutionInterval = 2
	wiimote[0].motionplus.update += motionplus_update
	wiimote[0].buttons.update += update_mouse_butts
	wiimote[0].enable(WiimoteCapabilities.MotionPlus)
