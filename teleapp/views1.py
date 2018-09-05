from django.shortcuts import render
from django.http.response import HttpResponseRedirect
# Create your views here.
import asyncio
from telethon import TelegramClient
from telethon.tl.types import InputPeerChat
from telethon.tl.functions.contacts import ResolveUsernameRequest

from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.functions.channels import InviteToChannelRequest
import time
import csv
api_id=277999
api_hash = '0ae0a703c7a845b4a710b8581a92e7be'
phone_number='+919234566892'
global client 
global phone1
async def starter():
    global client
    client = TelegramClient(phone_number, api_id, api_hash)
    client.session.report_errors = False
    await client.connect()
global loop
loop = asyncio.new_event_loop()
def index(requests):
    context={}
    
    asyncio.set_event_loop(loop)
    loop.run_until_complete(starter())
    


    async def internal(requests):
        global client
        v=await client.is_user_authorized() 
        print(v)
        return v
    
    loop2=asyncio.get_event_loop()
    v=loop2.run_until_complete(internal(requests))
    
    if not v:
        return HttpResponseRedirect("login/")
    else:
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
    async def coderequest(phone):
        global client
        
        await client.send_code_request(phone)
        print(client,phone)
    # loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(coderequest(phone))
    
    return render(request,"otp.html",context)
def login(request):
    context={}
    
    return render(request,"login.html",context)
def otp(request):
    global phone1
    context={}
    print(phone1)
    async def otprequest(otp):
        global client
        await client.sign_in(phone1,otp)

    if request.method=='POST':
        otp_value=request.POST.get("otp")
    asyncio.set_event_loop(loop)
    loop.run_until_complete(otprequest(otp_value))
        
    return render(request,"otp.html",context)
def abc(request):
    context={}
    return render(request,"getmembers.html",context)

def getmembers(request):
    opp_gid=request.POST.get('groupid')
    # print(client.send_message(323950976,'hi hello'))
    olist=[]
    global client
    print(client)
    async def internal_getmembers(opp_gid):
        global client
        if opp_gid.isnumeric():
            ulist=await client.get_participants(int(opp_gid))
        else:
            ulist=await client.get_participants(opp_gid)
        print(ulist)
        # for u in ulist:
        #     olist.append(u.id)
    
    asyncio.set_event_loop(loop)
    loop.run_until_complete(internal_getmembers(opp_gid))

    context={"olist":olist}
    return render(request,"displaymembers.html",context)
