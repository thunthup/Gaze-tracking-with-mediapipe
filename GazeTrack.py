import cv2
import mediapipe as mp

from util import calDist, getXRatio, getYRatio

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh







drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)
with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)

    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
        face_landmarks = face_landmarks
#         mp_drawing.draw_landmarks(
#             image=image,
#             landmark_list=face_landmarks,
#             connections=mp_face_mesh.FACEMESH_TESSELATION,
#             landmark_drawing_spec=None,
#             connection_drawing_spec=mp_drawing_styles
#             .get_default_face_mesh_tesselation_style())
#         mp_drawing.draw_landmarks(
#             image=image,
#             landmark_list=face_landmarks,
#             connections=mp_face_mesh.FACEMESH_CONTOURS,
#             landmark_drawing_spec=None,
#             connection_drawing_spec=mp_drawing_styles
#             .get_default_face_mesh_contours_style())
#         mp_drawing.draw_landmarks(
#             image=image,
#             landmark_list=face_landmarks,
#             connections=mp_face_mesh.FACEMESH_IRISES,
#             landmark_drawing_spec=None,
#             connection_drawing_spec=mp_drawing_styles
#             .get_default_face_mesh_iris_connections_style())
#         
        
        forehead = face_landmarks.landmark[10]
        chin = face_landmarks.landmark[152]
        yTiltRatio = forehead.z-chin.z
        leftCheek = face_landmarks.landmark[234]
        rightCheek = face_landmarks.landmark[454]
        xTiltRatio = leftCheek.z-rightCheek.z
        xRatio = getXRatio(face_landmarks)
        if(xRatio >= 7.3):
            xText ="left"
        elif(7.3>xRatio> 6.7):
            xText = "mid"
        else:
            xText = "right"
            
        yRatio = getYRatio(face_landmarks,xText)
        if(yRatio >= 3):
            yText ="Top"
        elif(3>yRatio> 2.5):
            yText = "mid"
        else:
            yText = "Bottom"
        
        if(yTiltRatio >= 0.045):
            yTiltText ="top"
        elif(0.045>yTiltRatio> -0.002):
            yTiltText = "mid"
        else:
            yTiltText = "bottom"
            
        if(xTiltRatio >= 0.025):
            xTiltText ="left"
        elif(0.025>xTiltRatio> -0.025):
            xTiltText = "mid"
        else:
            xTiltText = "right"
        
        
        cv2.putText(image, f'X: {xText}', (20,70), cv2.FONT_HERSHEY_PLAIN,
                2,(0,255,0),3)
        cv2.putText(image, f'Y: {yText}', (20,100), cv2.FONT_HERSHEY_PLAIN,
                2,(0,255,0),3)
        cv2.putText(image, f'Y Tilt: {yTiltText}', (20,130), cv2.FONT_HERSHEY_PLAIN,
                2,(0,255,0),3)
        cv2.putText(image, f'X Tilt: {xTiltText}', (20,160), cv2.FONT_HERSHEY_PLAIN,
                2,(0,255,0),3)
        
    # Flip the image horizontally for a selfie-view display.
#     cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
    cv2.imshow('MediaPipe Face Mesh', image)
    k = cv2.waitKey(1) & 0xFF
    if  k == ord('q'):
        print(mp_face_mesh.FACEMESH_IRISES)
        break
    
    elif k == ord('a'):
        print(yRatio)
    elif k == ord('z'):
        print(face_landmarks.landmark[73])
        print(face_landmarks.landmark[68])
    
cap.release()