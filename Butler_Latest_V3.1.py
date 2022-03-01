from tkinter import *  
import tkinter as tk
import time as tm
import datetime
from tkcalendar import *
from configparser import ConfigParser
import requests
from tkinter import messagebox as ms
from PIL import ImageTk,Image
from functools import partial
import json
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import ttk
import os
import sqlite3
import csv
import math                                      
from collections import Counter
import random
today=datetime.date.today()           

    

def delete_pass(event):          #function implimented to remove entry boxes 
    event.widget.delete(0, END)

class FirstPage(tk.Frame):                    #implimentions : login, registration
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
       
        
        
        temp_login_name = StringVar()                            #taking in username and pass
        temp_login_password = StringVar()
        border = tk.LabelFrame(self, bg='black')
        border.place(x=500,y=500,width=400,height=200)
        passw = tk.Label(border, text="Password", font=("Arial Bold", 15), bg='ivory').place(x=50, y=80)  
        Usern = tk.Label(border, text="Username", font=("Arial Bold", 15), bg='ivory').place(x=50, y=30)
        entry= tk.Entry(border, width = 30, bd = 5,textvariable=temp_login_name)
        entry.place(x=180, y=30)
        entryy = tk.Entry(border, width = 30, show='*', bd = 5,textvariable=temp_login_password)        #Mask the pass with *
        entryy.place(x=180, y=80)
        login_name = temp_login_name.get()                 #get the username

        def login_session():       #credential varification 
            global login_name
            global login_password
            global password
            global current_balance
            
            
            all_accounts = os.listdir()               #access textfile with creds 
            login_password = temp_login_password.get()
            login_name = temp_login_name.get()
            
            

            for name in all_accounts:               #matching the input creds against the file creds
                if name == login_name:
                    file = open(name,"r")
                    file_data = file.read()
                    file_data = file_data.split('\n')
                    password  = file_data[1]
                   
                    if login_password == password:            #giving acceess and removing eneteries
                        controller.show_frame(SecondPage)
                        entryy.delete(0, END)
                        entry.delete(0, END) 
                        
                       
                        return 
                    else: 
                        notifwrong=Label(self,fg="red", text="Password incorrect!!").place(x=500, y=500)      #errors (did not match)
                        return
            Noacc=Label(self,fg="red", text="No account found !!").place(x=500, y=500)  
      
       

        





        loginb = tk.Button(self, text ="Login", bg="blue",font=("Times",14), command= login_session).place(x=600,y=650, width=100, height=40)     
        #self.bind('<Return>', pross)
        Register1= tk.Button(self, text ="Register", bg="blue",font=("Times",14),command=lambda: controller.show_frame(Registerpage)).place(x=740,y=650, width=100, height=40)
        
        
        def weather():         #weather implimentation
             
            try:
                api_request = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Tampere&appid=7b51f4cf5374c28d05c1b5c4bef001c1')  #API for eather JSON
                api = json.loads(api_request.content)     #load JSON and match the following into python 
                city=api['name']
                weather=api['weather'][0]['main']
                temp=api['main']['temp']
                temp_c=round(temp-273.5)
                tempertature = str(temp_c)
                icon=api['weather'][0]['icon']
                image1="icon/{}.png".format(icon)    #matching the Images against the weather type
                img=ImageTk.PhotoImage(Image.open(image1))
               

                
                
            except Exception as e:     #implimentation into GUI int the following format
                return None
            self.frame3 =tk.LabelFrame(self, text="City:"+str(city) + "\nWeather:\t" + str(weather)+ "\nTemperature:"+ str(tempertature) + " c", fg="white", bg="black",font=("Helvetica", 17),bd=0).place(x=300,y=100,width=400,height=100)  #title on the
            panel = Label(self, image=img, bg='black')
            panel.photo=img
            panel.place(x=500,y=100)
        weather()

        

class SecondPage(tk.Frame):       #Main page, access to all pages from here 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
    
       
        #Buttons to all pages 
        Logout=tk.Button(self, text="Logout", command=lambda: controller.show_frame(FirstPage)).place(x=790,y=200,width=110,height=25)
        addtrans=tk.Button(self, text="Add Transaction",command=lambda: controller.show_frame(ThirdPage)).place(x=790,y=230,width=110,height=25)
        Edit_account=tk.Button(self, text="Edit Account", command=lambda: controller.show_frame(FourthPage)).place(x=790,y=260,width=110,height=25)
        Setup=tk.Button(self, text="Setup",command=lambda: controller.show_frame(FifthPage)).place(x=790,y=290,width=110,height=25)
        Accounts=tk.Button(self, text="Account Summary", command=lambda: controller.show_frame(SixthPage)).place(x=790,y=320,width=110,height=25)
        lotto=tk.Button(self, text="Play Lotto", command=lambda: controller.show_frame(SeventhPage)).place(x=790,y=350,width=110,height=25)
       
     
            

        
            



        def valget():    #Getting the balance from textfile by BB button (refresh)
            file = open(login_name, 'r')
            file_data = file.read()
            user_details = file_data.split('\n')
            details_balance = user_details[3]
            money=Label(self,text="Current balance : €"+str(details_balance),font=("Times",14)).place(x=380,y=40,width=300,height=100)

        

        

        BB=tk.Button(self, text="Refresh balance", command=valget).place(x=460,y=200,width=110,height=25) 
      
      
            
        
     

     

        
        

        

