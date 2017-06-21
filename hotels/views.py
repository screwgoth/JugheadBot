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
    facebook_url = "https://graph.facebook.com/v2.6/me/messages"
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
                    PAGE_ACCESS_TOKEN=os.environ['PAGE_ACCESS_TOKEN']
                    headers={"Content-Type":"applicaiton/json"}
                    params={"access_token":PAGE_ACCESS_TOKEN}
                    data=response_msg = json.dumps({"recipient":{"id":recipient_id}, "message":{"text":"Wassup Yo'"}})

                    status = requests.post(facebook_url,params=params,headers=headers,data=data)
                    print (status.status_code)
                    print (status.text)

        return Response(resp)

@api_view(['GET','POST'])
def get_hotel_info(request):
    # get all Hotel Categories
    if request.method == 'GET':
        print (request.body)
        body_unicode = request.body.decode('utf-8')
        #body = json.loads(body_unicode)
        #print (body)
        zomato_url="https://developers.zomato.com/api/v2.1/categories"
        headers={"Accept":"applicaiton/json",
        "user-key": "b0fcc8e574f96ad3e80be23d898aa861"}
        resp=requests.get(zomato_url,headers=headers)
        print (resp.content)
        #print (resp.status_code)
        jresp=json.loads(resp.text)
        #print (resp.text)
        print (jresp)
        return Response(jresp)
    if request.method == 'POST':
        #https://developers.zomato.com/api/v2.1/search?entity_id=5&entity_type=city&count=5&sort=rating&order=desc
        print (request.body)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        city_json = body['result']['parameters']
        city = city_json['street-address']
        print (city)
        headers={"Accept":"applicaiton/json",
        "user-key": "b0fcc8e574f96ad3e80be23d898aa861"}
        #eid=5
        search_url = "https://developers.zomato.com/api/v2.1/locations?query="+city
        search_resp=requests.get(search_url,headers=headers)
        search_resp_dict=json.loads(search_resp.text)
        loc_sug_list = search_resp_dict['location_suggestions']
        for loc_sug in loc_sug_list:
            entity_type = loc_sug["entity_type"]
            print (entity_type)
            entity_id = loc_sug["entity_id"]
            print (entity_id)

        zomato_url="https://developers.zomato.com/api/v2.1/search?entity_id="+str(entity_id)+"&entity_type="+str(entity_type)+"&count=5&sort=rating&order=desc"
        resp=requests.get(zomato_url,headers=headers)
        resp_dict=json.loads(resp.text)
        restaurants = (resp_dict['restaurants'])
        disp_cat = ""
        for restaurant in restaurants:
            #print (restaurant)
            name = restaurant['restaurant']['name']
            #disp_cat += "\n".join(name)
            disp_cat += name + " "
        # for item in resp_dict:
        #     cat_list = resp_dict[item]
        #     print (cat_list)
        #     disp_cat = ""
        #     for cats in cat_list:
        #         categ = (cats['categories']['name'])
        #         disp_cat += categ + ' '
        #         print (disp_cat)
        tempresp= {
            "speech" : disp_cat,
            "displayText" : disp_cat,
            "source" : "Zomato"
        }
        return Response(tempresp)
