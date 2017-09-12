import os
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from hotels.zomat import Zomat
from hotels.fb import FB

@api_view(['GET','POST'])
def get_hotel_info(request):
    # get all Hotel Categories
    if request.method == 'GET':
        print (request.body)
        body_unicode = request.body.decode('utf-8')
        zomato_url="https://developers.zomato.com/api/v2.1/categories"
        headers={"Accept":"applicaiton/json",
        "user-key": "b0fcc8e574f96ad3e80be23d898aa861"}
        resp=requests.get(zomato_url,headers=headers)
        print (resp.content)
        jresp=json.loads(resp.text)
        print (jresp)
        return Response(jresp)
    if request.method == 'POST':
        print (request.body)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        fb = FB(body)
        if fb.isFacebook:
            print ("sender_id = ", fb.sender_id)
            print ("recipient_id = ", fb.recipient_id)
            fb.independantTextMessage(fb.sender_id, "I love Burgers !!!")
        loc_json = body['result']['parameters']
        if loc_json['geo-city']:
            city = loc_json['geo-city']
            loc = city
            print (city)
        if loc_json['any']:
            area = loc_json['any']
            print (area)
            loc = area + " " + loc
        zom = Zomat()
        entity_id, entity_type = zom.getLocation(str(loc))
        print ("entity_id = ",entity_id, ", entity_type = ", entity_type)

        restaurant_list = []
        restaurant_list = zom.getBestRestaurants(entity_id, entity_type)


        messages = []
        messages = fb.textMessage(messages, "Alrighty !! Fetching your list")
        messages = fb.cardMessage(messages, restaurant_list)
        response = {
            "messages" : messages
        }
        print(response)
        return Response(response)
