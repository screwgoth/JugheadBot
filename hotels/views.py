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
