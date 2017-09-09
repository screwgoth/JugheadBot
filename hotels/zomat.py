import os
import logging
import requests
import json


class Zomat(object):
    """
    Fetch data using the Zomato API
    """

    def __init__(self):
        self.logger = logging.getLogger("Zomat")
        self.logger.debug("Initialzing Zomat class")
        self.userKey = os.environ.get("USER_KEY")
        self.headers={"Accept":"application/json", "user-key": "b0fcc8e574f96ad3e80be23d898aa861"}
        #self.logger.debug("user-key = ", self.userKey)

    def getLocation(self, location):
        """
        Get Zomato entity_id and entity_type
        """
        search_url = "https://developers.zomato.com/api/v2.1/locations?query="+location
        search_resp=requests.get(search_url,headers=self.headers)
        search_resp_dict=json.loads(search_resp.text)
        loc_sug_list = search_resp_dict['location_suggestions']
        for loc_sug in loc_sug_list:
            entity_type = loc_sug["entity_type"]
            print (entity_type)
            entity_id = loc_sug["entity_id"]
            print (entity_id)
        return entity_id, entity_type

    def getBestRestaurants(self, entity_id, entity_type):
        restaurant_list = []
        zomato_url="https://developers.zomato.com/api/v2.1/search?entity_id="+str(entity_id)+"&entity_type="+str(entity_type)+"&count=5&sort=rating&order=desc"
        resp=requests.get(zomato_url,headers=self.headers)
        resp_dict=json.loads(resp.text)
        restaurants = (resp_dict['restaurants'])

        for i in restaurants:
            zomato_dict = {}
            zomato_dict['res_name'] = i['restaurant']['name']
            zomato_dict['res_addr'] = i['restaurant']['location']['address']
            zomato_dict['res_url'] = i['restaurant']['url']
            zomato_dict['res_photo'] = i['restaurant']['featured_image']
            zomato_dict['res_menu'] = i['restaurant']['menu_url']
            restaurant_list.append(zomato_dict)
        return restaurant_list
