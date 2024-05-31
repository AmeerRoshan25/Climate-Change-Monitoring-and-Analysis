from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import sigup,comments
import math,random
from climate import settings
from django.core.mail import send_mail
import json
import requests,datetime
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
# Create your views here.
#s=[]
def sotp():
	d="0123456789"
	otp=""
	for i in range(4):
		otp+=d[math.floor(random.random()*10)]
		#s.append(otp)
	return otp

#just getting news form api using function
def print_top_10_weather_alerts():
    head = []
    api_key = '3e6f03796efa4e0f87016b7a6fb5f25b'
    api_url = 'https://newsapi.org/v2/everything'
    params = {
        'q': 'weather alert India',  # Include "India" in the search query
        'apiKey': api_key,
        'pageSize': 10  # Limit the number of articles to 10
    }

    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        if articles:
            print("Top 10 Weather Alerts in India:")
            for article in articles:
                headline = article.get('title')
                head.append(headline)
            return head  # Print the headline directly
        else:
            print("No weather alerts found.")
    else:
        print("Failed to fetch data:", response.status_code)

def start(request):
	return render(request,'html/start.html')

def signup(request):
	if request.method=="POST":
			n=request.POST['na']
			p=request.POST['pa']
			e=request.POST['ms']
			t=settings.EMAIL_HOST_USER
			sbj='OTP for SignUp'
			o=sotp()
			print(o)
			request.session['otp']=o
			request.session['emaill']=e
			request.session['place']=p
			request.session['name']=n
			m=f"Dear {n},\n Thank you for signing up for our climate website! To ensure the security of your account and provide personalized weather updates for your city, we require verification through a one-time password (OTP). Your OTP code is:\n{o}\nPlease enter this code on the verification page to complete your registration process. If you did not request this OTP, please ignore this message.\nBest regards,\nClimate Website Team"
			s=send_mail(sbj,m,t,[e])
			if(True):
				return redirect('otp')
	return render(request,'html/sign-up.html')

def otpcheck(request):
	try:
		if request.method=="POST":
			o=request.POST['otp']
			e=request.session.get('otp')
			ema=request.session.get('emaill')
			p=request.session.get('place')
			n=request.session.get('name')
			if(o==e):
				u=sigup.objects.create(name=n,place=p,em=ema)
				return redirect('sep')
			else:
				return render(request,'html/otpch.html',{'error':"OTP Is Invalid"})
	except:
		return render(request,'html/loguser.html',{'l':"Already you have a Account please Login"})
	return render(request,'html/otpch.html')

def createpass(request):
	e=request.session.get('emaill')
	print(e)
	try:
		if request.method=="POST":
			#e=request.session.get('emaill')
			print(e,type(e))
			p=request.POST['pa']
			h=request.POST['ca']
			if(p==h):
				x=sigup.objects.get(em=e)
				x.pasw=p
				x.save()
				t=settings.EMAIL_HOST_USER
				sbj='Welcome to  Climate Website!'
				m=f"Congratulations on successfully registering on Climate Website ! We are excited to welcome you to our community of weather enthusiasts!\nThank you for joining us on our mission to empower individuals with accurate weather information. We look forward to providing you with a seamless and enriching experience.\nBest regards,\nClimate Website Team"
				s=send_mail(sbj,m,t,[e])
				return redirect('lou')
			else:
				return render(request,'html/crepa.html',{'error':"confirm password does not match",'n':e})
	except:
		return redirect('notf')
	return render(request,'html/crepa.html',{'n':e})

def loginuser(request):
	try:
		if request.method=="POST":
			e=request.POST['ms']
			print(e)
			request.session['ms']=e
			p=request.POST['pa']
			x=sigup.objects.get(em=e)
			t=x.pasw
			if(p==t):
				request.session['email']=e
				return redirect('pro')
			else:
				return redirect('loginc')
	except:
		return redirect('notf')
	return render(request,'html/loguser.html')

def news(request):
	k=print_top_10_weather_alerts()
	return render(request,'html/news.html',{'n':k})

def alters(request):
	k=comments.objects.all()
	return render(request,'html/Alters.html',{'n':k})

