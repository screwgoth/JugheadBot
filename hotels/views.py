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
        #print ("================== Zomato Response Python Dict =============")
        #print (resp_dict)
        restaurants = (resp_dict['restaurants'])
        #print ("================== Zomato Response  - Restaurants ===============")
        #print (restaurants)
        disp_cat = ""
        elements1 = []
        sample_list = []
        for i in restaurants:
            zomato_dict = {}
            zomato_dict['res_name'] = i['restaurant']['name']
            zomato_dict['res_addr'] = i['restaurant']['location']['address']
            zomato_dict['res_url'] = i['restaurant']['url']
            zomato_dict['res_photo'] = i['restaurant']['featured_image']
            zomato_dict['res_menu'] = i['restaurant']['menu_url']
            sample_list.append(zomato_dict)



        # tempresp= {
        #     "messages": [
        #                 {
        #                     "type": 0,
        #                     "speech": disp_cat
        #                 }
        #     ]
        # }
        # tempresp = {
        #     "messages": [
        #     {
        #         "type": 4,
        #         "payload": {
        #         "facebook" : {
        #         "attachment": {
        #             "type": "template",
        #             "payload":{
        #                 "template_type":"generic",
        #                 "elements":[
        #                 {
        #                     "title":res_name,
        #                     "image_url": res_photo,
        #                     "subtitle": res_addr,
        #                     "default_action": {
        #                         "type": "web_url",
        #                         "url": res_url,
        #                         "webview_height_ratio": "tall"                            },
        #                     "buttons":[
        #                     {
        #                         "type":"web_url",
        #                         "url":res_menu,
        #                         "title":"Restaurant Menu"
        #                     }
        #                     ]
        #                 }
        #                 ]
        #             } #payload
        #         } #attachment
        #         } # facebook
        #         } #payload
        #     }
        #     ] #messages
        # }
        # tempresp = {
        #     "messages" : [
        #         {
        #             "type": 1,
        #             "title": res_name,
        #             "subtitle": res_addr,
        #             "buttons": [
        #             {
        #                 "text" : "More Info",
        #                 "postback" : res_url
        #             }
        #             ]
        #         }
        #     ]
        # }
        for restaurant in sample_list:
            tempresp = {}
            tempresp["messages"] = [
            {
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
            ]
            print (tempresp)
            elements1.append(tempresp)
        return Response(elements1)
