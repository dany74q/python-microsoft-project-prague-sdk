from __future__ import print_function
from microsoft.gestures.endpoint.gestures_service_endpoint_factory import GesturesServiceEndpointFactory
from microsoft.gestures.fingertip_placement_relation import FingertipPlacementRelation
from microsoft.gestures.fingertip_distance_relation import FingertipDistanceRelation
from microsoft.gestures.relative_placement import RelativePlacement
from microsoft.gestures.relative_distance import RelativeDistance
from microsoft.gestures.finger_flexion import FingerFlexion
from microsoft.gestures.pose_direction import PoseDirection
from microsoft.gestures.finger_pose import FingerPose
from microsoft.gestures.hand_pose import HandPose
from microsoft.gestures.gesture import Gesture
from microsoft.gestures.finger import Finger

def rotate_right():
    # Step 1: Connect to Microsoft Gestures Detection service
    gesturesService = GesturesServiceEndpointFactory.create()
    gesturesService.on_status_changed(lambda _: print('{}'.format(_.status)))
    gesturesService.connect()

    # Step 2: Define your custom gesture 
    # Start with defining the first pose, ...
    hold = HandPose(
        "Hold",
        FingerPose([Finger.Thumb, Finger.Index], FingerFlexion.Open, PoseDirection.Forward),
        FingertipDistanceRelation(Finger.Index, RelativeDistance.NotTouching, Finger.Thumb),
        FingertipPlacementRelation(Finger.Index, RelativePlacement.Above, Finger.Thumb)
    )

    # ... define the second pose, ...
    rotate = HandPose(
        "Rotate", 
        FingerPose([Finger.Thumb, Finger.Index], FingerFlexion.Open, PoseDirection.Forward),
        FingertipDistanceRelation(Finger.Index, RelativeDistance.NotTouching, Finger.Thumb),
        FingertipPlacementRelation(Finger.Index, RelativePlacement.Left, Finger.Thumb)
    )

    # ... finally define the gesture using the hand pose objects defined above forming a simple state machine: hold -> rotate
    rotateGesture = Gesture("RotateLeft", hold, rotate)
    rotateGesture.on_triggered(on_trigger)

    # Step 3: Register the gesture (When window focus is lost/gained the service will effectively change the gesture registration automatically)
    #         To manually control the gesture registration, pass 'isGlobal: true' parameter in the function call below
    gesturesService.register_gesture(rotateGesture)
    print('Try rotating your thumb and index finger to the left')
    gesturesService.poll()


def on_trigger():
    print('Rotate Left!')

if '__main__' == __name__:
    rotate_right()