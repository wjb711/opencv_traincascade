import cv2
import datetime
import easygui
from easygui import msgbox, multenterbox
import numpy as np
from PIL import Image
import pytesseract
def nothing(x):
    pass
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
cv2.namedWindow('A1',0)
cap=cv2.VideoCapture(2)
faceCascade = cv2.CascadeClassifier('C:\\temp\\pos4\\dt\\cascade.xml')
cv2.createTrackbar('1st', 'A1', 72, 299, nothing)
cv2.createTrackbar('2nd', 'A1', 8, 10, nothing)
cv2.createTrackbar('3rd', 'A1', 37, 360, nothing)
#创建一个叫做thrs1的滑动条，默认值是127， 在0-255的范围内， 手动调整阀值范围， 调用上面的nothing模块，其实相当于什么都没做，这是格式要求的。
    #while(True):
#循环，为什么要循环？因为手动调整阀值，效果跟着变，不停地调整，不停的变，所以要循环
mylist=[]
i=0
while i<20:
    _,frame=cap.read()
    
    copy0=frame.copy()
    thrs1 = cv2.getTrackbarPos('1st', 'A1')
    thrs2 = cv2.getTrackbarPos('2nd', 'A1')
    thrs3 = cv2.getTrackbarPos('3rd', 'A1')
    rects = faceCascade.detectMultiScale(copy0, (thrs1+101)/100, thrs2, 0)

    for x1, y1, x2, y2 in rects:
        roi=frame[y1:y1+y2, x1:x1+x2]
            
            
            #cv2.imwrite('a4.jpg',roi)
        value=image_colorfulness(roi)
        if value > thrs3:
            hello=roi
            cv2.rectangle(copy0, (x1, y1), (x1+x2, y1+y2), (127, 255, 0), 2)
            kernel_size = (11, 11);
            sigma = 1.5
            img = cv2.GaussianBlur(roi, kernel_size, sigma)
            gray=cv2.cvtColor(img,6)
            gray=cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            image = Image.fromarray(cv2.cvtColor(hello,cv2.COLOR_BGR2RGB)) 
            chepai=pytesseract.image_to_string(image,lang = 'chi_sim')
            if chepai !='':
                mylist.append(chepai)
                i=i+1
    print (rects)
    cv2.imshow('A1',copy0)
    cv2.waitKey(1)
print (mylist)
myset = set(mylist)
print (myset)
    #myset是另外一个列表，里面的内容是mylist里面的无重复 项
dict1={}
max=0
for item in myset:
  #print("the %d has found %d" %(item,mylist.count(item)))
  #print (mylist.count(item))
  if mylist.count(item)>max:
      max=mylist.count(item)
      max_item=item
  dict1[item]=mylist.count(item)
print ('dict is',dict1)
print ('max_item is :',max_item)
print ('max time is :',max)
