from flask import Flask, render_template, request, flash, redirect
##from tensorflow.keras.models import load_model
import sqlite3
import pickle
import numpy as np
import random
import requests
import warnings
warnings.filterwarnings('ignore')
model = pickle.load(open('LL.pkl', 'rb'))
import telepot
bot=telepot.Bot("6883989531:AAFDgb3ovqvoVru9UmMay2O7Ud_xi-pU0UY")
chatid="1411212019"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/class1')
def class1():
   return render_template('class1.html')

@app.route('/class2')
def class2():
   return render_template('class2.html')
@app.route('/class3')
def class3():
   return render_template('class3.html')
@app.route('/class4')
def class4():
   return render_template('class4.html')

@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()

        if len(result) == 0:
            return render_template('index.html', msg='Sorry , Incorrect Credentials Provided,  Try Again')
        else:
            data=requests.get("https://api.thingspeak.com/channels/2545971/feeds.json?api_key=23A6J0KT198JNNFI&results=2")
            bp=float(data.json()['feeds'][-1]['field1'])
            hb=float(data.json()['feeds'][-1]['field3'])
            oxy=float(data.json()['feeds'][-1]['field2'])
            ecg=float(data.json()['feeds'][-1]['field5'])
            temp=float(data.json()['feeds'][-1]['field4'])
           
            return render_template('logged.html',hb=hb,temp=temp,oxy=oxy,ecg=ecg,bp=bp)

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/logout')
def logout():
    return render_template('index.html')


@app.route("/kidneyPage")
def kidneyPage():
    data=requests.get("https://api.thingspeak.com/channels/2545971/feeds.json?api_key=23A6J0KT198JNNFI&results=2")
    bp=float(data.json()['feeds'][-1]['field1'])
    hb=float(data.json()['feeds'][-1]['field3'])
    oxy=float(data.json()['feeds'][-1]['field2'])
    ecg=float(data.json()['feeds'][-1]['field5'])
    temp=float(data.json()['feeds'][-1]['field4'])
    return render_template('logged.html',hb=hb,temp=temp,oxy=oxy,ecg=ecg,bp=bp)


@app.route("/predictPage", methods = ['POST', 'GET'])
def predictPage():
    
 
    name = request.form['name']
    Age = request.form['age']
    sexx = int(request.form['sex'])
    if sexx==1:
        sex="MALE"
    elif sexx==0:
        sex="FEMALE"
    else:
        sex="others"
    bp = request.form['bp']
    oxy = request.form['oxy']
    print(oxy)
    hb = request.form['heart']
    ecg = request.form['ecg']
    Temperature = request.form['Temperature']
    to_predict_list = np.array([[bp,oxy,hb,ecg,Temperature]])
    print(to_predict_list)
    prediction = model.predict(to_predict_list)
    output = prediction[0]
    print("Prediction is {}  :  ".format(output))
    print(output)
    
    # Check the output values and retrive the result with html tag based on the value
    
    if output == 1:
        result="Healthy    !!!!!!" 
        med=""
        bot.sendMessage(chatid,str("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)))
    if output == 2:
        result="Fever" 
        med="Diagnosis Drugs for Fever  \n  Paracetamol \n acetaminophen \n Tylenol  \n aspirin \n  Acephen  \n Ecpirin \n"
        bot.sendMessage(chatid,str("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)+" \n  Medicine Provided  :  "+str(med)+ "LOCATION:  https://maps.app.goo.gl/gxPvR7ZUUfP5i2c27"))
    if output == 3:
        result="Chest Pain" 
        med="Diagnosis Drugs for chest_pain \n Amlodipine \n Nadroparin \n Isosorbide \n Nifedipine \n Atenolol \n Diltiazem \n"
        bot.sendMessage(chatid,str("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)+" \n  Medicine Provided  :  "+str(med)+ "LOCATION https://maps.app.goo.gl/gxPvR7ZUUfP5i2c27"))
    if output == 4:
        result="Critical" 
        med="You are critical \n concern the doctor nearby"
        print("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)+" \n  Medicine Provided  :  "+str(med)+ "LOCATION https://maps.app.goo.gl/gxPvR7ZUUfP5i2c27")
        bot.sendMessage(chatid,str("Patient  :  "+str(name)+ "\n Age  :  "+str(Age)+ "\n Gender  :  "+str(sex)+ "\n Status  :  "+str(result)+" \n  Medicine Provided  :  "+str(med)+ "LOCATION https://maps.app.goo.gl/gxPvR7ZUUfP5i2c27"))
    
    
    # out=output
    print(result,output)
    return render_template('predict.html', result = result,out=output,name =name,med=med )  #,out=out)

    # return render_template('logged.html')

@app.route('/msg',methods = ['POST', 'GET'])
def msg():
    if request.method == 'POST':
        fileName=request.form['filename']
        img='dataset/'+fileName
        bot.sendPhoto(chatid, photo=open(img,'rb'))

    return render_template('logged.html')


if __name__ == '__main__':
	app.run(debug = True, use_reloader=False)
