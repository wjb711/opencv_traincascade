# -*- coding: cp936 -*-

#���ģ��㶮��
import cv2
import datetime
import easygui
from easygui import msgbox, multenterbox
import numpy as np
from PIL import Image
import pytesseract
def image_colorfulness(image): 
    #��ͼƬ��ΪB,G,R�����֣�ע�⣬����õ���R��G��BΪ���������Ǳ����� 
    (B, G, R) = cv2.split(image.astype("float")) 

    #rg = R - G
    rg = np.absolute(R - G) 

    #yb = 0.5 * (R + G) - B
    yb = np.absolute(0.5 * (R + G) - B) 

    #����rg��yb��ƽ��ֵ�ͱ�׼��
    (rbMean, rbStd) = (np.mean(rg), np.std(rg)) 
    (ybMean, ybStd) = (np.mean(yb), np.std(yb)) 

    #����rgyb�ı�׼���ƽ��ֵ
    stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
    meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2)) 

    # ������ɫ�ḻ��C 
    return stdRoot + (0.3 * meanRoot)

#image = cv2.imread('ͼƬ·��') 
#print(image_colorfulness(image))

#�������ģ��
def pressESC(img,rect):
#�Զ��尴��esc���������¼����˴�������easybox
    cv2.imwrite('pic.jpg',img)
    image = 'pic.jpg'
        
    msg = "�Ƿ���뵽����ʶ�����?"
    choices = ["Yes","No","�˳�����"]
    reply = easygui.buttonbox(msg, image=image, choices=choices)
    if reply=="Yes" or reply=='pic.jpg':
        print (reply)
        if len(rect)==1:
        
            flavor = easygui.enterbox("���������֣�������Ӣ�ģ�ƴ�����������пո��������ţ�") 
            easygui.msgbox ("�������ˣ� " + flavor)
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
            easygui.msgbox ('û��������ֹһ��������ȷ����������')

    elif reply=="No" or reply==None:
        print (reply)
        pass
    #elif reply=='pic.jpg':
    #    flavor = easygui.enterbox("���������֣�������Ӣ�ģ�ƴ�����������пո��������ţ�") 
    #    easygui.msgbox ("�������ˣ� " + flavor)
    else:
        print ('reply is ',reply)
        cap.release()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
#������

    logo='GD'
    #���Ͻǵ�ͼ��
    promotion='press ESC'
    #���½ǵ���ʾ

    cap=cv2.VideoCapture(0)
    cv2.namedWindow('output',0)
    print ('hello')
    #faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faceCascade = cv2.CascadeClassifier('C:\\temp\\pos2\\dt\\cascade.xml')
    #�������ֵ�xml·���� �����Ƿ�����û�������� ʶ����ʶ������������һ����
    print ('hello1')
    cap.set(3,1280)
    cap.set(4,960)
    while cv2.waitKey(1)!=ord('q'):
        time=datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
        #����ʱ����ʾ�����Ͻ�
        _,frame=cap.read()
        #frame=cv2.imread('a0.jpg')
        
        copy0=frame.copy()
        


        #rects = faceCascade.detectMultiScale(copy0, 1.1, 2, cv2.CASCADE_SCALE_IMAGE, (20,20))
        rects = faceCascade.detectMultiScale(copy0, 1.2, 10, 0)
        #print (len(rects))
  
        for x1, y1, x2, y2 in rects:
            
            #cv2.rectangle(copy0, (x1, y1), (x1+x2, y1+y2), (127, 255, 0), 2)
            roi=frame[y1-20:y1+int(y2*1.1), x1-20:x1+int(x2*1.1)]
            
            #cv2.imwrite('a4.jpg',roi)
            value=image_colorfulness(roi)
            #print (value)
            if value >50:
                cv2.rectangle(copy0, (x1, y1), (x1+x2, y1+y2), (127, 255, 0), 2)
                #print (value)
                image = Image.fromarray(cv2.cvtColor(roi,cv2.COLOR_BGR2RGB)) 
                chepai=pytesseract.image_to_string(image,lang = 'chepai')
                print (chepai)
                #print ('len is ',len(chepai))
                #if '��' in chepai:
                #    print ('yes, �� in chepai')
                #    chepai=chepai.replace(' ','')
                #    n=chepai.find('��')
                #    if n>=0:
                #        label=chepai[n:n+7]
                #        print ('label is: ',label)
                #        cv2.imshow('output',copy0)
                #        input('any key to continue:')
                #if chepai=='��F16712':
                #    #print ('yes',len(chepai))
                #    pass
                #print ('done')
                resize=cv2.resize(roi,(300,150))
                copy0[0:150,0:300]=resize
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
    
    #���Ի������ĵ�һ�������� Ҳ����ͼƬ������
            except:
                pass
            


    cap.release()
    cv2.destroyAllWindows()
    
