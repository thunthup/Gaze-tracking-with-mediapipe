import math
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
        self.topR = 3
        self.midR   = 0
        self.bottomR = 2.7
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
        averageLeft = (ratioList[0][0] + ratioList[3][0] + ratioList[7][0])/3
        averageRight = (ratioList[2][0] + ratioList[5][0] + ratioList[8][0])/3
        averageMidX = (ratioList[1][0] + ratioList[4][0] + ratioList[6][0])/3
        averageTop = (ratioList[0][1] + ratioList[1][1] + ratioList[2][1])/3
        averageBottom = (ratioList[3][1] + ratioList[4][1] + ratioList[5][1])/3
        averageMidY = (ratioList[6][1] + ratioList[7][1] + ratioList[8][1])/3
        
        self.left = (averageMidX + averageLeft)/2
        self.right = (averageMidX + averageRight)/2
        self.top = (averageMidY + averageTop)/2
        self.bottom = (averageMidY + averageBottom)/2
        
        
        #y calibrate v2
#         self.topL = (ratioList[0][1] + ratioList[7][1])/2
#         self.midL   = ratioList[7][1]
#         self.bottomL = (ratioList[3][1] + ratioList[7][1])/2
#         self.topM = (ratioList[1][1] + ratioList[6][1])/2
#         self.midM   = ratioList[6][1]
#         self.bottomM = (ratioList[4][1] + ratioList[6][1])/2
#         self.topR = (ratioList[2][1] + ratioList[8][1])/2
#         self.midR   = ratioList[8][1]
#         self.bottomR = (ratioList[5][1] + ratioList[8][1])/2
        self.topL = math.sqrt(ratioList[0][1]*ratioList[7][1])
        self.midL   = ratioList[7][1]
        self.bottomL = math.sqrt(ratioList[3][1]*ratioList[7][1])
        self.topM = math.sqrt(ratioList[1][1]*ratioList[6][1])
        self.midM   = ratioList[6][1]
        self.bottomM = math.sqrt(ratioList[4][1]*ratioList[6][1])
        self.topR = math.sqrt(ratioList[2][1]*ratioList[8][1])
        self.midR   = ratioList[8][1]
        self.bottomR = math.sqrt(ratioList[5][1]*ratioList[8][1])
        
        
    def xRatioToText(self,xRatio):
        if(xRatio >= self.left):
            xText ="left"
        elif(self.left > xRatio > self.right):
            xText = "mid"
        else:
            xText = "right"
        return xText
    
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
        
        
        