class ThirdPage(tk.Frame):      #adding transactions (income, expense) by cathegory, amount and date 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global cal
        global current_balance
        global money
        global withdraw_amount
        amount = StringVar() #getting amount, categroy and the withdrawn amount 
        category = StringVar()
        withdraw_amount = StringVar()   
        Lab1=Label(self,text="Category",bg='white',font=("times",15)).place(x=500,y=150)
        Lab2=Label(self,text="Amount",bg='white',font=("times",15)).place(x=500,y=200)
        #Lab3=Label(self,text="Date",bg='white',font=("times",15)).place(x=500,y=250)

      
        category1 = Entry(self, width = 30, bd = 4,textvariable=category)
        category1.place(x=600, y=150)
        amount1 = Entry(self,width = 30, bd = 4,textvariable=amount)
        amount1.place(x=600, y=200)
       

        
        
        return1=Button(self,text="Return",command=lambda: controller.show_frame(SecondPage)).place(width=100,height=30,x=780,y=650)
       
        

    
        
        def finish():      #Function for income (positive) transactions 
            global updated_balance
        
            
            if amount.get() =="" :                          #safety if satatement incase of bad or empty entry
                Label(self,text='Amount is required!',fg="red").place(x=200,y=200)
                return
            if float(amount.get()) <=0:
                Label(self,text='Negative currency is not accepted', fg='red').place(x=200,y=200)
                return
            else:                                #updating the balance by adding the amount to the current balance 
                file = open(login_name, 'r+')
                file_data = file.read()
                details = file_data.split('\n')
                current_balance = details[3]
                
                updated_balance = current_balance
                updated_balance = float(updated_balance) + float(amount.get())
                file_data       = file_data.replace(current_balance, str(updated_balance))
                file.seek(0)
                file.truncate(0)
                file.write(file_data)
                file.close()
                
                thedate=mydate.get_date()               #category, amount and date taken in from user into csv 
                thiscat=(category.get())              
                thisamount=float((amount.get()))
                with open(login_name+'.csv', 'a') as file1:
                    myFile= csv.writer(file1)
                    #myFile.writerow(["Money","category","amount","date"])
                    myFile.writerow([updated_balance,thiscat,thisamount,thedate])
                    file1.close()

                
      
                with open(login_name+'i'+'.csv', "a") as file2:            #getting the amount info to the csv file (of the same user )
                    myFile2= csv.writer(file2)
                    myFile2.writerow([thisamount])
                    file2.close()

                
               
            Label(self,text='Balance Updated', fg='green').place(x=500, y=400)                 #displace of updated balance + entery removing
            money=Label(self,text="Current balance : €"+str(updated_balance),font=("Times",14)).place(x=380,y=40,width=300,height=100)
            amount1.delete(0, END)
            category1.delete(0,END)
            
            
    

            
  
  
        def finish_withdraw():    #same as finish but for expense 
            if amount.get() == "":
                Label(self,text='Amount is required!',fg="red")
                return
            if float(amount.get()) <=0:
                Label(self,text='Negative currency is not accepted', fg='red')
                return
        
            file = open(login_name, 'r+')
            file_data = file.read()
            details = file_data.split('\n')
            current_balance = details[3]
        
            if float(amount.get()) >float(current_balance):
                Label(self,text='Insufficient Funds!', fg='red').place(x=600,y=250)
                return
            #the amount is subtracted, the rest of the operatiosn are the same 
            updated_balance = current_balance
            updated_balance = float(updated_balance) - float(amount.get())
            file_data       = file_data.replace(current_balance, str(updated_balance))
            file.seek(0)
            file.truncate(0)
            file.write(file_data)
            file.close()
            thisdate=mydate.get_date()
            thiscat=(category.get())
            thisamount=(-float(amount.get()))
            thisamount3=(float(amount.get()))
            with open(login_name+'.csv', 'a') as file1:
                myFile= csv.writer(file1)
                #myFile.writerow(["Money","category","amount","date"])
                myFile.writerow([updated_balance,thiscat,thisamount,thisdate])
             

            with open(login_name+'e'+'.csv', "a") as file3:
                myFile3= csv.writer(file3)
                myFile3.writerow([thisamount3])
                file3.close()
         
            amount1.delete(0, END)
            category1.delete(0,END)
           

            

            Label(self,text='Balance Updated', fg='green').place(x=500,y=400)   
            money=Label(self,text="Current balance : €"+str(updated_balance),font=("Times",14)).place(x=380,y=40,width=300,height=100)
        
        adv=Label(self,text="Please pick the date from the calendar",font=("Times",14)).place(x=600,y=250) 
        icome=Button(self,text="Income",command=finish).place(x=620,y=300)
        expense=Button(self,text="Expense",command=finish_withdraw).place(x=680,y=300)
        
       
      
            

       
      


