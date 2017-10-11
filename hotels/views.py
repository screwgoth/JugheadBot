import os
from time import sleep
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from hotels.zomat import Zomat
from hotels.fb import FB
from hotels.models import Postbacks

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
        zom = Zomat()
        loc = str("Pune")
        entity_id = 0
        cuisine_id = 0
        entity_type = str()

        query_json = body['result']['parameters']
        #try:
        if 'postback' in body['originalRequest']['data']:
        #if body['originalRequest']['data']['postback']['payload']:
            fb_rating = Postbacks(
                first_name=fb.userInfo['first_name'],
                last_name=fb.userInfo['last_name'],
                gender=fb.userInfo['gender'],
                postback=str(body['originalRequest']['data']['postback']['payload']),
                fb_userId=str(fb.sender_id)
            )
            fb_rating.save_to_db()
            postback = body['originalRequest']['data']['postback']['payload']
            handle_postback(postback, fb)
            # if "NEW_USER_STARTED" in body['originalRequest']['data']['postback']['payload']:
            #     fb.independantTextMessage(fb.sender_id, "Hey there, Foodie !!! I'm JugheadBot, your friendly neighbourhood Restaurant finding Bot")
            #     sleep(1)
            #     fb.independantTextMessage(fb.sender_id, "You can ask me following questions:")
            #     fb.independantTextMessage(fb.sender_id, "\"Which are the best Restaurants in Kothrud, Pune\"")
            #     sleep(1)
            #     fb.independantTextMessage(fb.sender_id, "\"Which are the best Chinese Restaurants in Dadar, Mumbai\"")
            #     sleep(1)
            #     fb.independantTextMessage(fb.sender_id, "\"What is the review of Blue Nile in Camp Area, Pune\"")
            #     sleep(1)
            # elif "HELP_TEXT" in body['originalRequest']['data']['postback']['payload']:
            #     fb.independantTextMessage(fb.sender_id, "Currently, I understand only the following 3 types of questions")
            #     fb.independantTextMessage(fb.sender_id, "\"Which are the best Restaurants in Kothrud, Pune\"")
            #     sleep(1)
            #     fb.independantTextMessage(fb.sender_id, "\"Which are the best Chinese Restaurants in Dadar, Mumbai\"")
            #     sleep(1)
            #     fb.independantTextMessage(fb.sender_id, "\"What is the review of Blue Nile in Camp Area, Pune\"")
            #     sleep(1)
            #     fb,independantTextMessage(fb.sender_id, "And PLEASE remember to specify the Area AND City. For example: \"Manhattan, New York\" or \"Dadar, Mumbai\"")
            #     sleep(1)
            # else:
            #     fb.independantTextMessage(fb.sender_id, "Thanks !! I'll let Raseel know how much you liked me !!")
            return Response("{}")
        # except:
        #         # Not a Postback, so continue
        #         print("Not a Postback, so continue")
        #         pass

        if 'geo-city' in query_json:
            city = query_json['geo-city']
            loc = city
            print (city)
        if 'area' in query_json:
            area = query_json['area']
            print (area)
            loc = area + " " + loc
        entity_id, entity_type = zom.getLocation(str(loc))
        print ("entity_id = ",entity_id, ", entity_type = ", entity_type)

        messages = []
        restaurant_list = []

        if "Cuisines" in query_json:
            cuisine = str()
            cuisine = query_json['Cuisines']
            print (cuisine)
            cuisine_id = zom.getCuisineID(city, cuisine)
            print("cuisine_id = ", cuisine_id)
            if int(cuisine_id) == 0:
                messages = fb.textMessage(messages, "Could not find Restaurants for your specific Cuisine. Could you maybe re-check the spelling and try again?")
            else:
                restaurant_list = zom.getBestRestaurants(entity_id, entity_type, cuisine_id)
                # Update FB Card message with Restaurant list
                messages = fb.cardMessage(messages, restaurant_list)
        elif "res-name" in query_json:
            print ("This is a query for a Review")
            res_name = query_json['res-name']
            print (res_name)
            restaurant_review = zom.getReviews(res_name, entity_id, entity_type)
            messages = fb.cardMessage(messages, restaurant_review)
        else:
            # Just get the Top 5 Restaurants in the location
            restaurant_list = zom.getBestRestaurants(entity_id, entity_type)
            messages = fb.cardMessage(messages, restaurant_list)

        response = {
            "messages" : messages
        }
        print(response)
        return Response(response)


def handle_postback(postback, fb):
    """
    Handle the postback
    """
    if "NEW_USER_STARTED" in postback:
        greeting_message = "Hello " + fb.userInfo['first_name'] + ", I'm JugheadBot, your friendly neighbourhood Restaurant finding Bot"
        fb.independantTextMessage(fb.sender_id, greeting_message)
        help_message(fb)
    elif "HELP_TEXT" in postback:
        help_message(fb)
    elif "LIKED_JUGHEADBOT" in postback:
        fb.independantTextMessage(fb.sender_id, "Thanks !! I'll let Raseel know how much you liked me !!")
    elif "INTERESTED_IN_JUGHEADBOT" in postback:
        fb.independantTextMessage(fb.sender_id, "Hmm ... I'll try my best to be more helpful and entertaining")
    elif "BORED_WITH_JUGHEADBOT" in postback:
        fb.independantTextMessage(fb.sender_id, "That's too bad :-( But hey, don't blame me, Raseel's the one who's made me Boring")
    else:
        fb.independantTextMessage(fb.sender_id, "I Live to Eat")


def help_message(fb):
    """
    Help for JugheadBot
    """
    fb.independantTextMessage(fb.sender_id, "Currently, I understand only the following 3 types of questions")
    sleep(2)
    fb.independantTextMessage(fb.sender_id, "Best Restaurants : \"Which are the best Restaurants in Kothrud, Pune\"")
    sleep(2)
    fb.independantTextMessage(fb.sender_id, "Best Restaurants by Cuisine : \"Which are the best Chinese Restaurants in Dadar, Mumbai\"")
    sleep(2)
    fb.independantTextMessage(fb.sender_id, "Reviews for a specific Restaurant : \"What is the review of Blue Nile in Camp Area, Pune\"")
    sleep(2)
    fb.independantTextMessage(fb.sender_id, "PLEASE REMEMBER to specify an Area and City. For example : \"Gomti Nagar, Lucknow\" or \"Mahim, Mumbai\" or \"Kothrud, Pune\"")
