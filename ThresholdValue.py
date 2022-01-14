import math
import numpy as np
class ThresholdValue():
    def __init__(self,left=7.3,right=6.7,top= 3,bottom=2.55):
        self.left = left
        self.right = right
        self.top =  top
        self.bottom = bottom
        self.ratioList = []
        self.topL = 3
        self.midL   = 0
        self.bottomL = 2.55
        self.topM = 3
        self.midM   = 0
        self.bottomM = 2.75
        self.topR = 5.7
        self.midR   = 0
        self.bottomR = 5
        #RatioList Index
        # 0 Top Left
        # 1 Top Mid
        # 2 Top Right
        # 3 bottom Left
        # 4 bottom Mid
        # 5 bottom Right 
        # 6 Mid Mid
        # 7 Mid Left
        # 8 Mid Right
        
        
    def calibrate(self,ratioList):
        self.ratioList = ratioList
        
        averageLeft = np.mean([ratioList[0,:,0],ratioList[3,:,0], ratioList[7,:,0]])
        averageRight = np.mean([ratioList[2,:,0], ratioList[5,:,0] , ratioList[8,:,0]])
        averageMidX = np.mean([ratioList[1,:,0] , ratioList[4,:,0] , ratioList[6,:,0]])

        self.left = np.mean([averageMidX , averageLeft])
        self.right = np.mean([averageMidX , averageRight])

        self.topL = np.mean([ratioList[0,:,1],ratioList[7,:,1]])
        self.midL   = np.mean(ratioList[7,:,1])
        self.bottomL = np.mean([ratioList[3,:,1],ratioList[7,:,1]])
        self.topM = np.mean([ratioList[1,:,1],ratioList[6,:,1]])
        self.midM   = np.mean(ratioList[6,:,1])
        self.bottomM = np.mean([ratioList[4,:,1],ratioList[6,:,1]])
        self.topR = np.mean([ratioList[2,:,1],ratioList[8,:,1]])
        self.midR   = np.mean(ratioList[8,:,1])
        self.bottomR = np.mean([ratioList[5,:,1],ratioList[8,:,1]])
        
        
    def xRatioToText(self,xRatio):
        if(xRatio >= self.left):
            xText ="left"
        elif(self.left > xRatio > self.right):
            xText = "mid"
        else:
            xText = "right"
        return xText
    
    def xRatioToInt(self,xRatio):
        if(xRatio >= self.left):
            xInt =1
        elif(self.left > xRatio > self.right):
            xInt = 0
        else:
            xInt = -1
        return xInt
    
    def yRatioToText(self,yRatio,xText):
        
        if xText == "left":
            topThres = self.topL
            bottomThres = self.bottomL
        elif xText == "mid":
            topThres = self.topM
            bottomThres = self.bottomM
        elif xText == "right":
            topThres = self.topR
            bottomThres = self.bottomR
            
        if(yRatio >= topThres):
            yText ="Top"
        elif(topThres>yRatio> bottomThres):
            yText = "mid"
        else:
            yText = "Bottom"
        return yText
        
    def yRatioToInt(self,yRatio,xText):
        if xText == "left":
            topThres = self.topL
            bottomThres = self.bottomL
        elif xText == "mid":
            topThres = self.topM
            bottomThres = self.bottomM
        elif xText == "right":
            topThres = self.topR
            bottomThres = self.bottomR
            
        if(yRatio >= topThres):
            yInt = 1
        elif(topThres>yRatio> bottomThres):
            yInt = 0
        else:
            yInt = -1
        return yInt
        
        