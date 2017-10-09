import os
import logging
import requests
import json


class Zomat(object):
    """
    Fetch data using the Zomato API
    """

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("Zomat")
        self.userKey = os.environ.get("USER_KEY")
        self.headers = {"Accept":"application/json", "user-key": self.userKey}

    def getLocation(self, location):
        """
        Get Zomato entity_id and entity_type
        """
        entity_id = 0
        entity_type = str()
        self.logger.info("Looking up for location : %s", location)
        search_url = "https://developers.zomato.com/api/v2.1/locations?query="+location
        search_resp = requests.get(search_url,headers=self.headers)
        search_resp_dict = json.loads(search_resp.text)
        loc_sug_list = search_resp_dict['location_suggestions']
        for loc_sug in loc_sug_list:
            entity_type = loc_sug["entity_type"]
            entity_id = loc_sug["entity_id"]
            if entity_id and entity_type:
                self.logger.info("entity_id = %d, entity_type = %s", entity_id, entity_type)
        return entity_id, entity_type

    def getBestRestaurants(self, entity_id, entity_type, cuisine_id = 0):
        restaurant_list = []
        if cuisine_id == 0:
            self.logger.info("No specific cuisine")
            zomato_url = "https://developers.zomato.com/api/v2.1/search?entity_id="+str(entity_id)+"&entity_type="+str(entity_type)+"&count=5&sort=rating&order=desc"
        else:
            self.logger.info("Finding Restaurants as per cuisines")
            zomato_url = "https://developers.zomato.com/api/v2.1/search?entity_id="+str(entity_id)+"&entity_type="+str(entity_type)+"&count=5&radius=5000&cuisines="+str(cuisine_id)+"&sort=rating&order=desc"
        resp = requests.get(zomato_url,headers=self.headers)
        resp_dict = json.loads(resp.text)
        restaurants = (resp_dict['restaurants'])
        print ("Top 5 restaurants : ",restaurants)

        for i in restaurants:
            zomato_dict = {}
            zomato_dict['fbcard_name'] = i['restaurant']['name']
            zomato_dict['fbcard_subtitle'] = i['restaurant']['location']['address']
            zomato_dict['fbcard_url'] = i['restaurant']['url']
            zomato_dict['fbcard_photo'] = i['restaurant']['featured_image']
            zomato_dict['button_url'] = i['restaurant']['menu_url']
            zomato_dict['button_title'] = "Restaurant Menu"
            restaurant_list.append(zomato_dict)
        return restaurant_list

    def getCityID(self, city):
        """
        Get Zomato ID and other info for a City
        """
        city_id = 0
        zomato_url = "https://developers.zomato.com/api/v2.1/cities?q="+city
        resp = requests.get(zomato_url,headers=self.headers)
        resp_dict = json.loads(resp.text)
        # Assuming there is only one entry for this City
        city_id = resp_dict['location_suggestions'][0]['id']
        self.logger.info("For City : %s, got city_id = %d", city, city_id)
        return city_id

    def getCuisineID(self, city, cuisine):
        """
        Get the Zomate Cuisine ID
        """
        city_id = self.getCityID(city)
        if city_id != 0:
            zomato_url = "https://developers.zomato.com/api/v2.1/cuisines?city_id="+str(city_id)
            resp = requests.get(zomato_url,headers=self.headers)
            resp_dict = json.loads(resp.text)
            cusines = (resp_dict['cuisines'])
            for zcuisine in cusines:
                if cuisine.lower() == zcuisine['cuisine']['cuisine_name'].lower():
                    self.logger.info("For Cuisine : %s, cuisine_id = %d", cuisine, zcuisine['cuisine']['cuisine_id'])
                    return zcuisine['cuisine']['cuisine_id']

        # Cuisine not found
        self.logger.info("Cuisine, %s, not found for city %s", cuisine, city)
        return 0

    def getReviews(self, res_name, entity_id = 0, entity_type = ""):
        """
        Get the review for the specified Restaurant
        """
        self.logger.info("Restaurant review for : %s", res_name)
        res_review = []
        res_id = 0
        if entity_id == 0 and not entity_type:
            zomato_url = "https://developers.zomato.com/api/v2.1/search?q="+res_name
        else:
            zomato_url = "https://developers.zomato.com/api/v2.1/search?entity_id="+str(entity_id)+"&entity_type="+entity_type+"&q="+res_name

        resp = requests.get(zomato_url,headers=self.headers)
        resp_dict = json.loads(resp.text)
        restaurants = (resp_dict['restaurants'])
        #print ("Found restaurants : ",restaurants)

        for r in restaurants:
            print (r['restaurant']['name'])
            # Sometimes the queries will contains results where the Restaurant
            # name is part of the address. So check specifically for the name
            if res_name == r['restaurant']['name']:
                zomato_dict = {}
                res_id = r['restaurant']['R']['res_id']
                self.logger.info("For %s, Restaurant ID = %d", res_name, res_id)
                zomato_dict['fbcard_name'] = r['restaurant']['name']
                zomato_dict['fbcard_subtitle'] = "Votes : " + str(r['restaurant']['user_rating']['votes']) + "\n" + "Average Cost for Two : " + str(r['restaurant']['average_cost_for_two'])
                zomato_dict['fbcard_url'] = r['restaurant']['url']
                zomato_dict['fbcard_photo'] = r['restaurant']['featured_image']
                menu_url = r['restaurant']['menu_url']
                review_url = menu_url.replace("menu", "reviews", 1)
                #self.logger.info("Review URL = %s", review_url)
                zomato_dict['button_url'] = review_url
                zomato_dict['button_title'] = "Rating: " + r['restaurant']['user_rating']['aggregate_rating'] + "/5 (" + r['restaurant']['user_rating']['rating_text'] + ")"
                res_review.append(zomato_dict)

        return res_review
