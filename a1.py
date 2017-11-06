import cv2
import numpy as np
from PIL import Image
import pytesseract
def image_colorfulness(image): 
    #将图片分为B,G,R三部分（注意，这里得到的R、G、B为向量而不是标量） 
    (B, G, R) = cv2.split(image.astype("float")) 

    #rg = R - G
    rg = np.absolute(R - G) 

    #yb = 0.5 * (R + G) - B
    yb = np.absolute(0.5 * (R + G) - B) 

    #计算rg和yb的平均值和标准差
    (rbMean, rbStd) = (np.mean(rg), np.std(rg)) 
    (ybMean, ybStd) = (np.mean(yb), np.std(yb)) 

    #计算rgyb的标准差和平均值
    stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
    meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2)) 

    # 返回颜色丰富度C 
    return stdRoot + (0.3 * meanRoot)
cap=cv2.VideoCapture(0)
faceCascade = cv2.CascadeClassifier('C:\\temp\\pos2\\dt\\cascade.xml')
l=[]
count_times = []
while cv2.waitKey(1)!=27:
    _,frame=cap.read()
    copy0=frame.copy()
    gray=cv2.cvtColor(frame,6)
    gray_lap = cv2.Laplacian(gray,cv2.CV_16S,ksize = 3)  
    dst = cv2.convertScaleAbs(gray_lap)
    rects = faceCascade.detectMultiScale(frame, 1.1, 5, 0)
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(gray, (x1, y1), (x1+x2, y1+y2), (127, 255, 0), 2)
        #cv2.imshow('rect',rects)
        roi=frame[y1:y1+y2, x1:x1+x2]
        value=image_colorfulness(roi)
        
        #print (value)
        if value>30:
        #print(roi.shape)
        #gray=cv2.cvtColor(roi,6)
        #gray_lap = cv2.Laplacian(roi,cv2.CV_16S,ksize = 3)  
        #dst = cv2.convertScaleAbs(gray_lap)
            image = Image.fromarray(cv2.cvtColor(roi,cv2.COLOR_BGR2RGB))
            chepai=pytesseract.image_to_string(image,lang = 'chepai')
            print (chepai)
            l.append(chepai)
        
        
 
        

    cv2.imshow('1',gray)
print ('l is here:',l)
for i in l :
    count_times.append(l.count(i))
 
m = max(count_times)
print ('m is :',m)
n = l.index(m)
 
print (l[n])
