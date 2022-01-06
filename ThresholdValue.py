class ThresholdValue():
    def __init__(self,left=7.3,right=6.7,upper= 3,lower=2.55):
        self.left = left
        self.right = right
        self.upper =  upper
        self.lower = lower
        self.ratioList = []
        
        #RatioList Index
        # 0 Top Left
        # 1 Top Mid
        # 2 Top Right
        # 3 Lower Left
        # 4 Lower Mid
        # 5 Lower Right 
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
        self.upper = (averageMidY + averageTop)/2
        self.lower = (averageMidY + averageBottom)/2
        
        
        
    def xRatioToText(self,xRatio):
        if(xRatio >= self.left):
            xText ="left"
        elif(self.left > xRatio > self.right):
            xText = "mid"
        else:
            xText = "right"
        return xText
    
    def yRatioToText(self,yRatio):
        if(yRatio >= self.upper):
            yText ="Top"
        elif(self.upper>yRatio> self.lower):
            yText = "mid"
        else:
            yText = "Bottom"
        return yText
        
        
        