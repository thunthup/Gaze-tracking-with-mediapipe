class ThresholdValue():
    def __init__(self,left=7.3,right=6.7,upper= 3.08,lower=2.55):
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
        
        
        