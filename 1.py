import enum
import math
import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
cap = cv2.VideoCapture(0)
cap.set(3,800) #width
cap.set(4,600) #height
detector = HandDetector(detectionCon=0.7,maxHands=1) # تحديد الايد للعبه

class SnakeGame:
    def __init__(self, pathFood):
        self.points = [] #تحديد جميع نقاط الثعبان 
        self.length = [] # طول كل نقطه
        self.currentLenght = 0 # الطول الكامل للثعبان
        self.allowedLength = 100 # الطول الاجمال للثعبان
        self.perviousHead = 0,0 # النقطه الرئسية السابقة

        self.imageFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood , _ = self.imageFood.shape
        self.foodPoints = 0 , 0
        self.randomFoodLocation()        
    def randomFoodLocation(self):
        self.foodPoints = random.randint(100, 600), random.randint(100, 400)


    def update(self , imgMain , currentHead):
        px , py = self.perviousHead
        cx , cy = currentHead
        self.points.append([cx,cy])
        distance = math.hypot(cx - px , cy - py)
        self.length.append(distance)
        self.currentLenght += distance
        self.perviousHead = cx ,cy
        
        # اكل الطعام
        rx , ry =self.foodPoints
        if rx - self.wFood//2 < cx < rx + self.wFood//2 and ry - self.hFood//2 < cy < ry + self.hFood//2:
            self.randomFoodLocation()
            self.allowedLength += 25
        # تنقيص الطول 
        if self.currentLenght > self.allowedLength:
            for i , length in enumerate(self.length):
                self.currentLenght -= length # يقوم بتنقيصه
                self.length.pop(i) #التحقق منها
                self.points.pop(i)
                if self.currentLenght < self.allowedLength: # اذا كان اصغر من الحجم المسموح تابع 
                    break
        # للرسم الثعبان
        if self.points:
            for i , points in enumerate(self.points):
                if i != 0 :
                    # يرسم الخط ويحدد النقطة الاولى والنقطة الثانية
                    cv2.line(imgMain,self.points[i-1],self.points[i],(0,0,255),20)
                cv2.circle(imgMain,self.points[-1],20,(200,0,200),cv2.FILLED)
        # رسم الطعام
            rx , ry = self.foodPoints
            imgMain = cvzone.overlayPNG(self.imageFood,
                                        (rx-self.wFood//2,ry-self.hFood//2)
                                        )
        return imgMain
game = SnakeGame('apple.png')
while True:
    success , img = cap.read()
    img = cv2.flip(img,1) # اعكس لي الصورة بقيمة 1
    hands, img = detector.findHands(img,flipType=False) # اوجد الايد في الكاميره
    
    if hands:
        lmList = hands[0]['lmList'] # قانون هاند ماركس
        # x - y - z
        pointIndex = lmList[8][0:2] # قيمة اليد السبابه 
        #يحدد خصائص اليد التى تتحكم بالعبة 
        # cv2.circle(img,pointIndex,20,(200,0,200),cv2.FILLED)
        img = game.update(img,pointIndex)
    cv2.imshow("Snake Game [python AI]", img)
    key = cv2.waitKey(1)
