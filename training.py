'''
本脚本的目的是为了生成自动训练器，使得opencv可以识别物体
'''
import os,cv2,easygui as g
#判断是否存在pos文件夹，neg文件夹， dr最终目标路径


def resize(folder,width,high):
    os.chdir(folder)
    for b in os.listdir():
        if b.endswith('.jpg'):
            pic=cv2.imread(b)
            if pic.shape==(high,width,3):

                print ('y',pic.shape)
            else:
                re=cv2.resize(pic,(width,high))
                print ('n',pic.shape)
                cv2.imwrite(b,re)
    os.chdir('../')
def precondition():
    #判断是否存在pos正样本文件夹，neg负样本文件夹，dr，最终目标文件夹
    #global pos_width
    #print (pos_width)
    if os.path.exists('pos'):
        
        a=exist('pos','.jpg',pos_min_number)
        if a[0]:
            #g.msgbox('正样本数量为 '+str(a[1])+'\n'+'最低要求数量为'+str(pos_min_number))
            global pos_real_num
            pos_real_num=a[1]
        else:
            return False
    else:
        os.mkdir('pos')
    if os.path.exists('neg'):
        c=exist('neg','.jpg',neg_min_number)
        if c[0]:
            #g.msgbox('负样本数量为 '+str(c[1])+'\n'+'最低要求数量为'+str(neg_min_number))
            global neg_real_num
            neg_real_num=c[1]
        else:
            return False
    else:
        os.mkdir('neg')
    if os.path.exists('dt'):
        pass
    else:
        os.mkdir('dt')

            
def exist(location,houzhui,min_num):
    i=0
    for b in os.listdir(location):
        if b.endswith(houzhui):
            i=i+1
    
    
    if i>=min_num:
        return True,i
    else:
        g.msgbox(location+' '+houzhui+'样本数量不足 '+str(min_num)+'\n'+'最低要求数量为'+str(neg_min_number))
        return False
        

def pos_text():
    with open("pos.txt","w") as f:
        for b in os.listdir('pos'):
            print ('pos'+'/'+b+' 1 0 0 '+str(pos_width)+' '+str(pos_high))

            f.write('pos'+'/'+b+' 1 0 0 '+str(pos_width)+' '+str(pos_high)+'\n')        


def neg_text():
    with open("neg.txt","w") as f:
        for b in os.listdir('neg'):
            print ('neg'+'/'+b)

            f.write('neg'+'/'+b+'\n')             
    
pos_high=19
pos_width=78
neg_high=19
neg_width=78
#正样本最低数量
pos_min_number=10
#负样本最低数量
neg_min_number=50       
if __name__=='__main__':
    precondition()
    pos_text()
    neg_text()
    resize('pos',pos_width,pos_high)
    #resize('neg',neg_width,neg_high)
    print ('.\\bin\\opencv_createsamples.exe -info pos.txt -bg neg.txt -maxidev 40 -maxxangle 1.100000 -maxyangle 1.100000 -maxzangle 0.5 -num '+str(pos_real_num)+' -vec pos.vec -w '+str(pos_width)+' -h '+str(pos_high))
    os.system('.\\bin\\opencv_createsamples.exe -info pos.txt -bg neg.txt -maxidev 40 -maxxangle 1.100000 -maxyangle 1.100000 -maxzangle 0.5 -num '+str(pos_real_num)+' -vec pos.vec -w '+str(pos_width)+' -h '+str(pos_high))
    print ('done')
    #print ('.\\bin\\opencv_haartraining.exe -data dt -vec pos.vec -bg neg.txt -numPos '+str(pos_real_num)+' -numNeg '+str(pos_real_num)+' -numStages 16 -precalcValbufSize 4096 -precalcdxBufSize 4096 -featureType LBP')
    #os.system('.\\bin\\opencv_haartraining.exe -data dt -vec pos.vec -bg neg.txt -numPos '+str(pos_real_num)+' -numNeg '+str(pos_real_num)+' -numStages 16 -precalcValbufSize 4096 -precalcdxBufSize 4096 -featureType LBP')
    #print ('done all')
    print ('.\\bin\\opencv_traincascade.exe -data dt -vec pos.vec -bg neg.txt -numPos '+str(pos_real_num)+' -numNeg '+str(pos_real_num)+' -numStages 20 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -mode ALL -precalcValbufSize 4096 -precalcdxBufSize 4096 -featureType LBP -w '+str(pos_width)+' -h '+str(pos_high))
    #os.system('.\\bin\\opencv_traincascade.exe -data dt -vec pos.vec -bg neg.txt -numPos '+str(pos_real_num)+' -numNeg '+str(pos_real_num)+' -numStages 16 -precalcValbufSize 4096 -precalcdxBufSize 4096 -w '+str(pos_width)+' -h '+str(pos_high))
    os.system('.\\bin\\opencv_traincascade.exe -data dt -vec pos.vec -bg neg.txt -numPos '+str(pos_real_num)+' -numNeg '+str(pos_real_num)+' -numStages 15 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -weightTrimRate 0.95 -maxDepth 1 -mode ALL -precalcValbufSize 4096 -precalcdxBufSize 4096 -featureType LBP -w '+str(pos_width)+' -h '+str(pos_high))
    
    print ('done all')
    input('press any key to continue:')