class FourthPage(tk.Frame):        #implimentations : change of password, view of the whole csv spreadsheet, and seaching by date 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        c1=StringVar()              #c1:new pass
        cc1=StringVar()             #cc1: confirmation 
        _search =tk.StringVar(self) #search input taken in 
     
        Lab1=Label(self,text="Date range",bg='white',font=("times",15)).place(x=300,y=100)
        Lab2=Label(self,text="to",bg='white',font=("times",15)).place(x=600,y=100)
      

       
        
        #GUI setup frame for pass changing 
        return1=Button(self,text="Return",command=lambda: controller.show_frame(SecondPage)).place(width=100,height=30,x=780,y=650)
        border2 = tk.LabelFrame(self,bg='black')
        border2.place(x=290,y=530,width=300,height=160)
        Label(border2, text="Change password", font=('Calibri',10)).place(x= 80,y=10)
        Label(border2, text="Password", font=('Calibri',12)).place(x= 10,y=80-20)
        newp=Entry(border2,width=15,show="*",bd=5,textvariable=c1)
        newp.place(x = 150,y=80-25)
        Label(border2, text="Confirm password", font=('Calibri',12)).place(x=10, y=120-25)
        newpc=Entry(border2,width=15,show="*",bd=5,textvariable=cc1)
        newpc.place(x = 150, y=120-25)                                   
       
        
        def check():                          #quick confrimation of the safe enetry of pass  
            if c1.get()== "" or cc1.get()== "":
                Label(self,text='Cant be empty!', fg='red').place(x=400,y=530)
                return
                
            file = open(login_name, 'r+')     #replacing the old pass with new one in the txt file 
            file_data = file.read()
            details = file_data.split('\n')
            current_pass = details[1]
            updated_pass = current_pass
            updated_pass =  str(c1.get())
            file_data       = file_data.replace(current_pass,str(updated_pass))
            file.seek(0)
            file.truncate(0)
            file.write(file_data)
            file.close()
    
            Label(border2,text='Password Updated', fg='green').place(x=180,y=10)     #confirmed chnage of pass + entries removed 
            newp.delete(0, END)
            newpc.delete(0,END)
                    
                    
        changepassbutton=Button(border2,text="Confirm",command=check).place(width=100,height=30,x=150,y=150-20)

        def showcsv():                    #function for displaying csv (all transactions) in pop up frame 
            global framex
            global tv1
            df=pd.read_csv(login_name+'.csv')
            framex=tk.LabelFrame(self)
            framex.place(height=200, width=400,x=400,y=300)
            tv1 = ttk.Treeview(framex)
            tv1.place(relheight=1,relwidth=1)
            treescrolly = tk.Scrollbar(framex, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
            treescrollx = tk.Scrollbar(framex, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
            tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
            treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
            treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

            tv1["column"] = list(df.columns)
            tv1["show"] = "headings"
            for column in tv1["columns"]:
                tv1.heading(column, text=column) # let the column heading = column name

            df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
            for row in df_rows:
                tv1.insert("", "end", values=row) 
            return None
        def clear():    #closeing the label frame 
            framex.destroy()
           

     
            
            
        Viewsheet=Button(self,text="View spreadsheet",command=showcsv).place(width=110,height=25,x=600+100+30+40,y=200+100+250)
        Endview=Button(self,text="close view",command=clear).place(width=110,height=25,x=600+100+30+40,y=230+100+250)

       
        #search by date in range format 
        def search_choose():      #this is the first date 
            global framex4
            global cdate
            global cdate1
            global thiscal
            framex4=tk.LabelFrame(self, bg='black')
            framex4.place(height=250, width=210,x=400,y=250)
            thiscal=Calendar(framex4, setmode='day',date_pattern= 'd/m/yy')    #date chosen from a pop clandaer and stored as the minimum range
            thiscal.place(width=200,height=200,x=1,y=1)
           
            Confirm=Button(framex4,text="Confirm",command=close)
            Confirm.place(width=110, height=25, x=100-10,y=230-10)
            
        
        def search_choose2():   #exactly like the above function but this is the max range of date 
            global framex5
            global cdate2
            global thiscal2
            framex5=tk.LabelFrame(self, bg='black')
            framex5.place(height=250, width=210,x=400,y=250)
            thiscal2=Calendar(framex5, setmode='day',date_pattern= 'd/m/yy')
            thiscal2.place(width=200,height=200,x=1,y=1)
            
           
            Confirm=Button(framex5,text="Confirm",command=close1).place(width=110, height=25, x=100-10,y=230-10)
            
            
        def close():    #closing the first pop up calendar 
            global cdate1
            cdate1= thiscal.get_date()
            Date1 = Label(self,width = 20, bd = 4,text=cdate1).place(width=100,x=450, y=100)
            framex4.destroy()
            
        def close1():    #closing the second pop up calendar  
            global cdate2
            cdate2= thiscal2.get_date()
            Date2 = Label(self,width = 20, bd = 4,text=cdate2).place(width=100,x=650, y=100)
            framex5.destroy()

        def fetch():       #showing the csv info (only from the chosen date range )
            global framex6            #very similar to the "showcsv" function but the rows are now limited to the specified range 
            global tv3
            
            df=pd.read_csv(login_name+'.csv')
            framex6=tk.LabelFrame(self)
            framex6.place(height=200, width=400,x=400,y=300)
            tv3 = ttk.Treeview(framex6)
            tv3.place(relheight=1,relwidth=1)
            treescrolly = tk.Scrollbar(framex6, orient="vertical", command=tv3.yview) # command means update the yaxis view of the widget
            treescrollx = tk.Scrollbar(framex6, orient="horizontal", command=tv3.xview) # command means update the xaxis view of the widget
            tv3.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
            treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
            treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
            #df = df[(df['Date']> cdate1) & (df['Date']< cdate2)]
            df = df.set_index(['Date'])
            print(df.loc[cdate1:cdate2])
            tv3["column"] =df.loc[cdate1:cdate2]#list(df.columns)   #   specified dates 
            tv3["show"] = "headings"
            df=df.loc[cdate1:cdate2]
            for column in tv3["columns"]:
                tv3.heading(column, text=column) # let the column heading = column name
            opencal=Button(framex6,text='Close', command=clear).place(x=1,y=1)
         
            df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
            for row in df_rows:
                tv3.insert("", "end", values=row) 
            return None
            
            
        def clear():     #closing the label frame 
            framex6.destroy()

        Label(self, text="Choose date",bg='white',font=("times",15)).place(x=300,y=140)
        Confirm21=Button(self,text="Save choice",command=fetch).place(width=300, height=25, x=450,y=180)
        opencal=Button(self,text='From', command=search_choose).place(width=100,x=500-50,y=140)  
        To=Button(self,text="To",command=search_choose2).place(width=100,x=700-50,y=140)  
  
        
    

        
            

        

class FifthPage(tk.Frame):      #implimentations : set saving target, and spending target 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global spendingt1
        savingt = StringVar()     #taking in saving taget
        spendingt = StringVar()   #taking in spending target
        Lab1=Label(self,text="Saving Target",bg='white',font=("times",15)).place(x=370,y=150)
        Lab2=Label(self,text="Spending Target",bg='white',font=("times",15)).place(x=370,y=200)
        ST = tk.Entry(self, width = 30, bd = 4,textvariable=savingt)
        ST.place(x=600, y=150)
        Spend = tk.Entry(self,width = 30, bd = 4,textvariable=spendingt)
        Spend.place(x=600, y=200)
        def tagets():     #storing the input targets into the database (txt file)
            global savingt1
            global spendingt1
            if savingt.get()== "" or spendingt.get()== "":             #safety
                Label(self,text='Cant be empty!', fg='red').place(x=500,y=400)
                return
            else:                                      #writing the input into the file + edit option (if the user chnages the set targets)
                savingt1=((savingt.get()))
                spendingt1=((spendingt.get()))
                f = open(login_name+'t',"w")   #overwrite option on the same rows         
                f.write(savingt1 + '\n')    
                f.write(spendingt1 + '\n')
                f.close()
                ST.delete(0, END)         #delete the eneries 
                Spend.delete(0,END)
            

            
        def howamidoing():               #feedback to the user 
            global framex3               #getting the balance
            global details_age
            global user_details
            file = open(login_name, 'r')
            file_data = file.read()
            user_details = file_data.split('\n')
            details_name = user_details[0]
            details_age = user_details[2]
            details_balance = user_details[3]
            file.close()
        

            file2 = open(login_name+'t', 'r+')   #getting the defined targets
            file_data2 = file2.read()
            user_details2 = file_data2.split('\n')
            details_saving2= user_details2[0]
            details_spening2= user_details2[1]
            file2.close()
            
            df=pd.read_csv(login_name+'.csv')    #getting the expense 
            df_array=df.values 
            ave_float=+df_array[:,2].mean()
            df2=pd.read_csv(login_name+'e'+'.csv')
            df_array1=df2.values
            ave1_float=(df_array1[:,0]).sum()
            print(ave1_float)
            framex3=tk.LabelFrame(self, bg='black')
            framex3.place(height=300, width=500,x=290,y=400)
             
             
            U=Label(framex3,text="Saving target:"+str(details_saving2)+' €',fg='white',bg='black',font=("times",15)).place(x=1,y=1)
            Balance=Label(framex3,text="current balance:"+details_balance +' €',fg='white',bg='black',font=("times",15)).place(x=1,y=60)
            U2=Label(framex3,text="Spending target:"+str(details_spening2)+' €',fg='white',bg='black',font=("times",15)).place(x=1,y=30)
            U3=Label(framex3,text="Spent so far:"+str(ave1_float)+' €',fg='white',bg='black',font=("times",15)).place(x=1,y=90)

            if details_saving2 <= details_balance and ave1_float <= float(spendingt1) :    #if the balance is > or= to the set target and spending not one over the defined taget
                Label(framex3, text="You are doing well" ).place(x=1,y=90+30)               #positive feed back
            else:
                Label(framex3, text="You havent managed well, you are spending too much" ).place(x=1,y=120+30)   #negative feedback 

       
        return1=Button(self,text="Return",command=lambda: controller.show_frame(SecondPage)).place(width=100,height=30,x=780,y=650)
        b2=Button(self,text="Status",command=howamidoing).place(x=710,y=300)
        submit1=Button(self,text="Submit",command=tagets).place(x=620,y=300)



class SixthPage(tk.Frame):          #implimentations: quick summary of everything 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
     

      
    
        def personal_details():              #getting username, age, balance 
           global details_age
           global user_details
           file = open(login_name, 'r')
           file_data = file.read()
           user_details = file_data.split('\n')
           details_name = user_details[0]
           details_age = user_details[2]
           details_balance = user_details[3]
        
        def summary():        #getting expense, income, net, max epense, max income
            
            global framex2
            global tv2
            global details_age
            global user_details
            global details_balance
            file = open(login_name, 'r')
            file_data = file.read()
            user_details = file_data.split('\n')
            details_name = user_details[0]
            details_age = user_details[2]
            details_balance = user_details[3]
            

            
            #expense  ave                             
            df2=pd.read_csv(login_name+'e'+'.csv')
            df_array1=df2.values
            ave1_float=(df_array1[:,0]).mean()
            rounded_ave = round(ave1_float, 2)
            ave1=str(rounded_ave)

            #income ave
            df3=pd.read_csv(login_name+'i'+'.csv')
            df_array2=df3.values
            ave2_float=(df_array2[:,0]).mean()
            rounded_ave2 = round(ave2_float, 2)
            ave2=str(rounded_ave2)
            
           
        

            df=pd.read_csv(login_name+'.csv')   #getting the net of the transactions 
            df_array=df.values 
            ave34_float=(df_array[:,2]).mean()
            rounded_ave34=round(ave34_float, 2)
            ave34=str(rounded_ave34)
        


         
          
                
          
            

            maxinc1=(-df_array[:,2]).max()    #getting max expense, and max income 
            max1=str(maxinc1)
            maxinc=df_array[:,2].max()
            max2=str(maxinc)
  

            

            
            #Displaying the all the fetched info here into a Label frame 

            
            framex2=tk.LabelFrame(self, bg='black')
            framex2.place(height=450, width=400,x=290,y=50)
            Username=Label(framex2,text="Name",fg='white',bg='black',font=("times",15)).place(x=1,y=1)
            Username1=Label(framex2,text=login_name,fg='white',bg='black',font=("times",15)).place(x=210,y=1)
            Line=Label(framex2,text='_________________________________________________________________________________________________',fg='white',bg='black',font=("times",5)).place(x=1,y=22)

            age=Label(framex2,text="Age",fg='white',bg='black',font=("times",15)).place(x=1,y=30+10)
            age1=Label(framex2,text=details_age,fg='white',bg='black',font=("times",15)).place(x=210,y=40)
            Line=Label(framex2,text='_________________________________________________________________________________________________',fg='white',bg='black',font=("times",5)).place(x=1,y=64)

            Balance=Label(framex2,text="Balance",fg='white',bg='black',font=("times",15)).place(x=1,y=60+20)
            Balance1=Label(framex2,text=details_balance+' €',fg='white',bg='black',font=("times",15)).place(x=210,y=80)
            Line=Label(framex2,text='_________________________________________________________________________________________________',fg='white',bg='black',font=("times",5)).place(x=1,y=104)
            
            Average_expense=Label(framex2,text="Average expense",fg='white',bg='black',font=("times",15)).place(x=1,y=90+30)
            Average_expense1=Label(framex2,text=ave1 + ' €',fg='white',bg='black',font=("times",15)).place(x=210,y=120)
            Line=Label(framex2,text='_________________________________________________________________________________________________',fg='white',bg='black',font=("times",5)).place(x=1,y=144)

            Average_income=Label(framex2,text="Average income",fg='white',bg='black',font=("times",15)).place(x=1,y=120+40)
            Average_income1=Label(framex2,text=ave2 +' €',fg='white',bg='black',font=("times",15)).place(x=210,y=160)
            Line=Label(framex2,text='_________________________________________________________________________________________________',fg='white',bg='black',font=("times",5)).place(x=1,y=184)

            Lexpense=Label(framex2,text="Largest expense",fg='white',bg='black',font=("times",15)).place(x=1,y=150+50)
            Lexpense1=Label(framex2,text=max1 +' €',fg='white',bg='black',font=("times",15)).place(x=210,y=200)
            Line=Label(framex2,text='_________________________________________________________________________________________________',fg='white',bg='black',font=("times",5)).place(x=1,y=224)

            Lincome=Label(framex2,text="Largest income",fg='white',bg='black',font=("times",15)).place(x=1,y=180+60)
            Lincome1=Label(framex2,text=max2 +' €',fg='white',bg='black',font=("times",15)).place(x=210,y=240)
            Line=Label(framex2,text='_________________________________________________________________________________________________',fg='white',bg='black',font=("times",5)).place(x=1,y=264)

            Common=Label(framex2,text="Combined net",fg='white',bg='black',font=("times",15)).place(x=1,y=280)
            common1=Label(framex2,text=ave34 +' €',fg='white',bg='black',font=("times",15)).place(x=210,y=280)
            #make recommendation
            
        def clear():     #closing this frame

            framex2.destroy()

        def check_categories():
            df=pd.read_csv(login_name+'.csv')
            array_of_categories=df.values 
            number=array_of_categories.shape[0]
            
             
            list_category=[]
            list_category = list(array_of_categories[:,1])
            dropdown_list= ttk.Combobox(self)
            dropdown_list.place(x=400, y=500)
            dropdown_list['values'] = list(list_category)


        View_summary=Button(self,text="View summary",command=personal_details and summary).place(width=100,height=25,x=400,y=600)   
        Endview=Button(self,text="close view",command=clear).place(width=100,height=25,x=530,y=600)
        return1=Button(self,text="Return",command=lambda: controller.show_frame(SecondPage)).place(width=100,height=30,x=780,y=650)
        analytics=Button(self,text="Graphs", command=check_categories).place(width=100, height=25,x=650, y=600)



#crap

            
class SeventhPage(tk.Frame):       #Implimentation : Playing lottery 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)                #just a randomizer
        Label(self,text="Cost: 2€",font=("Times",14)).place(width=100,x=700,y=160)
        def valget2():    #Getting the balance from textfile by BB button (refresh)
            file = open(login_name, 'r')
            file_data = file.read()
            user_details = file_data.split('\n')
            details_balance = user_details[3]
            money=Label(self,text="Current balance : €"+str(details_balance),font=("Times",14)).place(x=380,y=20,width=300,height=100)
            
        

    

        def play():
            global framex8                 #6 user inputs 
            s1 = StringVar()
            s2 = StringVar()
            s3 = StringVar()
            s4 = StringVar()
            s5 = StringVar()
            s6 = StringVar()
            framex8=tk.LabelFrame(self, bg='black')
            framex8.place(height=450, width=400,x=290,y=190)
            cgame=Button(framex8,text="Done",command=clear2).place(width=100,height=30,x=160,y=410)
            Label(framex8, text="Pick number from 1-50", font=('Times',15)).place(x=110,y=1)
            
            n1=tk.Entry(framex8,textvariable=s1)
            n1.place(width=30,height=25,x=1,y=40)              #enteries 
            n2=tk.Entry(framex8,textvariable=s2)
            n2.place(width=30,height=25,x =50,y=40)
            n3=tk.Entry(framex8,textvariable=s3)
            n3.place(width=30,height=25,x =100,y=40)
            n4=tk.Entry(framex8,textvariable=s4)
            n4.place(width=30,height=25,x = 150,y=40)
            n5=tk.Entry(framex8,textvariable=s5)
            n5.place(width=30,height=25,x = 200,y=40)
            n6=tk.Entry(framex8,textvariable=s6)
            n6.place(width=30,height=25,x = 250,y=40)
            

            def gogame():          #initiates the num generation and comparison 
                
                
                usern=[]
                L1=s1.get()             #saving the enetres in an array 
                usern.append(L1)
                L2=s2.get()
                usern.append(L2)
                L3=s3.get()
                usern.append(L3)
                L4=s4.get()
                usern.append(L4)
                L5=s5.get()
                usern.append(L5)
                L6=s6.get()
                usern.append(L6)
                #print(usern)
                lotteryNumbers = []
                
                for i in range (0,6):               #6 random numbers are generated from 1 to 5
                  number = random.randint(1,50)
                  #Check if this number has already been picked 
                  while number in lotteryNumbers:
                    # ... if it has, pick a new number instead 
                    number = random.randint(1,50)
                  
                  #Now that we have a unique number, let's append it to our list.
                  lotteryNumbers.append(number)
                
                #Sort the list in ascending order
                lotteryNumbers.sort()

                
                usern_pd=pd.DataFrame(usern)               #user input into panadas dataframe
                usern_array=usern_pd.values
                print(usern_array)
                for i in (0,5):
                    if ((int(usern_array[i,0])<1) or (int(usern_array[i,0])>50)):                #safety check that the numbers not too big not negative 
                        Label(framex8,text="Invalid numbers, Please eneter between 1 to 50. Please re-enter").place(x=1,y=120)
                        usern.clear()
                    else:
                        Label(framex8,text="Today's lottery numbers are: "+str(lotteryNumbers)).place(x=1,y=160)      #if all good, deduct money from database
                        Label(framex8,text="Your number :"+ str(usern)).place(x=1,y=200)
                        file = open(login_name, 'r+')
                        file_data = file.read()
                        details = file_data.split('\n')
                        current_balance = details[3]
                        updated_balance = current_balance
                        updated_balance = float(updated_balance) - 1
                        file_data       = file_data.replace(current_balance, str(updated_balance))
                        file.seek(0)
                        file.truncate(0)
                        file.write(file_data)
                        file.close()
                        thisdate=mydate.get_date()
                        thiscat=("Lotto")
                        thisamount=(-1)
                        thisamount3=(1)
                        with open(login_name+'.csv', 'a') as file1:
                            myFile= csv.writer(file1)
                            #myFile.writerow(["Money","category","amount","date"])
                            myFile.writerow([updated_balance,thiscat,thisamount,thisdate])
                         
            
                        with open(login_name+'e'+'.csv', "a") as file3:
                            myFile3= csv.writer(file3)
                            myFile3.writerow([thisamount3])
                            file3.close() 
                        valget2()
            
                        
                    
                
        
    
    
                counter = 0                                        #checking how many the user got right 
                for number in usern:
                    if number in lotteryNumbers:
                        counter+1
                Label(framex8,text='Matching numbers: '+str(counter)).place(x=1,y=240)
                if counter==4:                                                              #prices , if 4 correct win 4 euros
                    Label(framex8,text='You have won 4€ ').place(x=1,y=280)
                    file = open(login_name, 'r+')
                    file_data = file.read()
                    details = file_data.split('\n')
                    current_balance = details[3]
                    updated_balance = current_balance
                    updated_balance = float(updated_balance) + 4
                    file_data       = file_data.replace(current_balance, str(updated_balance))
                    file.seek(0)
                    file.truncate(0)
                    file.write(file_data)
                    file.close()
                    thisdate=mydate.get_date()
                    thiscat=("Lotto")
                    thisamount=(4)
                    thisamount3=(4)
                    with open(login_name+'.csv', 'a') as file1:
                        myFile= csv.writer(file1)
                        #myFile.writerow(["Money","category","amount","date"])
                        myFile.writerow([updated_balance,thiscat,thisamount,thisdate])
                     
        
                    with open(login_name+'i'+'.csv', "a") as file4:
                        myFile4= csv.writer(file4)
                        myFile4.writerow([thisamount3])
                        file4.close() 
                    valget2()
                elif counter == 5:                                             #if 5 correct win 100 euros
                    Label(framex8,text='You have won 100€ ').place(x=1,y=280)
                    file = open(login_name, 'r+')
                    file_data = file.read()
                    details = file_data.split('\n')
                    current_balance = details[3]
                    updated_balance = current_balance
                    updated_balance = float(updated_balance) + 100
                    file_data       = file_data.replace(current_balance, str(updated_balance))
                    file.seek(0)
                    file.truncate(0)
                    file.write(file_data)
                    file.close()
                    thisdate=mydate.get_date()
                    thiscat=("Lotto")
                    thisamount=(100)
                    thisamount3=(100)
                    with open(login_name+'.csv', 'a') as file1:
                        myFile= csv.writer(file1)
                        #myFile.writerow(["Money","category","amount","date"])
                        myFile.writerow([updated_balance,thiscat,thisamount,thisdate])
                     
        
                    with open(login_name+'i'+'.csv', "a") as file4:
                        myFile4= csv.writer(file4)
                        myFile4.writerow([thisamount3])
                        file4.close() 
                    valget2() 
                elif counter ==6:                                                              #if 6 correct win 1M euros
                    Label(framex8,text='You have won 1000000€ ').place(x=1,y=280)
                    file = open(login_name, 'r+')
                    file_data = file.read()
                    details = file_data.split('\n')
                    current_balance = details[3]
                    updated_balance = current_balance
                    updated_balance = float(updated_balance) + 1000000
                    file_data       = file_data.replace(current_balance, str(updated_balance))
                    file.seek(0)
                    file.truncate(0)
                    file.write(file_data)
                    file.close()
                    thisdate=mydate.get_date()
                    thiscat=("Lotto")
                    thisamount=(1000000)
                    thisamount3=(1000000)
                    with open(login_name+'.csv', 'a') as file1:
                        myFile= csv.writer(file1)
                        #myFile.writerow(["Money","category","amount","date"])
                        myFile.writerow([updated_balance,thiscat,thisamount,thisdate])
                     
        
                    with open(login_name+'i'+'.csv', "a") as file4:
                        myFile4= csv.writer(file4)
                        myFile4.writerow([thisamount3])
                        file4.close() 
                    valget2()


                n1.delete(0, END) 
                n2.delete(0, END)
                n3.delete(0, END)
                n4.delete(0, END)
                n5.delete(0, END)
                n6.delete(0, END)
            
            c2game=Button(framex8,text="Enter",command=gogame).place(width=100,height=30,x=1,y=80)
        def clear2():     #closing this frame 
            framex8.destroy()

        BB=tk.Button(self, text="Show balance", command=valget2).place(x=460,y=150,width=110,height=25) 
        return1=Button(self,text="Return",command=lambda: controller.show_frame(SecondPage)).place(width=100,height=30,x=780,y=650)
        play=Button(self,text="Play",command=play).place(width=100,height=30,x=400,y=650)












class Registerpage(tk.Frame):          #implimentation : Register oage 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        temp_name = StringVar()     #get name
        temp_age = StringVar()      #get age
        temp_password = StringVar() #get password 
        Label(self, text="Please enter your details below to register", font=('Calibri',12)).place(width=300,height=30,x=500,y=50)
        Label(self, text="Name", font=('Calibri',12)).place(width=100,height=30,x=500,y=250)
        Label(self, text="Age", font=('Calibri',12)).place(width=100,height=30,x=500,y=300)
        Label(self, text="Password", font=('Calibri',12)).place(width=100,height=30,x=500,y=350)
        
        namenetry=tk.Entry(self,textvariable=temp_name)
        namenetry.place(width=100,height=30,x=650,y=250)
        ageentry=tk.Entry(self,textvariable=temp_age)
        ageentry.place(width=100,height=30,x=650,y=300)
        passentry=tk.Entry(self,textvariable=temp_password,show="*")
        passentry.place(width=100,height=30,x=650,y=350)
        
       
         
        
        def finish_reg():     #Getting the userinfo into the file and opening database for the user 
            global df
            global age
            name = temp_name.get()
            age = temp_age.get()
            password = temp_password.get()   #getting the eneries 
            all_accounts = os.listdir()  
            print(name)
            if name == "" or age == "" or password == "":    #safety for input
                notiferr = Label(self,fg="red",text="All fields requried * ",font=('Calibri',12)).place(width=300,height=30,x=500,y=600)
                return
                
            for name_check in all_accounts:    #safety for not allowing multiple accounts with the same name 
                if name == name_check:
                    notiferr = Label(self,fg="red",text="Account already exists ",font=('Calibri',12)).place(width=300,height=30,x=500,y=600)
                    return
                #else:                    
                new_file = open(name,"w")   #cred txtfile database 
                new_file.write(name+'\n')
                new_file.write(password+'\n')
                new_file.write(age+'\n')     
                new_file.write('0')
                new_file.close()
                new_file1 = open(name+'.csv', "w")     #general transaction csv database 
                writer= csv.writer(new_file1)
                writer.writerow(['Money','Category','Amount','Date'])
                
                new_file1.close()
                df=pd.read_csv(name+'.csv')    #creating pandas dataframe for the user 

                expensefile = open(name+'e'+'.csv', "w")   #file for negative transactions 
                writer= csv.writer(expensefile)
                writer.writerow(['expense'])
                expensefile.close()

                incomefile = open(name+'i'+'.csv', "w")   #file for positive transactions 
                writer= csv.writer(incomefile)
                writer.writerow(['income'])
                incomefile.close()
                namenetry.delete(0, END)
                ageentry.delete(0, END)
                passentry.delete(0, END)
                
                
         
               
                

                
            
                    

                notiferr = Label(self,fg="green", text="Account has been created",font=('Calibri',12)).place(width=300,height=30,x=500,y=600)
        Button(self, text="Register", command = finish_reg, font=('Calibri',12)).place(width=100,height=30,x=500,y=500)    
        Backing=tk.Button(self, text="Back to login",font=('Calibri',12), command=lambda: controller.show_frame(FirstPage)).place(width=100,height=30,x=650,y=500)

#Central class
class Application(tk.Tk):     #implimantions: All pages=> same theme, clock, calendar, exit button, help buttom 
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #creating a window
        window = tk.Frame(self)
        window.pack()
        window.config(bg="black")
        window.grid_rowconfigure(0, minsize = 700)
        window.grid_columnconfigure(0, minsize = 900)
    
        
        
        self.frames = {}     #access to all other classes (subframes (pages))
        for F in (FirstPage, SecondPage, ThirdPage,FourthPage,FifthPage,SixthPage,SeventhPage,Registerpage):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row = 0, column=0, sticky="nsew")
            
        self.show_frame(FirstPage)   #default show first page
        
    def show_frame(self, page):    #clock, theme and calndar 
        global mydate
        frame = self.frames[page]
        frame.tkraise()
        self.resizable(width=False, height=False)  #same size
        self.bakc=frame.config(bg="black")    #black background
        self.title("Amazing buttler")
        self.ex=Button(frame, text="Exit", command=exit).place(x=3, y=675, width=60, height=25) #exit button
        info="Register and login!\n\n\tEnjoy!"
        self.help=Button(frame, text="Help", command= lambda: ms.showinfo("Information",info)).place(x=840,y=10, width=60, height=25)   #help button
        self.Timeframe =tk.LabelFrame(frame, text="Local Time", fg="white", bg="black",font=("Times",15),bd=0).place(x=20,y=40,width=220, height=230)  #title on the screen
        current_time=tm.strftime('%H:%M')#clock
        self.clock_label=Label(self.Timeframe, font='Times 50', bg='black', fg='red', text=current_time).place(x=10,y=100)

        self.Datelbl=tk.Label(frame, text="Date", fg="white", bg="black",font=("Times",15)).place(y=300)  #title on the screen
        #Label(text=current_date).place(y=380,width=300, height=280)
        self.calendarini= Calendar(frame, selectmode="day", year=today.year, month=today.month, day=today.day, date_pattern='dd/mm/y')#calendar 
        self.calendarini.place(y=330,width=280, height=280)
        mydate=self.calendarini    #global access to this calndar with mydate 
        
      
      

app = Application()
app.maxsize(1000,800)
app.mainloop()

