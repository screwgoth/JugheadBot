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
        # Reference independant FB message
        # if fb.isFacebook():
        #     fb.independantTextMessage(fb.sender_id, "I love Burgers !!!")

        query_json = body['result']['parameters']
        if query_json['geo-city']:
            city = query_json['geo-city']
            loc = city
            print (city)
        if query_json['area']:
            area = query_json['area']
            print (area)
            loc = area + " " + loc
        cuisine = str()
        if query_json['Cuisines']:
            cuisine = query_json['Cuisines']
            print (cuisine)
        zom = Zomat()
        entity_id, entity_type = zom.getLocation(str(loc))
        print ("entity_id = ",entity_id, ", entity_type = ", entity_type)

        restaurant_list = []
        if not cuisine:
            restaurant_list = zom.getBestRestaurants(entity_id, entity_type)
        else:
            cuisine_id = zom.getCuisineID(city, cuisine)
            if cuisine_id = 0:
                if fb.isFacebook():
                    fb.independantTextMessage(fb.sender_id, "Could not find Restaurants for your specific Cuisine. Could you maybe re-check the spelling and try again?")

            restaurant_list = zom.getBestRestaurants(entity_id, entity_type, cuisine_id)


        messages = []
        # Reference Text Message
        #messages = fb.textMessage(messages, "Alrighty !! Fetching your list")

        # Update FB Card message with Restaurant list
        messages = fb.cardMessage(messages, restaurant_list)

        # Reference Image Message
        #messages = fb.imageMessage(messages, "https://blog.magicpin.in/wp-content/uploads/2017/07/pizza.jpg")

        response = {
            "messages" : messages
        }
        print(response)
        return Response(response)
