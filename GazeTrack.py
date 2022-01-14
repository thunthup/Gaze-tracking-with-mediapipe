import cv2
import mediapipe as mp
from util import getXRatio, getYRatio, getYTiltRatio, getXTiltRatio
from ThresholdValue import ThresholdValue
import numpy as np
import time


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
ratioList = np.ndarray((9,30,2))
thresholds = ThresholdValue()
calibrating = True
calibateStepXTextList = ["left","mid","right","left","mid","right","mid","left","right"]
testWidth = 1920
testHeight = 1080 
circleLocations = [(30,30),(testWidth//2,30),(testWidth-30,30),(30,testHeight-25),(testWidth//2,testHeight-25),(testWidth-30,testHeight-25),(testWidth//2,testHeight//2),(30,testHeight//2),(testWidth-30,testHeight//2)]
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
calibrateStep = 0
valueCount = 0
cv2.namedWindow("Calibrate Screen", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Calibrate Screen",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

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
    blackScreen = np.zeros((testHeight,testWidth))
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
        yTiltRatio = getYTiltRatio(face_landmarks)
        xTiltRatio = getXTiltRatio(face_landmarks)
        
        xRatio = getXRatio(face_landmarks)
        xText = thresholds.xRatioToText(xRatio)
            
        yRatio = getYRatio(face_landmarks,xText)
        yText = thresholds.yRatioToText(yRatio,xText)
        
        xInt = thresholds.xRatioToInt(xRatio)
        yInt = thresholds.yRatioToInt(yRatio,xText)
        
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
        
        if not calibrating:
            cv2.putText(image, f'X: {xText,xRatio}', (20,70), cv2.FONT_HERSHEY_PLAIN,
                    2,(0,255,0),3)
            cv2.putText(image, f'Y: {yText,yRatio}', (20,100), cv2.FONT_HERSHEY_PLAIN,
                    2,(0,255,0),3)
            cv2.putText(image, f'Y Tilt: {yTiltText,yTiltRatio}', (20,130), cv2.FONT_HERSHEY_PLAIN,
                    2,(0,255,0),3)
            cv2.putText(image, f'X Tilt: {xTiltText,xTiltRatio}', (20,160), cv2.FONT_HERSHEY_PLAIN,
                    2,(0,255,0),3)
            for i in range(9):
                blackScreen = cv2.circle(blackScreen, circleLocations[i], 5, (255, 0, 0), 2)
            blackScreen = cv2.rectangle(blackScreen, (testWidth*(1-xInt)//3,testHeight*(1-yInt)//3),\
                                        (testWidth*(2-xInt)//3-1,testHeight*(2-yInt)//3-1), (255, 0, 0), 2)
            
        if calibrating:
            
            if calibrateStep < 9:
                
                blackScreen = cv2.circle(blackScreen, circleLocations[calibrateStep], 5, (255, 0, 0), 2)   
                cv2.putText(image, f'Calibrating:{calibrateStep}', (20,70), cv2.FONT_HERSHEY_PLAIN,
                    2,(0,255,0),3)
                cv2.putText(blackScreen, "Look at the white circle and press any key ..", \
                            (testWidth//2-300,testHeight//2+30), cv2.FONT_HERSHEY_PLAIN,
                    1.5,(255,0,0),2)
                cv2.imshow('Calibrate Screen',blackScreen)
                cv2.imshow('MediaPipe Face Mesh', image)
                time.sleep(0.008)
                
                if valueCount == 0: cv2.waitKey(0)
                if valueCount < 30:
                    ratioList[calibrateStep,valueCount]=[getXRatio(face_landmarks),\
                                                         getYRatio(face_landmarks,calibateStepXTextList[calibrateStep])]
                    valueCount = valueCount + 1
                else:
                    calibrateStep = calibrateStep + 1
                    valueCount = 0
                    
                    
            else:
                calibrating = False
                calibrateStep = 0
                valueCount = 0
                thresholds.calibrate(ratioList)
                
            
                    
                
                
        
    # Flip the image horizontally for a selfie-view display.
#     cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
    
    
 
    cv2.imshow('Calibrate Screen',blackScreen)
    cv2.imshow('MediaPipe Face Mesh', image)
    k = cv2.waitKey(2) & 0xFF
    if  k == ord('q'):
        print(mp_face_mesh.FACEMESH_IRISES)
        break
    
    elif k == ord('a'):
        print(yRatio)
    elif k == ord('z'):
        print(face_landmarks.landmark[73])
        print(face_landmarks.landmark[68])
    elif k == ord('c'):
        
       
        calibrating = True
    elif k == ord('d'):
        thresholds.calibrate(ratioList)
        print(thresholds.left,thresholds.right)
        
    elif k == ord('r'):
        ratioList = np.ndarray((9,30,2))
        calibrating = False
        calibrateStep = 0
        valueCount = 0
    
cap.release()
cv2.destroyAllWindows()