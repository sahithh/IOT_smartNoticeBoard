from flask import Flask, flash, redirect, render_template, request, session, abort
import lcddriver
import time
import threading
import multiprocessing
app = Flask(__name__)
queue = []
flag=True
#This is used to display the message on to the LCD
def sync(msg):
    display = lcddriver.lcd()
    try:
        flag=False
        display.lcd_display_string(msg,1)
        time.sleep(5)
        display.lcd_clear()
        flag=True
    except KeyboardInterrupt:
        print("Cleaning up!")
        display.lcd_clear()
        
class msgdisplay:
    
    #This function is used to append given messages to queue     
    def append(self,msg):
        session['lcd'] = True  
        queue.append(msg) 
        print(queue)
    #This function is used to remove the selected message by user from queue   
    def delete(self,q):
        for i in q:
            queue.remove(i)
    #Synchronisation of messages are done by this function         
    def display(self):    
        i=0
        print(i)
        while i<len(queue):
            t1=threading.Thread(target=sync, args=(queue[i],))
            if  not t1.is_alive():
                print("active threads:",threading.active_count())
                print("current threads:",threading.current_thread())
                t1.start()
                t1.join()
                i=i+1
                print("second:",i)
                
                print("thread status:",t1.is_alive())
        i=0
        print("third:",i)
        

          


