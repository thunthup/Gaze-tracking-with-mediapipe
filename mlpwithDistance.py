import cv2
import mediapipe as mp
from util import getSectionFromXY, getXRatio, getYRatio, getYTiltRatio, getXTiltRatio, getYRatio2, getMousePosFromSection
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import time
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sklearn import linear_model
import pyautogui
from sklearn.neural_network import MLPRegressor
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
ratioList = []
xRatioList = []
yRatioList = []
yList = []
xList = []
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
emaXList = []
emaYList = []
sleeping = 0
DIV = (4, 4)
testWidth = 1920
testHeight = 1080
moveCursor = 0
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
calibrating = 0
fitted = 0
xEstimator = MLPRegressor(max_iter=500000,
                          hidden_layer_sizes=(4, ),)
yEstimator = MLPRegressor(max_iter=500000,
                          hidden_layer_sizes=(4, ),)
poly = PolynomialFeatures(degree=2)


def add_data(x, y):

    ratioList.append([xRatio, yRatio, yRatio2])
    xRatioList.append(xRatio)
    yRatioList.append(yRatio)
    yList.append(y)
    xList.append(x)


cv2.namedWindow("Calibrate Screen", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Calibrate Screen",
                      cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

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
        blackScreen = np.ones((testHeight, testWidth))
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

                xRatio = getXRatio(face_landmarks)
                yRatio = getYRatio(face_landmarks)
                yRatio2 = getYRatio2(face_landmarks)
                #xTiltRatio = getXTiltRatio(face_landmarks)
                #yTiltRatio = getYTiltRatio(face_landmarks)

                cv2.putText(image, f'Xr: {xRatio}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                            2, (0, 255, 0), 3)
                cv2.putText(image, f'Yr: {yRatio}', (20, 100), cv2.FONT_HERSHEY_PLAIN,
                            2, (0, 255, 0), 3)
                if fitted:
                    polyVariablesTemp = poly.fit_transform(
                        [[xRatio, yRatio,  yRatio2]])
                    xCursorTemp = int(xEstimator.predict(polyVariablesTemp))
                    yCursorTemp = int(yEstimator.predict(polyVariablesTemp))
                    if xCursorTemp < 0:
                        xCursorTemp = 0
                    if xCursorTemp > 1915:
                        xCursorTemp = 1915
                    if yCursorTemp < 0:
                        yCursorTemp = 0
                    if yCursorTemp > 1075:
                        yCursorTemp = 1075

                    emaXList.append(xCursorTemp)
                    emaYList.append(yCursorTemp)
                    if(len(emaXList) > 25):
                        emaXList.pop(0)
                    if(len(emaYList) > 25):
                        emaYList.pop(0)
                    xPredict = int(np.mean(emaXList))
                    yPredict = int(np.mean(emaYList))
                    blackScreen = cv2.circle(
                        blackScreen, (xPredict, yPredict), 5, (0, 0, 0), 2)
                    sections = getSectionFromXY(xPredict, yPredict, DIV)
                    xMousePos, yMousePos = getMousePosFromSection(
                        sections, DIV)
                    if moveCursor:
                        pyautogui.moveTo(xMousePos, yMousePos, duration=0)
                if not calibrating:
                    for i in range(DIV[0]):
                        for j in range(DIV[1]):
                            blackScreen = cv2.circle(
                                blackScreen, getMousePosFromSection((i, j), DIV), 5, (0, 0, 0), 2)
                if calibrating:
                    if calibrateCounterJ < 4:
                        if calibrateCounterI < 4:
                            if calibrateRep == 0:
                                time.sleep(0.5)
                            calibratingPoint = getMousePosFromSection(
                                (calibrateCounterI, calibrateCounterJ), DIV)
                            blackScreen = cv2.circle(
                                blackScreen, calibratingPoint, 8, (0, 0, 0), 2)
                            cv2.circle(
                                blackScreen, calibratingPoint, 20, (189, 255, 201), 10)
                            cv2.imshow('Calibrate Screen', blackScreen)
                            add_data(calibratingPoint[0], calibratingPoint[1])

                        if calibrateRep < 130:
                            calibrateRep = calibrateRep + 1
                        elif calibrateRep == 130:
                            calibrateRep = 0
                            blackScreen = np.ones((testHeight, testWidth))
                            cv2.imshow('Calibrate Screen', blackScreen)
                            #sleeping = 1
                            if calibrateCounterI < 3:
                                calibrateCounterI = calibrateCounterI + 1
                            elif calibrateCounterI == 3:
                                calibrateCounterI = 0
                                calibrateCounterJ = calibrateCounterJ + 1
                    else:
                        calibrating = 0
                        polyVariables = poly.fit_transform(ratioList)
                        xEstimator.fit(polyVariables, xList)
                        yEstimator.fit(polyVariables, yList)
                        fitted = 1
                    # Flip the image horizontally for a selfie-view display.
                    #     cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
        if sleeping:
            time.sleep(1)
            sleeping = sleeping - 1
            blackScreen = np.ones((testHeight, testWidth))
        cv2.imshow('Calibrate Screen', blackScreen)
        cv2.imshow('MediaPipe Face Mesh', image)

        k = cv2.waitKey(2) & 0xFF
        if k == ord('q'):
            # print(mp_face_mesh.FACEMESH_IRISES)
            break

        elif k == ord('a'):
            print(ratioList)
        elif k == ord('x'):

            x, y = np.array(xRatioList), np.array(yRatioList)
            # z = np.array([yEstimator.predict(ratioList)])
            # a,b,c =xEstimator
            print(xEstimator.coef_, xEstimator.intercept_)
            mpl.rcParams['legend.fontsize'] = 12

            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')

            ax.scatter(xRatioList, yRatioList, xList, label='x', s=5)
            ax.set_xlabel('X Ratio')
            ax.set_ylabel('Y Ratio')
            ax.set_zlabel('X Coor')
            ax.legend()
            ax.view_init(45, 0)
            # ax.plot_surface(xRatioList, yRatioList, z)
            plt.show()
        elif k == ord('y'):

            x, y = np.array(xRatioList), np.array(yRatioList)
            # z = np.array([yEstimator.predict(ratioList)])
            mpl.rcParams['legend.fontsize'] = 12

            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
            ax.set_xlabel('X Ratio')
            ax.set_ylabel('Y Ratio')
            ax.set_zlabel('Y Coor')
            ax.scatter(xRatioList, yRatioList, yList, label='y', s=5)
            ax.legend()
            # print(yEstimator.predict(ratioList))
            # ax.plot_surface(xRatioList, yRatioList, z)
            ax.view_init(45, 0)

            plt.show()
        elif k == ord('c'):
            calibrating = 1
            calibrateCounterI = 0
            calibrateCounterJ = 0
            calibrateRep = 0
        elif k == ord('d'):
            moveCursor = not moveCursor

        elif k == ord('r'):
            pass

cap.release()
cv2.destroyAllWindows()
