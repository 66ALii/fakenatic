from asyncio.windows_events import NULL
from pickle import TRUE
from time import time
from MySQLdb import Timestamp
from datetime import datetime,date
import pyttsx3,docx2txt,os,numpy
from flask import Flask,render_template,request,flash,redirect,url_for
from flask_mysqldb import MySQL
from sqlalchemy import null
from werkzeug.security import generate_password_hash, check_password_hash
from moviepy.editor import *
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files (x86)\\ImageMagick-7.1.0-Q16\\magick.exe"})	
""" here at line 13 you need to give the path to imagemagick.exe file which you get after installing imagemagick 7.1.0 """

app= Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'    
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'fakenatic'
mysql = MySQL(app)
userlogin="False"
adminlogin="False"
p_data=""
org_data=""
cmp_account=""
cmp_org=""
all=""



@app.route('/')
def homepage():
   return render_template('index.html')

@app.route('/lets_create_it',methods=['POST','GET'])
def lets_create_it():
    if request.method=='POST':
        if userlogin=="True":
            #file inputs
            file=request.files['file-input']
            text=request.form['text-input']
            gender = request.form['voices']
            
            for row in p_data:
                u_id=row[0]
                u_name=row[1]

            #current date
            current_datetime=date.today()

            #primary key
            primarykey=null             
            audioname=null
            videoname=null
            a=[]
            cursor = mysql.connection.cursor()
            cursor.execute(''' SELECT * FROM video_catalog WHERE user_id= (%s) ''',[u_id])
            videocatalog_ids=cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            length=len(videocatalog_ids)
            
            if length==0:
                num=1
                primarykey=u_id+"_"+str(num)
                audioname=u_id+"_aud"+str(num)+".mp3"
                videoname=u_id+"_vid"+str(num)+".mp4"
            elif length!=0:
               for i in videocatalog_ids:
                    pk=i[0]
                    npk=pk.find("_",2)
                    npk+=1
                    a.append(int(pk[npk:]))
               max = numpy.amax(a)                  
               max=max+1
               primarykey=u_id+"_"+str(max)
               audioname=u_id+"_aud"+str(max)+".mp3"
               videoname=u_id+"_vid"+str(max)+".mp4" 

            if (len(text)==0 or len(text)==1) and file.filename=='' :
                flash("NO INPUT FOUND")
                return render_template('lets_create_it.html')
            
            elif (len(text)==0 or len(text)==1) and file.filename!='':
                

                #file path
                filepath="static/main"
                         
                path=os.path.join(filepath,u_id)
                s="/script"
                s_path=path+s
                s_path=os.path.join(s_path,file.filename)
                file.save(s_path)
                
                #video path
                v="/video"
                v_path=path+v+"/"+videoname

                #audio path
                a="/audio"                
                a_path=path+a+"/"+audioname 
                
                #storing the data in the database
                cursor = mysql.connection.cursor()
                cursor.execute(''' INSERT INTO video_catalog (video_id,user_id,video_url,audio_url,script_url,created_on,created_by) VALUES(%s,%s,%s,%s,%s,%s,%s)''',(primarykey,u_id,v_path,a_path,s_path,current_datetime,u_name))
                mysql.connection.commit()
                cursor.close()

                #text to speech

                r = docx2txt.process(file)
                result=r.replace("\n","")
                result=result.replace(".","   ")
                result=result.replace(",","   ")
                video_generation(gender,result,a_path,v_path)
                return render_template('lets_create_it.html')

            elif (len(text)!=0 or len(text)!=1) and file.filename=='':
                res = len(text.split())
                if res<=1000:
                  #new line check
                  print(text)
                  print("")
                  text=text.replace("\n"," ")
                  print(text)
                  t= text.replace(",","   ")
                  t= t.replace(".","   ")
                  #audio path
                  filepath="static/main"
                  path=os.path.join(filepath,u_id)  
                  a="/audio"
                  a_path=path+a+"/"+audioname

                  #video path
                  v="/video"
                  v_path=path+v+"/"+videoname

                  #storing data in database             
                  cursor = mysql.connection.cursor()
                  cursor.execute(''' INSERT INTO video_catalog (video_id,user_id,video_url,audio_url,created_on,created_by) VALUES(%s,%s,%s,%s,%s,%s)''',(primarykey,u_id,v_path,a_path,current_datetime,u_name))
                  mysql.connection.commit()
                  cursor.close()
                  
                  #text to speech
                  video_generation(gender,t,a_path,v_path)
                  return render_template('lets_create_it.html')

                else:
                  flash("TEXT SIZE EXCEEDS THE GIVEN WORD LIMIT")  
                  return render_template('lets_create_it.html')  

            elif (len(text)!=0 or len(text)!=1) and file.filename!='':
                flash("BOTH INPUTS CAN'T BE SENT TOGEHTER")
                return render_template('lets_create_it.html')                
        else:
            flash("PLEASE LOGIN FIRST")
            return render_template('lets_create_it.html')    

    else:
        return render_template('lets_create_it.html')    


