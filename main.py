# -*- coding: cp936 -*-

#中文，你懂得
import cv2
import datetime
import easygui
from easygui import msgbox, multenterbox
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

#image = cv2.imread('图片路径') 
#print(image_colorfulness(image))

#导入各个模块
def pressESC(img,rect):
#自定义按了esc键后发生的事件，此处调用了easybox
    cv2.imwrite('pic.jpg',img)
    image = 'pic.jpg'
        
    msg = "是否加入到人脸识别库中?"
    choices = ["Yes","No","退出程序"]
    reply = easygui.buttonbox(msg, image=image, choices=choices)
    if reply=="Yes" or reply=='pic.jpg':
        print (reply)
        if len(rect)==1:
        
            flavor = easygui.enterbox("请输入名字（必须是英文（拼音），不能有空格和特殊符号）") 
            easygui.msgbox ("您输入了： " + flavor)
            folder='raw'
            name=folder+"/"+flavor+'.jpg'
            #easygui.msgbox (name)
            cv2.imwrite(name,img)
            for x1, y1, x2, y2 in rects:
            
            #cv2.rectangle(copy0, (x1, int(y1*0.7)), (x1+x2, y1+int(y2*1.3)), (127, 255, 0), 2)
                roi=img[y1:y1+y2, x1:x1+x2]
                folder1='faces'
                name1=folder1+"/"+flavor+'.jpg'
                cv2.imwrite(name1,roi)
            #print (roi)
        else:
            easygui.msgbox ('没有人脸或不止一张脸，请确保单人拍照')

    elif reply=="No" or reply==None:
        print (reply)
        pass
    #elif reply=='pic.jpg':
    #    flavor = easygui.enterbox("请输入名字（必须是英文（拼音），不能有空格和特殊符号）") 
    #    easygui.msgbox ("您输入了： " + flavor)
    else:
        print ('reply is ',reply)
        cap.release()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
#主函数

    logo='GD'
    #右上角的图标
    promotion='press ESC'
    #最下角的提示

    cap=cv2.VideoCapture(2)
    cv2.namedWindow('output',0)
    print ('hello')
    #faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faceCascade = cv2.CascadeClassifier('C:\\temp\\pos4\\dt\\cascade.xml')
    #人脸发现的xml路径， 发现是发现有没有人脸， 识别是识别是哪张脸不一样。
    print ('hello1')
    #cap.set(3,1280)
    #cap.set(4,960)
    mylist=[]
    i=0
    while i<20:
        time=datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
        #日期时间显示在左上角
        _,frame=cap.read()
        #frame=cv2.imread('a0.jpg')
        
        copy0=frame.copy()
        


        #rects = faceCascade.detectMultiScale(copy0, 1.1, 2, cv2.CASCADE_SCALE_IMAGE, (20,20))
        rects = faceCascade.detectMultiScale(copy0, 1.01, 5, 0)
        #print (len(rects))
  
        for x1, y1, x2, y2 in rects:
            
            #cv2.rectangle(copy0, (x1, y1), (x1+x2, y1+y2), (127, 255, 0), 2)
            roi=frame[y1:y1+y2, x1:x1+x2]
            
            
            #cv2.imwrite('a4.jpg',roi)
            value=image_colorfulness(roi)
            #print (value)
            if value >50:
                cv2.rectangle(copy0, (x1, y1), (x1+x2, y1+y2), (127, 255, 0), 2)
                #print (value)
                #image = Image.fromarray(cv2.cvtColor(roi,cv2.COLOR_BGR2RGB)) 
                #chepai=pytesseract.image_to_string(image,lang = 'chepai1')
                #print (chepai)
                #print ('len is ',len(chepai))
                #if '赣' in chepai:
                #    print ('yes, 赣 in chepai')
                #    chepai=chepai.replace(' ','')
                #    n=chepai.find('赣')
                #    if n>=0:
                #        label=chepai[n:n+7]
                #        print ('label is: ',label)
                #        cv2.imshow('output',copy0)
                #        input('any key to continue:')
                #if chepai=='赣F16712':
                #    #print ('yes',len(chepai))
                #    pass
                #print ('done')
                #resize=cv2.resize(roi,(300,150))
                kernel_size = (11, 11);
                sigma = 1.5
                img = cv2.GaussianBlur(roi, kernel_size, sigma)
                gray=cv2.cvtColor(img,6)
                ret, gray = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2, 2))
                gray = cv2.erode(gray,kernel)


                
                _,contours, hierarchy = cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                for c in contours:
    # find bounding box coordinates
    # 现计算出一个简单的边界框
                    x, y, w, h = cv2.boundingRect(c)   # 将轮廓信息转换成(x, y)坐标，并加上矩形的高度和宽度
                    #cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)  # 画出矩形
                    if h >20:
                        hello=roi[y:y+h,x:x+w]
                        cv2.imshow('frame',hello)
                #cv2.drawContours(frame,contours,-1,(0,0,255),3)
                
                
                #ret,gray=cv2.threshold(gray,140,255,cv2.THRESH_BINARY_INV)
                #gray = cv2.Canny(gray, 80, 150)  
                #x = cv2.Sobel(gray,cv2.CV_16S,1,0)  
                #y = cv2.Sobel(gray,cv2.CV_16S,0,1)  
  
                #absX = cv2.convertScaleAbs(x)   # 转回uint8  
                #absY = cv2.convertScaleAbs(y)  
  
                #dst = cv2.addWeighted(absX,0.5,absY,0.5,0)
                #ret,dst=cv2.threshold(dst,40,255,cv2.THRESH_BINARY)
                #_,contours, hierarchy = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 画出轮廓，-1,表示所有轮廓，画笔颜色为(0, 255, 0)，即Green，粗细为3
                #cv2.drawContours(dst, contours, -1, (0, 255, 0), 2)
                
                #kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2, 2))
                #dst = cv2.erode(dst,kernel)
                #for cnt in contours:
                #    if cv2.contourArea(cnt)>10:
                #cv2.drawContours(copy0, contours, -1, (0, 255, 0), 3)
                #cv2.imshow('dst',copy0)
#腐蚀图像  
                #dst = cv2.erode(dst,kernel)
                #dst = cv2.erode(dst,kernel) 
                #kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5, 5))  
  
#闭运算  
                #closed = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, kernel)
                #closed = cv2.morphologyEx(closed, cv2.MORPH_CLOSE, kernel) 

                gray=cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
                image = Image.fromarray(cv2.cvtColor(hello,cv2.COLOR_BGR2RGB)) 
                chepai=pytesseract.image_to_string(image,lang = 'chepai')
                mylist.append(chepai)
                i=i+1
                #print (chepai)
                #copy0[0:150,0:300]=gray
        cv2.imshow('output',copy0)
                #cv2.imshow('roi',resize)
                #input('a')
                #cv2.imwrite('a4.jpg',roi)
                #font = cv2.FONT_HERSHEY_DUPLEX
        #cv2.putText(copy0, logo, (600, 10), font, 0.5, (0, 0, 0), 1)
        #cv2.putText(copy0, time, (0, 10), font, 0.5, (255, 255, 255), 1)
        #cv2.putText(copy0, promotion, (0, 470), font, 0.5, (0, 0, 255), 1)
        
        if cv2.waitKey(1)==27:
            try:
                pressESC(copy0,rects)
    
    #尝试获得命令的第一个参数， 也就是图片的名字
            except:
                pass
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
           


    cap.release()
    cv2.destroyAllWindows()
    
