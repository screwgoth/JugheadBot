import os
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from hotels.zomat import Zomat

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
        loc_json = body['result']['parameters']
        if loc_json['geo-city']:
            city = loc_json['geo-city']
            loc = city
            print (city)
        if loc_json['any']:
            area = loc_json['any']
            print (area)
            loc = loc + " " + area
        zom = Zomat()
        entity_id, entity_type = zom.getLocation(loc)
        print ("entity_id = ",entity_id, ", entity_type = ", entity_type)

        restaurant_list = []
        restaurant_list = zom.getBestRestaurants(entity_id, entity_type)


        # tempresp= {
        #     "messages": [
        #                 {
        #                     "type": 0,
        #                     "speech": disp_cat
        #                 }
        #     ]
        # }

        messages = []

        for restaurant in restaurant_list:
            tempresp = {}
            tempresp = {
                "type": 4,
                "payload": {
                    "facebook": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                                "template_type": "generic",
                                "elements": [
                                    {
                                        "title": restaurant["res_name"],
                                        "image_url": restaurant["res_photo"],
                                        "subtitle": restaurant["res_addr"],
                                        "default_action": {
                                                            "type": "web_url",
                                                            "url": restaurant["res_url"],
                                                            "webview_height_ratio": "tall"
                                                          },
                                        "buttons": [
                                                    {
                                                        "type": "web_url",
                                                        "url": restaurant["res_menu"],
                                                        "title": "Restaurant Menu"
                                                    }
                                                    ]
                                    }
                                ]
                            }
                        }
                    }
                }
            }
            messages.append(tempresp)

        response = {
            "messages" : messages
        }
        print (response)
        return Response(response)
