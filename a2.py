import cv2
cap=cv2.VideoCapture(0)

print ('hello')
#faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
faceCascade = cv2.CascadeClassifier('C:\\temp\\pos3\\dt\\cascade.xml')
#人脸发现的xml路径， 发现是发现有没有人脸， 识别是识别是哪张脸不一样。
print ('hello1')
#cap.set(3,1280)
#cap.set(4,960)
while cv2.waitKey(1)!=ord('q'):
    #time=datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
    #日期时间显示在左上角
    _,frame=cap.read()
    #frame=cv2.imread('a0.jpg')
    
    copy0=frame.copy()
    rects = faceCascade.detectMultiScale(copy0, 1.1, 3, 0)
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(copy0, (x1, y1), (x1+x2, y1+y2), (127, 255, 0), 2)
    cv2.imshow('copy',copy0)
