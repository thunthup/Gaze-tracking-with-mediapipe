import math


def calDist(lm1, lm2):
    # calculate the distance of (x1,y1,z1) and (x2,y2,z2) from landmarks
    return math.sqrt((lm1.x-lm2.x)**2+(lm1.y-lm2.y)**2+(lm1.z-lm2.z)**2)


def calDistY(lm1, lm2):

    return lm1.y-lm2.y


def getXRatio(face_landmarks):
    leftIris = face_landmarks.landmark[468]
    insideLeft = face_landmarks.landmark[133]
    outsideLeft = face_landmarks.landmark[33]
    # calculate ratio of distance between iris and outside eye corner and inside eye corner
    xLeftRatio = (calDist(leftIris, insideLeft) /
                  calDist(leftIris, outsideLeft)*100)
    rightIris = face_landmarks.landmark[473]
    insideRight = face_landmarks.landmark[362]
    outsideRight = face_landmarks.landmark[263]
    xRightRatio = (calDist(rightIris, outsideRight) /
                   calDist(rightIris, insideRight)*100)
    # find the average of both eyes
    xRatio = (xLeftRatio + xRightRatio)/2
    return xRatio

# def getYRatio(face_landmarks,xText):
#     leftIris = face_landmarks.landmark[468]
#     insideLeft = face_landmarks.landmark[133]
#     outsideLeft = face_landmarks.landmark[33]
#     lowerLeft1 = face_landmarks.landmark[163]
#     lowerLeft2 = face_landmarks.landmark[144]
#     lowerLeft3 = face_landmarks.landmark[145]
#     lowerLeft4 = face_landmarks.landmark[153]
#     lowerLeft5 = face_landmarks.landmark[154]
#
#     leftEyeSize = calDist(insideLeft,outsideLeft)
#
#     if xText == "left":
#         leftLowerDist = (calDist(leftIris,lowerLeft1) + calDist(leftIris,lowerLeft2)/leftEyeSize)
#     elif xText == "mid":
#         leftLowerDist = calDist(leftIris,lowerLeft3)/leftEyeSize
#     else:
#         leftLowerDist = (calDist(leftIris,lowerLeft4) + calDist(leftIris,lowerLeft5))/leftEyeSize
#
#     yLeft = leftLowerDist*100
#     return yLeft


def getYTiltRatio(face_landmarks):
    forehead = face_landmarks.landmark[10]
    chin = face_landmarks.landmark[152]
    yTiltRatio = forehead.z-chin.z
    return yTiltRatio


def getXTiltRatio(face_landmarks):
    leftCheek = face_landmarks.landmark[234]
    rightCheek = face_landmarks.landmark[454]
    xTiltRatio = leftCheek.z-rightCheek.z
    return xTiltRatio


def getYRatio(face_landmarks):
    leftIris = face_landmarks.landmark[468]
    insideLeft = face_landmarks.landmark[133]
    outsideLeft = face_landmarks.landmark[33]
    leftEyeSize = calDist(insideLeft, outsideLeft)
    yRatio = calDist(leftIris, face_landmarks.landmark[7])\
        + calDist(leftIris, face_landmarks.landmark[163]) \
        + calDist(leftIris, face_landmarks.landmark[154])\
        + calDist(leftIris, face_landmarks.landmark[155])
    return yRatio/leftEyeSize


def getYRatio2(face_landmarks):
    leftIris = face_landmarks.landmark[468]
    insideLeft = face_landmarks.landmark[133]
    outsideLeft = face_landmarks.landmark[33]
    leftEyeSize = calDist(insideLeft, outsideLeft)
    yRatio = calDist(leftIris, face_landmarks.landmark[145])

    return yRatio/leftEyeSize


def getSectionFromXY(X, Y, div, width=1920, height=1080):
    divx, divy = div
    xBorders = [(0 + width*e//divx) for e in range(divx)]
    yBorders = [(0 + height*e//divy) for e in range(divy)]
    xSection = 0
    ySection = 0
    for idx in range(divx-1, -1, -1):
        if X > xBorders[idx]:
            xSection = idx
            break
    for idx in range(divy-1, -1, -1):
        if Y > yBorders[idx]:
            ySection = idx
            break
    return (xSection, ySection)


def getMousePosFromSection(sections, div, width=1920, height=1080):
    divx, divy = div
    xSection, ySection = sections
    xPos = int(width*(xSection+0.5)/divx)
    yPos = int(height*(ySection+0.5)/divy)
    return (xPos, yPos)