def profile(request):
	current_datetime = datetime.datetime.now()
	cur_time = current_datetime.time()
	if cur_time >= datetime.time(hour=16, minute=0, second=0):
		b = "Good Evening"
	elif cur_time <= datetime.time(hour=11, minute=0, second=0):
		b = "Good Morning"
	else:
		b = "Good Afternoon"
	e = request.session.get('ms')
	try:
		x = sigup.objects.get(em=e)
		p = x.name
	except ObjectDoesNotExist:
		t = "Guest" 
	e=request.session.get('email')
	x=sigup.objects.get(em=e)
	t=x.place
	n=x.name
	k=x.em
	return render(request,'html/profile.html',{'n':n,'p':t,'e':k,'greeting': b, 'username': p})

def loginc(request):
	return render(request,'html/loginc.html')

def notfound(request):
	return render(request,'html/notfo.html')

def temp(request):
	try:
		e=request.session.get('email')
		x=sigup.objects.get(em=e)
		t=x.place
		apikey="3242af83f560996220f006015d1d544e"
		baseurl="https://api.openweathermap.org/data/2.5/weather?q="
		completeurl= baseurl + t + "&appid=" + apikey + "&units=metric"
		response = requests.get(completeurl)
		data=response.json()
		w=data['weather'][0]['main']
		des=data['weather'][0]['description']
		cut=data["main"]["temp"]
		mintemp=data["main"]["temp_min"]
		maxtemp=data["main"]["temp_max"]
		hum=data["main"]["humidity"]
		pre=data["main"]["pressure"]
		wind=data["wind"]["speed"]
		cld=data["clouds"]["all"]
		print("cld",cld)
		return render(request,'html/temp.html',{'p':t,'w':w,'ct':cut,'mit':mintemp,'mat':maxtemp,'sp':wind,'hun':hum,'pre':pre,'des':des,'cld':cld})
	except:
		w="404 Error !"
		L=f"Data NOT Found FOR "
		return render(request,'html/temp.html',{'cud':w,'curda':L,'p':t})

def forgotpassword(request):
	try:
		if request.method=="POST":
			c=request.POST['ms']
			x=sigup.objects.get(em=c)
			g=x.name
			t=settings.EMAIL_HOST_USER
			sbj='Password Reset Request'
			o=sotp()
			print(o)
			m=f"Dear {g},\nWe received a request to reset your password for our climate website. To proceed with resetting your password, please follow the OTP below\nOTP CODE : {o}\nBest regards,\nClimate Website Team"
			s=send_mail(sbj,m,t,[c])
			request.session['otp']=o
			request.session['emailfor']=c
			return redirect('forotp')
	except:
		return render(request,'html/start.html',{'error':"Do not hava a account.please sign-up first"})
	return render(request,'html/forgotpass.html')

def otppassword(request):
	e=request.session.get('otp')
	if request.method=="POST":
			o=request.POST['otp']
			if(o==e):
				return redirect('chgp')
			else:
				return render(request,'html/forgototp.html',{'error':"OTP Is Invalid"})
	return render(request,'html/forgototp.html')

def changepassword(request):
	e=request.session.get('emailfor')
	try:
		if request.method=="POST":
			p=request.POST['pa']
			h=request.POST['ca']
			if(p==h):
				x=sigup.objects.get(em=e)
				x.pasw=p
				x.save()
				return redirect('lou')
			else:
				return render(request,'html/chgpass.html',{'error':"confirm password does not match",'n':e})
	except:
		return redirect('notf')

	return render(request,'html/chgpass.html',{'n':e})

def logou(request):
	logout(request)
	return redirect('ho')


# policy makers code starts from here

#def polog(request):
	#return render(request,'html/pologin.html')
 
def paclimate(request):
	try:
		if request.method=="POST":
			c=request.POST['pa']
			apikey="3242af83f560996220f006015d1d544e"
			baseurl="https://api.openweathermap.org/data/2.5/weather?q="
			completeurl= baseurl + c + "&appid=" + apikey + "&units=metric"
			response = requests.get(completeurl)
			data=response.json()
			w=data['weather'][0]['main']
			des=data['weather'][0]['description']
			cut=data["main"]["temp"]
			mintemp=data["main"]["temp_min"]
			maxtemp=data["main"]["temp_max"]
			hum=data["main"]["humidity"]
			pre=data["main"]["pressure"]
			wind=data["wind"]["speed"]
			cld=data["clouds"]["all"]
			return render(request,'html/panc.html',{'w':w,'ct':cut,'mit':mintemp,'mat':maxtemp,'sp':wind,'hun':hum,'pre':pre,'des':des,'cld':cld})
	except:
		k="404 Error !"
		L=f"Data NOT Found FOR City"
		return render(request,'html/panc.html',{'k':k,'l':L})
	return render(request,'html/panc.html')


