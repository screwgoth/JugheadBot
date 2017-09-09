import os
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from hotel.zomat import Zomat

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
            loc = loc_json['geo-city']
            print (loc)
        zom = Zomat()
        entity_id, entity_type = zom.getLocation(loc)
        print ("entity_id = ",entity_id, ", entity_type = ", entity_type)


        zomato_url="https://developers.zomato.com/api/v2.1/search?entity_id="+str(entity_id)+"&entity_type="+str(entity_type)+"&count=5&sort=rating&order=desc"
        resp=requests.get(zomato_url,headers=headers)
        resp_dict=json.loads(resp.text)
        restaurants = (resp_dict['restaurants'])
        elements1 = []
        restaurant_list = []
        for i in restaurants:
            zomato_dict = {}
            zomato_dict['res_name'] = i['restaurant']['name']
            zomato_dict['res_addr'] = i['restaurant']['location']['address']
            zomato_dict['res_url'] = i['restaurant']['url']
            zomato_dict['res_photo'] = i['restaurant']['featured_image']
            zomato_dict['res_menu'] = i['restaurant']['menu_url']
            restaurant_list.append(zomato_dict)

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
