import cv2
import numpy as np
from collections import Counter
import datetime

class detect:

    def __init__(self):
        self.net=cv2.dnn.readNet(r"E:\Real-Time-Object-Counting-main\Real-Time-Object-Counting-main\yolov3.weights",r"E:\Real-Time-Object-Counting-main\Real-Time-Object-Counting-main\yolov3.cfg")
        self.classes=[]
        with open('coco.names','r') as f:
            self.classes=f.read().splitlines()
        self.cap=cv2.VideoCapture(0)
        

    def countobject(self,whole_track_list,index_of_track):
        count=0
        for p in whole_track_list:
            if(p==index_of_track):
                count+=1
        return count

    def numOfsameIndex(self,whole_redundant_list,item_id):
        count1=0
        for q in whole_redundant_list:
            if(q==item_id):
                count1+=1
        return count1

    def videowrite(self,receivedsize,redundant,img,countlists):
        i=0
        x=20
        y=30
        while i<receivedsize:
            label=str(self.classes[redundant[i]])
            cv2.putText(img,label,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
            x+=180
            text=":{}".format(countlists[i])
            cv2.putText(img,text,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
            i+=1
            x=x-180
            y+=30

    def capture(self):
        ret,img=self.cap.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #print("ret value",ret)
        #print("frmae value",img)
        fps=self.cap.get(cv2.CAP_PROP_FPS)
        #print("fps:{}".format(fps))
        
        
        raw_height,raw_width, _ =img.shape
        blob=cv2.dnn.blobFromImage(img,1/255,(416,416),(0,0,0),swapRB=True,crop=False)
        self.net.setInput(blob)
        
        output_layers_names=self.net.getUnconnectedOutLayersNames()
        finaloutputs=self.net.forward(output_layers_names)

        boxes_no=[]
        confidences_score=[]
        class_ids=[]
        for outputs in finaloutputs:
            for detect in outputs:
                scores=detect[5:]
                class_id=np.argmax(scores)
                confidence=scores[class_id]
                if confidence > 0.7:
                    x_center=int(detect[0]*raw_width)
                    y_center=int(detect[1]*raw_height)
                    w=int(detect[2]*raw_width)
                    h=int(detect[3]*raw_height)
                
                    x=int(x_center-w/2)
                    y=int(y_center-h/2)
                    boxes_no.append([x,y,w,h])
                    confidences_score.append((float(confidence)))
                    class_ids.append(class_id)
            
        #print(len(boxes_no))   
        index=cv2.dnn.NMSBoxes(boxes_no,confidences_score,0.7,0.4)
        
        colors=np.random.uniform(0,255,size=(len(boxes_no),3))
        track=[]
        self.object_name = []
        

        if len(index)>0: 
            
            for l in index.flatten():
                
            
                x,y,w,h=boxes_no[l]
                label=str(self.classes[class_ids[l]])
                #print(class_ids[i])
                track.append(class_ids[l])
                self.object_name.append(self.classes[class_ids[l]])
                confidence=str(round(confidences_score[l],2))
                color=colors[l]
                cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
                cv2.putText(img,label+" "+confidence,(x,y+10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),1)
        

        #print("values in track list",self.object_name)


        #self.count_object_in_frame(object_name,parameter=0)
        
        
        redundant=[]
        countlists=[]
        size=len(track)


        i=0
        while i<size:
            
            redundantsize=len(redundant)
            if (redundantsize==0):  
                totalobject=self.countobject(track,track[i])
                #print("lenth of redundant array",redundantsize)
                #print("value",redundant)
                redundant.append(track[i])
                countlists.append(totalobject)
                i+=1
            
            else:
                rslt=self.numOfsameIndex(redundant,track[i])
            
                if(rslt==0):
                    totalobject=self.countobject(track,track[i])
                    #print("lenth of redundant array",redundantsize)
                # print("value",redundant)
                    redundant.append(track[i])
                    countlists.append(totalobject)
                    i+=1
                else:
                    i+=1

        loopsize=len(countlists)
        #print("loopsize",loopsize)
        self.videowrite(loopsize,redundant,img,countlists)    
        return img

    def time(self):
        self.current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def count_object_in_frame(self,parameter=0):
        self.time()
    
        if parameter == 1:
            result = dict(Counter(self.object_name))
            #print("Time: " + self.current_time)
            result_list = [{'object': key, 'count': value , 'time': self.current_time } for key, value in result.items()]
            print("test",result_list)
            parameter = 0
            return result_list