from django.shortcuts import render
from django.http.response import HttpResponseRedirect
# Create your views here.
from telethon import TelegramClient
from telethon.tl.types import InputPeerChat
from telethon.tl.functions.contacts import ResolveUsernameRequest
from django.core.files.storage import FileSystemStorage
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.functions.channels import InviteToChannelRequest
import time
from django.conf import settings
import os
import csv
api_id=277999
api_hash = '0ae0a703c7a845b4a710b8581a92e7be'
phone_number='+919234566892'
global client 
global phone1

change=True
def index(requests):
    client = TelegramClient(phone_number, api_id, api_hash)
    client.session.report_errors = False
    client.connect()
    context={}
    if not client.is_user_authorized():
        return HttpResponseRedirect("login/")
    else:
        change=False
        return HttpResponseRedirect("main/")

    return render(requests,"index.html",context)
def main(request):
    context={}
    return render(request,"main.html",context)

def login1(request):
    context={}
    global phone1
    phone=request.POST.get("phone_number")
    phone1=phone
    print(phone1)
    client.send_code_request(phone)
    return render(request,"otp.html",context)
def login(request):
    context={}
    
    return render(request,"login.html",context)
def otp(request):
    global phone1
    context={}
    print(phone1)
    if request.method=='POST':
        otp_value=request.POST.get("otp")
        client.sign_in(phone1,otp_value)
        return HttpResponseRedirect("/main/")
    return render(request,"otp.html",context)
def abc(request):
    context={}
    return render(request,"getmembers.html",context)

def getmembers(request):
    org_gid=request.POST.get('groupid')
    if org_gid.isnumeric():
        ulist=client.get_participants(int(org_gid))
    else:
        ulist=client.get_participants(org_gid)
    olist=[]
    count=0
    for u in ulist:
        count=count+1
        olist.append([u.id,u.first_name,u.last_name,u.username,"not invited"])
    message="you can get a maximum of 10000 top active users from a group and if you try to use it again you will some different memebers but count will be 10000 only"        
    context={"olist":olist,"message":message}
    return render(request,"displaymembers.html",context)

def bcd(request):
    context={}
    return render(request,"addmembers.html",context)
def addmembers(request):
    org_gid=request.POST.get('originalid')
    opp_gid=request.POST.get('opponentid')
    ulist=client.get_participants(opp_gid)
    count=0
    message=""
    olist=[]
    i=0
    for u in ulist:
        i=i+1
        if org_gid.isnumeric():
            try:
                client(InviteToChannelRequest(int(org_gid),[u.id]))
                olist.append([u.id,u.first_name,u.last_name,u.username,"invited"])
                count=count+1
            except Exception as e:
                r="not invited due to error with user"+str(e)
                olist.append([u.id,u.first_name,u.last_name,u.username,r])
                y=str(e)
                print(y)
                if y.lower()=="too many requests":
                    message="your account has exceeded limit so has to wait for 24 hrs to use this account again"
                    break
                pass
        else:
            try:
                client(InviteToChannelRequest(org_gid,[u.id]))
                olist.append([u.id,u.first_name,u.last_name,u.username,"invited"])
                count=count+1
            except:
                r="not invited due to error with user"+str(e)
                olist.append([u.id,u.first_name,u.last_name,u.username,r])
                y=str(e)
                print(y)
                if y.lower()=="too many requests":
                    message="your account has exceeded limit so has to wait for 24 hrs to use this account again"
                    break
                pass
        if count>=50 or i>=65:
            message="you have added 50 members from this account and if you continue using this account further your account will be banned so best option is to use another signout an login through another account and continue the process"
            break
    context={"olist":olist,"message":message}
    return render(request,"displaymembers.html",context)

def cde(request):
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, "userlistfile.csv"))
    except:
        pass
    context={}
    return render(request,"custommembers.html",context)

def custommembers(request):
    org_gid=request.POST.get('originalid')
    myfile=request.FILES['userlist']
    fs = FileSystemStorage()
    filename = fs.save("userlistfile.csv", myfile)
    fname=os.path.join(settings.MEDIA_ROOT,"userlistfile.csv")
    userlist=open(fname,'r+',encoding="utf-8",errors='ignore')
    readCSV=list(csv.reader(userlist,delimiter=','))
    del readCSV[0]
    count=0
    olist=[]
    message=""
    i=0
    for row in readCSV:
        userid=int(row[0])
        if row[4]=="not invited":
            i=i+1
            if org_gid.isnumeric():
                try:
                    client(InviteToChannelRequest(int(org_gid),[userid]))
                    row[4]="invited"
                    olist.append([row[0],row[1],row[2],row[3],row[4]])
                    count=count+1
                except Exception as e:
                    row[4]="not invited due to error with user"+str(e)
                    olist.append([row[0],row[1],row[2],row[3],row[4]])
                    y=str(e)
                    print(y)
                    if y.lower()=="too many requests":
                        message="your account has exceeded limit so has to wait for 24 hrs to use this account again"
                        break
                    pass
            else:
                try:
                    client(InviteToChannelRequest(org_gid,[userid]))
                    row[4]="invited"
                    olist.append([row[0],row[1],row[2],row[3],row[4]])
                    count=count+1
                except Exception as e:
                    row[4]="not invited due to error with user"+str(e)
                    olist.append([row[0],row[1],row[2],row[3],row[4]])
                    y=str(e)
                    print(y)
                    if y.lower()=="too many requests":
                        message="your account has exceeded limit so has to wait for 24 hrs to use this account again"
                        break
                    pass
            if count>=50 or i>=65:
                message="you have added 50 members from this account and if you continue using this account further your account will be banned so best option is to use another signout an login through another account and continue the process"
                break
        else:
            continue
    context={"olist":olist,"message":message}
    userlist.close()
    return render(request,"displaymembers.html",context)


def signout(request):
    global client
    client.connect()
    client.log_out()
    client = TelegramClient(phone_number, api_id, api_hash)
    client.session.report_errors = False
    client.connect()

    message="successfully logged out"
    change=False
    context={"message":message}
    return render(request,"signout.html",context)
