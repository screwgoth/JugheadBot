import os
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import json

# Create your views here.
@api_view(['GET'])
def test_api(request):
    print ("In test_api")
    tempresp= {
        "api" : "reached"
    }
    return Response(tempresp)

@api_view(['GET','POST'])
def handle_webhook(request):
    # get all Hotel Categories
    resp = "{Webhook}"
    PAGE_ACCESS_TOKEN=os.environ['PAGE_ACCESS_TOKEN']
    print (PAGE_ACCESS_TOKEN)
    facebook_url = "https://graph.facebook.com/v2.10/me/messages"
    if request.method == 'GET':
        print ("In webhook")
        print (request.query_params)
        if request.query_params['hub.mode'] == "subscribe" and request.query_params['hub.challenge']:
            print ("Facebook verification request")
            if request.query_params['hub.verify_token'] == os.environ['VERIFY_TOKEN']:
                print ("Token matched")
                resp = json.loads(request.query_params['hub.challenge'])
            else:
                print ("Verification token mismatched")
        else:
            print ("Not a Facebook verification")
        #body_unicode = request.body.decode('utf-8')
        #body = json.loads(body_unicode)
        #print (body)
        #resp = "{Done}"
        return Response(resp)
    if request.method == 'POST':
        print (request.body)
        body_unicode = request.body.decode('utf-8')
        incoming_message = json.loads(body_unicode)
        print (incoming_message)
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                print (message)
                if 'message' in message:
                    print (message)
                    sender_id = message['sender']['id']
                    recipient_id = message['recipient']['id']
                    message_text = message['message']['text']
                    print (sender_id, recipient_id, message_text)
                    headers={"Content-Type":"application/json"}
                    params={"access_token":PAGE_ACCESS_TOKEN}
                    data = json.dumps({"recipient":{"id":sender_id}, "message":{"text":"Wassup Yo"}})

                    status = requests.post(facebook_url,params=params,headers=headers,data=data)
                    print (status.status_code)
                    print (status.text)
                    resp = {
                        "text" : "Wassup Yo!",
                    }

        return Response(resp)
