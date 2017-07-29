from __future__ import print_function
from microsoft.gestures.endpoint.gestures_service_endpoint_factory import GesturesServiceEndpointFactory
from microsoft.gestures.fingertip_placement_relation import FingertipPlacementRelation
from microsoft.gestures.pass_through_gesture_segment import PassThroughGestureSegment
from microsoft.gestures.fingertip_distance_relation import FingertipDistanceRelation
from microsoft.gestures.vertical_motion_segment import VerticalMotionSegment
from microsoft.gestures.all_fingers_context import AllFingersContext
from microsoft.gestures.any_finger_context import AnyFingerContext
from microsoft.gestures.relative_placement import RelativePlacement
from microsoft.gestures.relative_distance import RelativeDistance
from microsoft.gestures.any_hand_context import AnyHandContext
from microsoft.gestures.finger_flexion import FingerFlexion
from microsoft.gestures.pose_direction import PoseDirection
from microsoft.gestures.finger_pose import FingerPose
from microsoft.gestures.hand_motion import HandMotion
from microsoft.gestures.palm_motion import PalmMotion
from microsoft.gestures.palm_pose import PalmPose
from microsoft.gestures.hand_pose import HandPose
from microsoft.gestures.gesture import Gesture
from microsoft.gestures.finger import Finger


def video_playback():
	# Step 1: Connect to Microsoft Gestures Detection service
	_gesturesService = GesturesServiceEndpointFactory.create()
	_gesturesService.on_status_changed(lambda args: print('{}'.format(args.status)))
	_gesturesService.connect()

	""" 
	Step 2: Define the RewindGesture gesture as follows:                                                                                      
	    Idle    ->   Spread   ->   Pause    ->   Rewind   -> KeepRewind ->  Release   ->    Idle    
	               (unpinch)      (pinch)        (left)       (pinch)      (unpinch)                

		When ever the gesture returns to Idle state it will always resume playback
	"""
	spreadPose = generate_pinch_pose("Spread", True)
	pausePose = generate_pinch_pose("Pause")
	pausePose.on_triggered(lambda: print('Pause'))

	rewindMotion = HandMotion("Back", PalmMotion(AnyHandContext(), VerticalMotionSegment.Left))
	rewindMotion.on_triggered(lambda: print('Rewind Motion'))

	keepRewindingPose = generate_pinch_pose("KeepRewind")
	releasePose = generate_pinch_pose("Release", True)
            
	# Then define the gesture by concatenating the previous objects to form a simple state machine
	_rewindGesture = Gesture("RewindGesture", spreadPose, pausePose, rewindMotion, keepRewindingPose, releasePose)
	# Detect if the user releases his pinch-grab and return to playback
	_rewindGesture.add_sub_path(pausePose, releasePose)
            
	# Continue playing the video when the gesture resets (either successful or aborted)
	_rewindGesture.on_triggered(lambda: print('Rewind Gesture'))
	_rewindGesture.on_idle_triggered(lambda: print('Idle'))

	# Step 3: Register the gesture (When window focus is lost/gained the service will effectively change the gesture registration automatically)
	#         To manually control the gesture registration, pass 'isGlobal: True' parameter in the function call below
	_gesturesService.register_gesture(_rewindGesture)
	print('Make a rewind gesture - pinch your thumb and index, then move them to the left')
	_gesturesService.poll()


def generate_pinch_pose(name, pinchSpread=False):
	pinchingFingers = [Finger.Thumb, Finger.Index]
	openFingersContext = AllFingersContext(pinchingFingers) if pinchSpread else AnyFingerContext(pinchingFingers)
	return HandPose(name,
					FingerPose(openFingersContext, FingerFlexion.Open),
					FingertipDistanceRelation(pinchingFingers, RelativeDistance.NotTouching if pinchSpread else RelativeDistance.Touching),
					FingertipDistanceRelation(pinchingFingers, RelativeDistance.NotTouching, Finger.Middle)
	)


if '__main__' == __name__:
	video_playback()