def video_generation(gender,User_input,a_path,v_path):

    text=User_input
    voice_dict = {'Male': 0, 'Female': 1}
    code = voice_dict[gender]
    engine = pyttsx3.init()
    engine.setProperty('rate', 50)
    engine.setProperty('volume', 0.8)    
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[code].id)
    engine.say(User_input)
    engine.save_to_file(User_input,a_path)
    engine.runAndWait()    
    
    Phonems_Extracted=[]
    User_input = User_input.casefold()
    #extracting phonemes
    i = 0
    size = len(list(User_input))
    while i < len(list(User_input)): 
        
        #1  three letters
        try:
            if (User_input[i]=="i" and User_input[i+1]=="g" and User_input[i+2]=="h"):
                b=User_input[i]+User_input[i+1]+User_input[i+2]
                Phonems_Extracted.append(b)
                i+=3
                continue
            elif (User_input[i]=="e" and User_input[i+1]=="e" and User_input[i+2]=="r") or (User_input[i]=="e" and User_input[i+1]=="a" and User_input[i+1]=="r"):
                b=User_input[i]+User_input[i+1]+User_input[i+2]
                Phonems_Extracted.append(b)
                i+=3 
                continue
            elif (User_input[i]=="a" and User_input[i+1]=="i" and User_input[i+2]=="r") or (User_input[i]=="e" and User_input[i+1]=="r" and User_input[i+1]=="e"):
                b=User_input[i]+User_input[i+1]+User_input[i+2]
                Phonems_Extracted.append(b)
                i+=3 
                continue
            elif (User_input[i]=="o" and User_input[i+1]=="u" and User_input[i+2]=="r"):
                b=User_input[i]+User_input[i+1]+User_input[i+2]
                Phonems_Extracted.append(b)
                i+=3
                continue
        except IndexError:
            if i != size-1:
                Phonems_Extracted.append(User_input[i-1])
                i+=1
            
        #2    two letters
        try:

            if (User_input[i]=="a" and User_input[i+1]=="i") or (User_input[i]=="a" and User_input[i+1]=="y"):
                b=User_input[i]+User_input[i+1]
                Phonems_Extracted.append(b)
                i+=2
                continue          
            elif (User_input[i]=="e" and User_input[i+1]=="e") or (User_input[i]=="e" and User_input[i+1]=="a"):
                b=User_input[i]+User_input[i+1]
                Phonems_Extracted.append(b)
                i+=2 
                continue
            elif (User_input[i]=="i" and User_input[i+1]=="e"):
                b=User_input[i]+User_input[i+1]
                Phonems_Extracted.append(b)
                i+=2
                continue
            elif (User_input[i]=="o" and User_input[i+1]=="e") or (User_input[i]=="o" and User_input[i+1]=="w"):
                b=User_input[i]+User_input[i+1]
                Phonems_Extracted.append(b)
                i+=2
                continue
            elif (User_input[i]=="o" and User_input[i+1]=="o") or (User_input[i]=="u" and User_input[i+1]=="e"):
                b=User_input[i]+User_input[i+1]
                Phonems_Extracted.append(b)
                i+=2
                continue          
            elif (User_input[i]=="a" and User_input[i+1]=="r"):
                b=User_input[i]+User_input[i+1]
                Phonems_Extracted.append(b)
                i+=2
                continue
            elif (User_input[i]=="e" and User_input[i+1]=="r") or (User_input[i]=="i" and User_input[i+1]=="r") or (User_input[i]=="u" and User_input[i+1]=="r"):
                b=User_input[i]+User_input[i+1]
                Phonems_Extracted.append(b)
                i+=2
                continue
            elif (User_input[i]=="o" and User_input[i+1]=="r"):
                b=User_input[i]+User_input[i+1]
                Phonems_Extracted.append(b)
                i+=2    
                continue
            elif (User_input[i]=="o" and User_input[i+1]=="w") or (User_input[i]=="o" and User_input[i+1]=="u"):
                b=User_input[i]+User_input[i+1]
                Phonems_Extracted.append(b)
                i+=2
                continue
            elif (User_input[i]=="o" and User_input[i+1]=="y") or (User_input[i]=="o" and User_input[i+1]=="i"):
                b=User_input[i]+User_input[i+1]
                Phonems_Extracted.append(b)
                i+=2
                continue
            elif (User_input[i]=="n" and User_input[i+1]=="g"):
                b=User_input[i]+User_input[i+1]
                Phonems_Extracted.append(b)
                i+=2
                continue
            elif (User_input[i]=="t" and User_input[i+1]=="h"):
                b=User_input[i]+User_input[i+1]
                Phonems_Extracted.append(b)
                i+=2
                continue
            elif (User_input[i]=="s" and User_input[i+1]=="h"):
                b=User_input[i]+User_input[i+1]
                Phonems_Extracted.append(b)
                i+=2
                continue
            elif (User_input[i]=="g" and User_input[i+1]=="e"):
                b=User_input[i]+User_input[i+1]
                Phonems_Extracted.append(b)
                i+=2
                continue
            elif (User_input[i]=="c" and User_input[i+1]=="h"):
                b=User_input[i]+User_input[i+1]
                Phonems_Extracted.append(b)
                i+=2
                continue
        except IndexError:
            if i == size-1:
                Phonems_Extracted.append(User_input[i])
                i+=1
                

        #4  one letters
        try:      
            if User_input[i]== " ":
                Phonems_Extracted.append(User_input[i])
                i+=1 
                continue
            elif User_input[i]=="a":
                Phonems_Extracted.append(User_input[i])
                i+=1    
                continue
            elif User_input[i]=="e":
                Phonems_Extracted.append(User_input[i])  
                i+=1  
                continue
            elif User_input[i]=="i":
                Phonems_Extracted.append(User_input[i]) 
                i+=1   
                continue
            elif User_input[i]=="o":
                Phonems_Extracted.append(User_input[i]) 
                i+=1    
                continue
            elif User_input[i]=="u":
                Phonems_Extracted.append(User_input[i]) 
                i+=1    
                continue
            elif User_input[i]=="p":
                Phonems_Extracted.append(User_input[i])
                i+=1    
                continue 
            elif User_input[i]=="b":
                Phonems_Extracted.append(User_input[i]) 
                i+=1    
                continue
            elif User_input[i]=="t":
                Phonems_Extracted.append(User_input[i]) 
                i+=1    
                continue
            elif User_input[i]=="d":
                Phonems_Extracted.append(User_input[i])
                i+=1    
                continue 
            elif User_input[i]=="k" or User_input[i]=="c":
                Phonems_Extracted.append(User_input[i])    
                i+=1 
                continue
            elif User_input[i]=="g":    
                Phonems_Extracted.append(User_input[i])    
                i+=1 
                continue
            elif User_input[i]=="m":
                Phonems_Extracted.append(User_input[i])    
                i+=1 
                continue
            elif User_input[i]=="n":
                Phonems_Extracted.append(User_input[i])    
                i+=1 
                continue
            elif User_input[i]=="f":
                Phonems_Extracted.append(User_input[i])    
                i+=1 
                continue
            elif User_input[i]=="v":
                Phonems_Extracted.append(User_input[i])    
                i+=1 
                continue
            elif User_input[i]=="s":
                Phonems_Extracted.append(User_input[i])    
                i+=1 
                continue
            elif User_input[i]=="z":
                Phonems_Extracted.append(User_input[i])    
                i+=1 
                continue
            elif User_input[i]=="h":
                Phonems_Extracted.append(User_input[i])    
                i+=1 
                continue
            elif User_input[i]=="j":
                Phonems_Extracted.append(User_input[i])    
                i+=1 
                continue
            elif User_input[i]=="w":
                Phonems_Extracted.append(User_input[i])    
                i+=1 
                continue
            elif User_input[i]=="r":
                Phonems_Extracted.append(User_input[i])    
                i+=1 
                continue
            elif User_input[i]=="y":
                Phonems_Extracted.append(User_input[i])    
                i+=1 
                continue
            elif User_input[i]=="l":
                Phonems_Extracted.append(User_input[i])
                i+=1 
                continue
            elif User_input[i]=="q":
                Phonems_Extracted.append(User_input[i])  
                i+=1 
                continue
            elif User_input[i]=="x":
                Phonems_Extracted.append(User_input[i]) 
                i+=1  
                continue

            elif User_input[i]=="." or User_input[i]==",":
                Phonems_Extracted.append(User_input[i]) 
                i+=1  
                continue
            
            elif User_input[i]=="/" or User_input[i]=="-"   :
                i+=1   
                continue
            else :
                i=i+1
                continue
        except IndexError:
            i+=1
    '''Print Phonems'''
    print(Phonems_Extracted)      

    #comparing phonemes and video concatenation
    j=1
    if gender=="Male":
        if Phonems_Extracted[0]==" ":
            pth="/space bar"
        else:
            pth="/"+Phonems_Extracted[0]    
        path="visemes/male visemes"
        
        path=path+pth+".mp4"
        final_clip=VideoFileClip(path)
        
        while j<len(Phonems_Extracted):
            #three letters
            if (Phonems_Extracted[j]=="igh"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/igh.mp4')])
            elif (Phonems_Extracted[j]=="eer") or (Phonems_Extracted[j]=="ear"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/eer,ear.mp4')])
            elif (Phonems_Extracted[j]=="air") or (Phonems_Extracted[j]=="ere"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/air,ere.mp4')])
            elif (Phonems_Extracted[j]=="our"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/our.mp4')])


            #two letter
            elif (Phonems_Extracted[j]=="ai") or (Phonems_Extracted[j]=="ay"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/ai,ay.mp4')])
            elif (Phonems_Extracted[j]=="ee") or (Phonems_Extracted[j]=="ea"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/ee,ea.mp4')])
            elif (Phonems_Extracted[j]=="ie"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/ie.mp4')])
            elif (Phonems_Extracted[j]=="oe") or (Phonems_Extracted[j]=="ow"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/oe,ow.mp4')])
            elif (Phonems_Extracted[j]=="oo") or (Phonems_Extracted[j]=="ue"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/oo,ue.mp4')])
            elif (Phonems_Extracted[j]=="ar"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/ar.mp4')])
            elif (Phonems_Extracted[j]=="er") or (Phonems_Extracted[j]=="ir") or (Phonems_Extracted[j]=="ur"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/er,ir,ur.mp4')])
            elif (Phonems_Extracted[j]=="or"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/or.mp4')])
            elif (Phonems_Extracted[j]=="ow") or (Phonems_Extracted[j]=="ou"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/ow,ou.mp4')])
            elif (Phonems_Extracted[j]=="oy") or (Phonems_Extracted[j]=="oi"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/oy,oi.mp4')])
            elif (Phonems_Extracted[j]=="ng"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/ng.mp4')])
            elif (Phonems_Extracted[j]=="th"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/th.mp4')])
            elif (Phonems_Extracted[j]=="sh"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/sh.mp4')])
            elif (Phonems_Extracted[j]=="ge"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/ge.mp4')])
            elif (Phonems_Extracted[j]=="ch"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/ch.mp4')])
        
            #one letter
            elif Phonems_Extracted[j]== " ":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/space bar.mp4')])
            elif Phonems_Extracted[j]=="a":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/a.mp4')])
            elif Phonems_Extracted[j]=="e":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/e.mp4')])
            elif Phonems_Extracted[j]=="i":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/i.mp4')])
            elif Phonems_Extracted[j]=="o":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/o.mp4')]) 
            elif Phonems_Extracted[j]=="u":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/u.mp4')])
            elif Phonems_Extracted[j]=="p":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/p.mp4')])
            elif Phonems_Extracted[j]=="b":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/b.mp4')])
            elif Phonems_Extracted[j]=="t":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/t.mp4')])
            elif Phonems_Extracted[j]=="d":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/d.mp4')])
            elif Phonems_Extracted[j]=="k" or Phonems_Extracted[j]=="c":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/k,c.mp4')])
            elif Phonems_Extracted[j]=="g":    
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/g.mp4')])
            elif Phonems_Extracted[j]=="m":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/m.mp4')])
            elif Phonems_Extracted[j]=="n":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/n.mp4')])
            elif Phonems_Extracted[j]=="f":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/f.mp4')])
            elif Phonems_Extracted[j]=="v":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/v.mp4')])
            elif Phonems_Extracted[j]=="s":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/s.mp4')])
            elif Phonems_Extracted[j]=="z":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/z.mp4')])
            elif Phonems_Extracted[j]=="h":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/h.mp4')])
            elif Phonems_Extracted[j]=="j":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/j.mp4')])
            elif Phonems_Extracted[j]=="w":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/w.mp4')])
            elif Phonems_Extracted[j]=="r":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/r.mp4')])
            elif Phonems_Extracted[j]=="y":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/y.mp4')])
            elif Phonems_Extracted[j]=="l":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/l.mp4')])
            elif Phonems_Extracted[j]=="q":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/q.mp4')]) 
            elif Phonems_Extracted[j]=="x":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/x.mp4')])
            elif Phonems_Extracted[j]=="." or Phonems_Extracted[j]==",":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/male visemes/fullstop,comma.mp4')])   
            j+=1
    
    elif gender=="Female":
        if Phonems_Extracted[0]==" ":
            pth="/space bar"
        else:
            pth="/"+Phonems_Extracted[0]    
        path="visemes/female visemes"
        path=path+pth+".mp4"
        final_clip=VideoFileClip(path)
        
        while j<len(Phonems_Extracted):
            #three letters
            if (Phonems_Extracted[j]=="igh"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/igh.mp4')])
            elif (Phonems_Extracted[j]=="eer") or (Phonems_Extracted[j]=="ear"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/eer,ear.mp4')])
            elif (Phonems_Extracted[j]=="air") or (Phonems_Extracted[j]=="ere"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/air,ere.mp4')])
            elif (Phonems_Extracted[j]=="our"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/our.mp4')])


            #two letter
            elif (Phonems_Extracted[j]=="ai") or (Phonems_Extracted[j]=="ay"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/ai,ay.mp4')])
            elif (Phonems_Extracted[j]=="ee") or (Phonems_Extracted[j]=="ea"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/ee,ea.mp4')])
            elif (Phonems_Extracted[j]=="ie"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/ie.mp4')])
            elif (Phonems_Extracted[j]=="oe") or (Phonems_Extracted[j]=="ow"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/oe,ow.mp4')])
            elif (Phonems_Extracted[j]=="oo") or (Phonems_Extracted[j]=="ue"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/oo,ue.mp4')])
            elif (Phonems_Extracted[j]=="ar"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/ar.mp4')])
            elif (Phonems_Extracted[j]=="er") or (Phonems_Extracted[j]=="ir") or (Phonems_Extracted[j]=="ur"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/er,ir,ur.mp4')])
            elif (Phonems_Extracted[j]=="or"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/or.mp4')])
            elif (Phonems_Extracted[j]=="ow") or (Phonems_Extracted[j]=="ou"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/ow,ou.mp4')])
            elif (Phonems_Extracted[j]=="oy") or (Phonems_Extracted[j]=="oi"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/oy,oi.mp4')])
            elif (Phonems_Extracted[j]=="ng"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/ng.mp4')])
            elif (Phonems_Extracted[j]=="th"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/th.mp4')])
            elif (Phonems_Extracted[j]=="sh"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/sh.mp4')])
            elif (Phonems_Extracted[j]=="ge"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/ge.mp4')])
            elif (Phonems_Extracted[j]=="ch"):
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/ch.mp4')])
        
            #one letter
            elif Phonems_Extracted[j]== " ":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/space bar.mp4')])
            elif Phonems_Extracted[j]=="a":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/a.mp4')])
            elif Phonems_Extracted[j]=="e":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/e.mp4')])
            elif Phonems_Extracted[j]=="i":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/i.mp4')])
            elif Phonems_Extracted[j]=="o":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/o.mp4')]) 
            elif Phonems_Extracted[j]=="u":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/u.mp4')])
            elif Phonems_Extracted[j]=="p":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/p.mp4')])
            elif Phonems_Extracted[j]=="b":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/b.mp4')])
            elif Phonems_Extracted[j]=="t":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/t.mp4')])
            elif Phonems_Extracted[j]=="d":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/d.mp4')])
            elif Phonems_Extracted[j]=="k" or Phonems_Extracted[j]=="c":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/k,c.mp4')])
            elif Phonems_Extracted[j]=="g":    
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/g.mp4')])
            elif Phonems_Extracted[j]=="m":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/m.mp4')])
            elif Phonems_Extracted[j]=="n":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/n.mp4')])
            elif Phonems_Extracted[j]=="f":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/f.mp4')])
            elif Phonems_Extracted[j]=="v":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/v.mp4')])
            elif Phonems_Extracted[j]=="s":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/s.mp4')])
            elif Phonems_Extracted[j]=="z":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/z.mp4')])
            elif Phonems_Extracted[j]=="h":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/h.mp4')])
            elif Phonems_Extracted[j]=="j":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/j.mp4')])
            elif Phonems_Extracted[j]=="w":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/w.mp4')])
            elif Phonems_Extracted[j]=="r":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/r.mp4')])
            elif Phonems_Extracted[j]=="y":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/y.mp4')])
            elif Phonems_Extracted[j]=="l":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/l.mp4')])
            elif Phonems_Extracted[j]=="q":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/q.mp4')]) 
            elif Phonems_Extracted[j]=="x":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/x.mp4')])
            elif Phonems_Extracted[j]=="." or Phonems_Extracted[j]==",":
                final_clip=concatenate_videoclips([final_clip,VideoFileClip('visemes/female visemes/fullstop,comma.mp4')])   
                
            j+=1






    
    audioclip = AudioFileClip(a_path)
    new_audioclip = CompositeAudioClip([audioclip])
    final_clip.audio = new_audioclip
    final_clip=final_clip.fx(vfx.speedx,1.2)
    #final_clip.write_videofile(v_path)

    text=text.split()
    w=[]

    #placing text on video
    l = 0
    size = len(list(text))
    while l <= len(list(text)): 
            
            try:
                
                    b=text[l]+" "+text[l+1]+" "+text[l+2]+" "+text[l+3]
                    w.append(b)
                    l+=4
                    continue
            
            except IndexError:
                if l != size:
                    if size-l==3:
                        b=text[l]+" "+text[l+1]+" "+text[l+2]
                        w.append(b)
                        l+=3
                    elif size-l==2:
                        b=text[l]+" "+text[l+1]
                        w.append(b)
                        l+=2
                    elif size-l==1:
                        b=text[l]
                        w.append(b)
                        l+=1     
                
            l=l+2       
            

    print(w)
    t_clip = final_clip
    print(t_clip.duration/len(w))
    i=0
    t=0
    t1=t
    t2=0

    while i<len(w):
            t2=t2+(t_clip.duration/len(w))
            txt_clip = TextClip(w[i], fontsize = 60, color = 'white',bg_color="black")
            txt_clip = txt_clip.set_pos('bottom').set_start(t1).set_end(t2)
            t_clip = CompositeVideoClip([t_clip, txt_clip])
            #t2=t2+(t_clip.duration/len(w))
            t1=t2
            i=i+1
    
    t_clip.write_videofile(v_path)




@app.route('/how_it_works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/plans')    
def plans():
    return render_template('plans.html')

@app.route('/accounts', methods=['POST','GET'])
def accounts():
    global userlogin,adminlogin,p_data,org_data,cmp_account,cmp_org,all
    try:
        if request.method=='POST':
                L_email_name=request.form['email-name']
                L_passwd=request.form['pass']
                cursor = mysql.connection.cursor()
                
                """ cursor.execute(''' SELECT * FROM user ''')
                accounts=cursor.fetchall()
                mysql.connection.commit()
                cursor.close()
                
                orgid=""
                cmporg=()
                #returning complete data for admin page
                for rows in accounts:
                    orgid=rows[6]
                    cursor = mysql.connection.cursor()
                    cursor.execute(''' SELECT * FROM organization WHERE ORG_ID= (%s) ''',[orgid])
                    organization=cursor.fetchall()
                    mysql.connection.commit()
                    cursor.close()
                    cmporg=cmporg+organization """
 
                cursor = mysql.connection.cursor()
                cursor.execute(''' SELECT * FROM `user` s INNER join organization O on O.ORG_ID = s.ORG_ID  ''' )
                all=cursor.fetchall()
                mysql.connection.commit()
                cursor.close()


                #returning single user data which has logged in
                cursor = mysql.connection.cursor()
                cursor.execute(''' SELECT * FROM user where U_EMAIL=(%s) or U_NAME=(%s) ''',(L_email_name,L_email_name))
                account=cursor.fetchall()
                mysql.connection.commit()
                cursor.close()
                loginemail=""
                loginusername=""
                loginpass=""
                for row in account:
                    loginusername=row[1]
                    loginemail=row[3]
                    loginpass=row[5]
                    orgid=row[6]
                    cursor = mysql.connection.cursor()
                    cursor.execute(''' SELECT * FROM organization where ORG_ID=(%s)''',[orgid])
                    org_row=cursor.fetchall()
                    mysql.connection.commit()
                    cursor.close()

                #password encrypt hokr db kay password say match hoga ya to db ka password encrypt hoga aur input walay say match hoga
                
                if loginemail==L_email_name and check_password_hash(loginpass, L_passwd) and userlogin=="False" :
                    p_data=account 
                    org_data=org_row  
                    userlogin="True"
                    return render_template('userdetails.html',account=account,org_rows=org_row)
                elif loginusername==L_email_name and check_password_hash(loginpass, L_passwd) and userlogin=="False" :
                    p_data=account 
                    org_data=org_row  
                    userlogin="True"
                    return render_template('userdetails.html',account=account,org_rows=org_row)

                elif L_email_name=='admin' and L_passwd=='admin' and adminlogin=="False" :
                    adminlogin="True"
                    """ cmp_account=accounts
                    cmp_org=cmporg """
                    return render_template('admin.html',all=all)
                    #return render_template('admin.html',accounts=accounts,cmporgs=cmporg,all=all)
      
                else: 
                    return render_template('accounts.html')

                    

                                      
        else:
            if userlogin=="True":
                return render_template('userdetails.html',account=p_data,org_rows=org_data)
            elif adminlogin=="True":
                return render_template('admin.html',all=all)
                """return render_template('admin.html',accounts=cmp_account,cmporgs=cmp_org) """
            else:         
                return render_template('accounts.html')

    except  Exception as e:
        print(e)
        return e

@app.route('/signup',methods=['POST', 'GET'])
def signup():
    try:
        if request.method=='POST':
                usernanme=request.form['u-name']
                fullnanme=request.form['full-name']
                email=request.form['Email']
                contact=request.form['contact']
                S_passwd=request.form['pass']
                role=request.form['role']
                org_name=request.form['org-name']
                org_contact=request.form['org-contact']
                org_email=request.form['org-email']
                org_location=request.form['org-location']
                u_id="U_"+usernanme
                a=org_email.find("@")
                org_id="ORG_"+org_email[0:a]
                S_password=generate_password_hash(S_passwd, method='sha256')
                cursor = mysql.connection.cursor() 
                cursor.execute(''' SELECT * FROM organization ''')
                organization=cursor.fetchall()
                mysql.connection.commit()
                cursor.close()
                cursor = mysql.connection.cursor()
                cursor.execute(''' SELECT * FROM user ''')
                users=cursor.fetchall()
                mysql.connection.commit()
                cursor.close()
                
                for row in users:
                        dbusername=row[1]
                        dbuseremail=row[3]
                        if usernanme==dbusername:
                            flash("USER NAME ALREADY REGISTERED")
                            return render_template('signup.html')
                        elif email==dbuseremail:
                            flash("USER ALREADY EXIST")
                            return render_template('signup.html')
                
                for i in organization:
                    organizationid=i[0]
                    organizationname=i[1]
                    if org_name==organizationname:
                        cursor = mysql.connection.cursor()
                        cursor.execute(''' INSERT INTO user VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''',(u_id,usernanme,fullnanme,email,contact,S_password,organizationid,role))
                        mysql.connection.commit()
                        cursor.close()
                        
                        directory = u_id  
                        parent_dir = "static/main"
        
                        path = os.path.join(parent_dir, directory)
                        os.mkdir(path)
                 
                        directory_script="script"
                        path1=os.path.join(path,directory_script)
                        os.mkdir(path1)

                        directory_audio="audio"
                        path2=os.path.join(path,directory_audio)
                        os.mkdir(path2)

                        directory_video="video"
                        path3=os.path.join(path,directory_video)
                        os.mkdir(path3)

                        print("similar organization exist in database, test")
                        return redirect("/accounts") 
                    elif org_name!=organizationname:
                        continue   
                    
                cursor = mysql.connection.cursor()
                cursor.execute(''' INSERT INTO user VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''',(u_id,usernanme,fullnanme,email,contact,S_password,org_id,role))
                mysql.connection.commit()
                cursor.close()  
                cursor = mysql.connection.cursor()
                cursor.execute(''' INSERT INTO organization VALUES(%s,%s,%s,%s,%s)''',(org_id,org_name,org_contact,org_email,org_location))
                mysql.connection.commit()
                cursor.close()
                directory = u_id  
                parent_dir = "static/main"
                path = os.path.join(parent_dir, directory)
                os.mkdir(path)

                directory_script="script"
                path1=os.path.join(path,directory_script)
                os.mkdir(path1)

                directory_audio="audio"
                path2=os.path.join(path,directory_audio)
                os.mkdir(path2)

                directory_video="video"
                path3=os.path.join(path,directory_video)
                os.mkdir(path3)        

                #print("diffrent organization found")
                return redirect("/accounts") 
                 
        else:
                return render_template('signup.html')
    except Exception as e:
        return e            

@app.route('/forgotpass',methods=['POST', 'GET'])
def forgotpass():
    try:
        if request.method=='POST':
            F_email=request.form['email']
            F_passwd=request.form['pass']
            cursor = mysql.connection.cursor()
            cursor.execute(''' SELECT * FROM user where U_EMAIL=(%s) ''',[F_email])
            account=cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            print(F_passwd)
            F_password=generate_password_hash(F_passwd, method='sha256')
            print(F_password)

            for row in account:
                    forgotemail=row[3]
            
                    if forgotemail==F_email:
                        cursor = mysql.connection.cursor()
                        cursor.execute(''' UPDATE user SET U_PASSWD = (%s) WHERE U_EMAIL = (%s)''',(F_password,F_email))
                        mysql.connection.commit()
                        cursor.close()  
                        return redirect(url_for('accounts'))
            
            return render_template('forgotpass.html')    
        else:
            return render_template('forgotpass.html')
    except  Exception as e:
        return e

@app.route('/logout')    
def logout():
        global userlogin,adminlogin
        if userlogin=="True" : 
            userlogin="False"
            return redirect(url_for('accounts'))
        elif adminlogin=="True" :
            adminlogin="False" 
            return redirect(url_for('accounts'))

@app.route('/user_catalog')
def user_catalog():
    nlinks=[]
    for row in p_data:
        u_id=row[0]
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT video_url FROM video_catalog where user_id=(%s) ''',[u_id])
    videoslinks=cursor.fetchall()
    mysql.connection.commit()
    cursor.close()    

    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT video_url,created_on,created_by FROM `video_catalog` WHERE user_id=(%s); ''',[u_id])
    data=cursor.fetchall()
    mysql.connection.commit()
    cursor.close()    
    names=[]
    for row in data:
        i=row[0].index("video/")
        i=i+6
        names.append(row[0][i:-4])
        
    


    links=list(videoslinks)
    for i in links:
        i= ''.join(i)
        i=i.replace("\\","/")
        a=i.index("static")
        b=i[a:-1]
        b=b+"4"
        nlinks.append(b)
    nlinks=list(nlinks)
    return render_template('user_catalog.html',nlinks=nlinks,packed=zip(nlinks,data,names))

@app.route('/admin_catalog')
def admin_catalog():
    x = request.query_string
    x=str(x)
    a=x.find("=")
    a=a+1
    b=x[a:-1]
   
    #database query
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT video_url FROM video_catalog where user_id=(%s) ''',[b])
    videoslinks=cursor.fetchall()
    mysql.connection.commit()
    cursor.close()    
    



    #data
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT video_url,created_on,created_by FROM video_catalog where user_id=(%s) ''',[b])
    data=cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    data=list(data)
    
    names=[]
    for row in data:
        i=row[0].index("video/")
        i=i+6
        names.append(row[0][i:-4])
    #videos
    nlinks=[]
    links=list(videoslinks)
    for i in links:
        i= ''.join(i)
        i=i.replace("\\","/")
        a=i.index("static")
        b=i[a:-1]
        b=b+"4"
        nlinks.append(b)
    nlinks=list(nlinks)
   
    return render_template('admin_catalog.html',nlinks=nlinks,packed=zip(nlinks,data,names))

if __name__=="__main__":
    app.run(debug=True)
