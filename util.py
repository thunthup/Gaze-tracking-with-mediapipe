import math

def calDist(lm1,lm2):
    return math.sqrt((lm1.x-lm2.x)**2+(lm1.y-lm2.y)**2+(lm1.z-lm2.z)**2)

def getXRatio(face_landmarks):
    leftIris = face_landmarks.landmark[468]
    insideLeft = face_landmarks.landmark[133]
    outsideLeft = face_landmarks.landmark[33]
    xLeftRatio = math.log(calDist(leftIris,insideLeft)/calDist(leftIris,outsideLeft)*1000)
    rightIris = face_landmarks.landmark[473]
    insideRight = face_landmarks.landmark[362]
    outsideRight = face_landmarks.landmark[263]
    xRightRatio = math.log(calDist(rightIris,outsideRight)/calDist(rightIris,insideRight)*1000)
    xRatio = (xLeftRatio + xRightRatio)/2
    return xRatio

def getYRatio(face_landmarks,xText):
    leftIris = face_landmarks.landmark[468]
    insideLeft = face_landmarks.landmark[133]
    outsideLeft = face_landmarks.landmark[33]
    lowerLeft1 = face_landmarks.landmark[163]
    lowerLeft2 = face_landmarks.landmark[144]
    lowerLeft3 = face_landmarks.landmark[145]
    lowerLeft4 = face_landmarks.landmark[153]
    lowerLeft5 = face_landmarks.landmark[154]
    
    leftEyeSize = calDist(insideLeft,outsideLeft)
    
    if xText == "left":
        leftLowerDist = (calDist(leftIris,lowerLeft1) + calDist(leftIris,lowerLeft2)/leftEyeSize)
    elif xText == "mid":
        leftLowerDist = calDist(leftIris,lowerLeft3)/leftEyeSize *1.07
    else:
        leftLowerDist = (calDist(leftIris,lowerLeft4) + calDist(leftIris,lowerLeft5))/leftEyeSize/2.1
    
    yLeft = leftLowerDist*10
#     rightIris = face_landmarks.landmark[477]
#     upperRight = face_landmarks.landmark[362]
#     lowerRight = face_landmarks.landmark[263]
#     yRightRatio = math.log(calDist(rightIris,outsideRight)/calDist(rightIris,insideRight)*1000)
#     yRatio = (yLeftRatio + yRightRatio)/2
    return yLeft