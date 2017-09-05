import os
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import json

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
        headers={"Accept":"applicaiton/json",
        "user-key": "b0fcc8e574f96ad3e80be23d898aa861"}
        search_url = "https://developers.zomato.com/api/v2.1/locations?query="+loc
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
        res_name = restaurants[0]['restaurant']['name']
        res_url = restaurants[0]['restaurant']['url']
        res_photo = restaurants[0]['restaurant']['featured_image']
        res_menu = restaurants[0]['restaurant']['menu_url']
        print (res_name, res_url, res_photo, res_menu)
        for restaurant in restaurants:
            name = restaurant['restaurant']['name']
            disp_cat += name + "\n "
        # tempresp= {
        #     "messages": [
        #                 {
        #                     "type": 0,
        #                     "speech": disp_cat
        #                 }
        #     ]
        # }
        tempresp = {
            "message":{
                "attachment": {
                    "type": "template",
                    "payload":{
                        "template_type":"generic",
                        "elements":[
                        {
                            "title":res_name,
                            "image_url": res_photo,
                            "subtitle":"A little about this Restaurant",
                            "default_action": {
                                "type": "web_url",
                                "url": res_url,
                                "webview_height_ratio": "tall"                            },
                            "buttons":[
                            {
                                "type":"web_url",
                                "url":res_menu,
                                "title":"Restaurant Menu"
                            }
                            ]
                        }
                        ]
                    } #payload
                } #attachment
            } #message
        }
        print (tempresp)
        return Response(tempresp)
