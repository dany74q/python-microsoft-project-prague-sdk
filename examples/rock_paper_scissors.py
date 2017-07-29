from __future__ import print_function
from microsoft.gestures.endpoint.gestures_service_endpoint_factory import GesturesServiceEndpointFactory
from microsoft.gestures.fingertip_placement_relation import FingertipPlacementRelation
from microsoft.gestures.pass_through_gesture_segment import PassThroughGestureSegment
from microsoft.gestures.fingertip_distance_relation import FingertipDistanceRelation
from microsoft.gestures.all_fingers_context import AllFingersContext
from microsoft.gestures.relative_placement import RelativePlacement
from microsoft.gestures.relative_distance import RelativeDistance
from microsoft.gestures.any_hand_context import AnyHandContext
from microsoft.gestures.finger_flexion import FingerFlexion
from microsoft.gestures.pose_direction import PoseDirection
from microsoft.gestures.finger_pose import FingerPose
from microsoft.gestures.palm_pose import PalmPose
from microsoft.gestures.hand_pose import HandPose
from microsoft.gestures.gesture import Gesture
from microsoft.gestures.finger import Finger


def rock_paper_scissors():
	# Step1: Define the Rock-Paper-Scissors gestures
	# Create a pose for 'Rock'...
	rockPose = HandPose(
		"RockPose",
		FingerPose(AllFingersContext(), FingerFlexion.Folded)
	)
	rockPose.on_triggered(lambda: print('You Played Rock!'))

	# ...another for 'Paper'...
	paperPose = HandPose(
		"PaperPose",
		PalmPose(
			AnyHandContext(),
			PoseDirection.Left | PoseDirection.Right,
			PoseDirection.Forward
		),
		FingerPose(AllFingersContext(), FingerFlexion.Open)
	)
	paperPose.on_triggered(lambda: print('You Played Paper!'))

	# ...and last one for 'Scissors'...
	scissorsPose = HandPose(
		"ScissorsPose", 
		FingerPose([Finger.Index, Finger.Middle], FingerFlexion.Open),
		FingertipDistanceRelation(Finger.Index, RelativeDistance.NotTouching, Finger.Middle),
		FingerPose([Finger.Ring, Finger.Pinky], FingerFlexion.Folded)
	)
	scissorsPose.on_triggered(lambda: print('You Played Scissors!'))

	# ...a PassThroughtGestureSegment is a structural gesture segment that provides a way to simplify a gesture state machine construction by 'short-circuiting' 
	# between gesture segments connectd to it and gesture segements it connects to. It helps reduce the number of SubPaths that needs to be defined.
	# Very handy when you need to define a Clique (see https:#en.wikipedia.org/wiki/Clique_(graph_theory)#1)
	# as in this case where Rock, Paper and Scissors are all connected to each other...
	epsilonState = PassThroughGestureSegment("Epsilon")
	
	# ...this pose is an artificial stop pose. Namely, we want to keep the gesture detector in one of the pose states without ending the gesture so we add this
	# pose as a pose that completes the gesture assuming the user will not perform it frequently. 
	# As long as the user continues to perform the 'Rock', 'Paper' or 'Scissors' poses we will remain within the gesture's state machine.
	giveUpPose = HandPose(
		"GiveUpPose", 
		PalmPose(AnyHandContext(), PoseDirection.Forward, PoseDirection.Up),
		FingerPose(AllFingersContext(), FingerFlexion.Open)
	)

	_gameGesture = Gesture("RockPaperScissorGesturz", epsilonState, giveUpPose)
	# ...add a sub path back and forth from the PassthroughGestureSegment to the various poses
	_gameGesture.add_sub_path(epsilonState, rockPose, epsilonState)
	_gameGesture.add_sub_path(epsilonState, paperPose, epsilonState)
	_gameGesture.add_sub_path(epsilonState, scissorsPose, epsilonState)

	# In case the user performs a pose that is not one of the game poses the gesture resets and this event will trigger
	_gameGesture.on_idle_triggered(lambda: print('Idle'))

	# Step2: Connect to Gesture Detection Service, route StatusChanged event to the UI and register the gesture
	_gesturesService = GesturesServiceEndpointFactory.create()
	_gesturesService.on_status_changed(lambda _: print('{}'.format(_.status)))
	_gesturesService.connect()
	_gesturesService.register_gesture(_gameGesture)
	print('Make any gesture: Rock, Paper, or Scissors')
	_gesturesService.poll()

if '__main__' == __name__:
	rock_paper_scissors()
