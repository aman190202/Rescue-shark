from os import name
from flask import Flask, redirect, url_for, request
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from twilio.rest import Client 
import pandas as pd

df1=pd.read_csv("data.csv")
 
account_sid = 'ACe601f95cfb82423582b96f77ea0f9af7' 
auth_token = '0b950f1ade33ce75761e18dab6aee2b0' 
client = Client(account_sid, auth_token) 

app= Flask(__name__)

def activatehelp(number):
    for i in range(df1.shape[0]):
        num=df1['number'][i]
        num=str(num)
        num='whatsapp:'+num
        number=str(number)
        body=number+' needs help right now! '
        message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body=body,      
                              to=num 
                          ) 
        message.sid


@app.route('/register/<user>')
def register(user):
    return '<div style="text-align: center; "><h1>%s Whatsapp +1 415 523 8886 with code join daily-frame.</h1><br><a href="/">BACK</a></div>' % user


@app.route('/',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user1 = request.form['nm']
      content=user1.split()
      df2=pd.DataFrame({"number":[content[0]], "name":[content[1]]})
      df2=df2.append(df1)
      df2.to_csv("data.csv")
      return redirect(url_for('register',user=content[1]))

   return render_template('base.html')

@app.route('/help',methods = ['POST', 'GET'])
def help():
   if request.method == 'POST':
      user1 = request.form['nm']
      pos=0
      for i in df1['name']:
          if(i==user1):
              number=df1['number'][pos]
              activatehelp(number)
              break
          else:
              pos+=1


      return 'SIT TIGHT!HELP IS ON THE WAY'

   return render_template('help.html')




if __name__=='__main__':
    app.run(debug=True)