# graphs code
def get_graph():
	buffer=BytesIO()
	plt.savefig(buffer,format='png')
	buffer.seek(0)
	image_png=buffer.getvalue()
	graph=base64.b64encode(image_png)
	graph=graph.decode('utf-8')
	buffer.close()
	return graph

def get_plot(x,y):
	plt.switch_backend('AGG')
	plt.figure(figsize=(6,4))
	plt.title('tem')
	plt.plot(x,y)
	plt.xticks(rotation=45)
	plt.xlabel('year')
	plt.ylabel('temp')
	plt.tight_layout()
	graph=get_graph()
	return graph

def ind_plot(x):
	plt.switch_backend('AGG')
	plt.figure(figsize=(6,4))
	plt.title('avg_temp_by_state')
	plt.plot(x)
	plt.xticks(rotation=45)
	plt.xlabel('year')
	plt.ylabel('temp')
	plt.tight_layout()
	graph=get_graph()
	return graph


def bar_plot(x,y):
	plt.switch_backend('AGG')
	plt.figure(figsize=(6,4))
	plt.title('tem')
	plt.bar(x,y ,color = "#4CAF50")
	plt.xticks(rotation=45)
	plt.xlabel('year')
	plt.ylabel('temp')
	plt.tight_layout()
	graph=get_graph()
	return graph

def in_bar_plot(x):
	plt.switch_backend('AGG')
	plt.figure(figsize=(6,4))
	x.plot(kind='bar', color='orange')
	plt.xlabel('State')
	plt.ylabel(' Temperature (°C)')
	plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
	plt.tight_layout()
	graph=get_graph()
	return graph


# predict months for user selected years

def predict_temperature(year, month):
    data = pd.read_csv("C:\\Users\\Ameer roshan\\Downloads\\sample data final.csv")
    x = data["YEAR"].values.reshape(-1, 1)
    y = data["ANN"]
    poly_features = PolynomialFeatures(degree=3)
    x_poly = poly_features.fit_transform(x)
    poly_model = LinearRegression()
    poly_model.fit(x_poly, y)
    month_index = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'].index(month.upper())
    # Predict temperature for the given year using the polynomial model
    year_poly = poly_features.transform(np.array([[year]]))
    predicted_temperature = poly_model.predict(year_poly)
    return predicted_temperature[0]

def graph(request):
	data=pd.read_csv("C:\\Users\\Ameer roshan\\Downloads\\sample data final.csv")
	x=data["YEAR"]
	y=data["ANN"]
	chart=get_plot(x,y)
	bar=bar_plot(x,y)
	return render(request,'html/pgrp.html',{'chart':chart,'bar':bar})

def indgrp(request):
	data=pd.read_csv("C:\\Users\\Ameer roshan\\Downloads\\weather csv.csv")
	avg_feels_like_by_state = data.groupby('region')['feels_like_celsius'].mean().sort_values()
	feels=in_bar_plot(avg_feels_like_by_state)
	avg_temp_by_state = data.groupby('region')['temperature_celsius'].mean().sort_values()
	temp=ind_plot(avg_temp_by_state)
	return render(request,'html/indgrp.html',{'feel':feels,'temp':temp})


def predict(request):
	data=pd.read_csv("C:\\Users\\Ameer roshan\\Downloads\\sample data final.csv")
	x=data["YEAR"]
	y=data["ANN"]
	mymodel=np.poly1d(np.polyfit(x,y,3))
	try:
		if request.method=="POST":
			x=request.POST['pa']
			s=request.POST['smo']
			year=float(x)
			y=mymodel(year)
			g=predict_temperature(x,s)
			return render(request,'html/predict.html',{'year':x,'pre':f"{g:.2f}",'m':s})
	except:
		return render(request,'html/predict.html',{'year':x,'pre':f"{y:.2f}"})
	return render(request,'html/predict.html')

def commits(request):
	if request.method=="POST":
			p=request.POST['pa']
			e=request.POST['ms']
			o=request.POST['st']
			print(o)
			try:
				x=sigup.objects.get(em=e)
				v=x.em
				if(o=="comment"):
					u=comments.objects.create(signup=v,comm=p,post="N/A")
				else:
					u=comments.objects.create(signup=v,post=p,comm="N/A")
			except:
				return redirect("ho")
	l=comments.objects.all()
	return render(request,'html/comm.html',{'o':l})

