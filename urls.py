from django.urls import path
from . import views
from django.contrib.auth import views as ad
urlpatterns=[
    path('',views.start,name="ho"),
    path('sign_up/',views.signup,name="log"),
    path('otp_verfication/',views.otpcheck,name="otp"),
    path('create_password/',views.createpass,name="sep"),
    path('login/',views.loginuser,name="lou"),
    path('profile/',views.profile,name="pro"),
    path('news/',views.news,name="new"),
    path('Alters/',views.alters,name="alt"),
    path('login_incorrect/',views.loginc,name="loginc"),
    path('temp/',views.temp,name="temp"),
    path('notf/',views.notfound,name="notf"),
    path('Forgotpassword/',views.forgotpassword,name="forp"),
    path('otpcheck/',views.otppassword,name="forotp"),
    path('changepassword/',views.changepassword,name="chgp"),
    path('logout/',views.logou,name="loout"),
    #policy makers code starts from here
    #path('polog/',views.polog,name="polog"),
    path('plgn/',ad.LoginView.as_view(template_name="html/pologin.html"),name="plog"),
    path('plout/',ad.LogoutView.as_view(template_name="html/start.html"),name="lgt"),
    #username=adminAAYH
    #password=AAYH123
    path('pancl/',views.paclimate,name="panc"),
    path('grp/',views.graph,name="grp"),
    path('indiagraphs/',views.indgrp,name="indg"),
    path('predict/',views.predict,name="pred"),
    path('comm/',views.commits,name="com"),
]