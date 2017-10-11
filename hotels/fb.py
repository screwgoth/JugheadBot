import os
import logging
import requests
import json
from hotels.models import FBUser

class FB(object):
    """
    Create Facebook Responses
    """

    def __init__ (self, body):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("Facebook")
        self.body = body
        self.source = self.body['originalRequest']['source']
        self.logger.info("Source is : %s", self.source)
        self.page_access_token = os.environ.get("PAGE_ACCESS_TOKEN")
        self.facebook_message_url = "https://graph.facebook.com/v2.10/me/messages"
        self.facebook_user_url = "https://graph.facebook.com/v2.10/"
        self.sender_id = self.body['originalRequest']['data']['sender']['id']
        self.recipient_id = self.body['originalRequest']['data']['recipient']['id']
        self.userInfo = self.getUserInfo(self.sender_id)
        # self.logger.info("User Info:\n%s", self.userInfo)
        # fb_user = FBUser(
        #     first_name = self.userInfo['first_name'],
        #     last_name = self.userInfo['last_name'],
        #     #profile_pic = self.userInfo['profile_pic'],
        #     gender = self.userInfo['gender'],
        #     timezone = self.userInfo['timezone'],
        #     is_payment_enabled = self.userInfo['is_payment_enabled'],
        #     fb_userId = str(self.sender_id)
        #     )
        # fb_user.save_to_db()



    def isFacebook (self, senderID = 0):
        if self.source == "facebook":
            self.logger.info("Source IS facebook")
            if senderID == 0:
                self.sender_id = self.body['originalRequest']['data']['sender']['id']
            return True
        else:
            self.logger.info("Source is NOT facebook")
        return False

    def independantTextMessage(self, senderId, text):
        """
        Reference independant FB message
        if fb.isFacebook():
           fb.independantTextMessage(fb.sender_id, "I love Burgers !!!")
        """
        headers = {"Content-Type":"application/json"}
        params = {"access_token":self.page_access_token}
        data = json.dumps({"recipient":{"id":senderId}, "message":{"text":text}})

        status = requests.post(self.facebook_message_url,params=params,headers=headers,data=data)
        self.logger.info("status_code = %s, status_text = %s", status.status_code, status.text)

    def textMessage(self, messages, text):
        """
        Simple Text message Response
        Reference Text Message:
        messages = fb.textMessage(messages, "Alrighty !! Fetching your list")
        """
        self.logger.info("No Speech Response")
        tempresp = {
            "type": 0,
            "speech": text
        }
        messages.append(tempresp)
        self.logger.info("Appended FB Text messages")

        return messages

    def cardMessage(self, messages, restaurant_list):
        """
        Facebook Cards Response
        """

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
                                        "title": restaurant["fbcard_name"],
                                        "image_url": restaurant["fbcard_photo"],
                                        "subtitle": restaurant["fbcard_subtitle"],
                                        "default_action": {
                                                            "type": "web_url",
                                                            "url": restaurant["fbcard_url"],
                                                            "webview_height_ratio": "tall"
                                                          },
                                        "buttons": [
                                                    {
                                                        "type": "web_url",
                                                        "url": restaurant["button_url"],
                                                        "title": restaurant["button_title"]
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

        self.logger.info("Appended FB card messages")
        # response = {
        #     "messages" : messages
        # }
        # self.logger.info("Response : %s", response)
        return messages

    def imageMessage(self, messages, image_url = "" ):
        """
        Facebook Image card
        Reference Image Message:
        messages = fb.imageMessage(messages, "https://blog.magicpin.in/wp-content/uploads/2017/07/pizza.jpg")
        """
        if image_url == "":
            self.logger.info("No Image URL provided")
            return messages

        tempresp = {}
        tempresp = {
            "type": 4,
            "payload": {
                "facebook": {
                    "attachment": {
                        "type": "image",
                        "payload": {
                            "url": image_url
                        }
                    }
                }
            }
        }
        messages.append(tempresp)
        self.logger.info("Appended FB Image messages")
        return messages


    def getUserInfo(self, userID):
        """
        Get User info
        """
        first_name = "First Name"
        last_name = "Last Name"
        gender = "Not mentioned"
        timezone = "0.0"
        is_payment_enabled = False

        headers = {"Content-Type":"application/json"}
        fields = "first_name,last_name,profile_pic,timezone,gender,is_payment_enabled,last_ad_referral"
        params = {"fields": fields, "access_token":self.page_access_token}
        final_fb_url = self.facebook_user_url + userID
        self.logger.info("Final FB URL for user : %s", final_fb_url)
        status = requests.get(final_fb_url,params=params,headers=headers)
        self.logger.info("status_code = %s, status_text = %s", status.status_code, status.text)
        userInfo = json.loads(status.text)
        if 'first_name' in userInfo:
            first_name = userInfo['first_name']
        else:
            userInfo['first_name'] = first_name
        if 'last_name' in userInfo:
            last_name = userInfo['last_name']
        else:
            userInfo['last_name'] = last_name
        if 'gender' in userInfo:
            gender = userInfo['gender']
        else:
            userInfo['gender'] = gender
        if 'timezone' in userInfo:
            timezone = userInfo['timezone']
        else:
            userInfo['timezone'] = timezone
        if 'is_payment_enabled' in userInfo:
            is_payment_enabled = userInfo['is_payment_enabled']
        else:
            userInfo['is_payment_enabled'] = is_payment_enabled
        self.logger.info("User Info:\n%s", userInfo)
        fb_user = FBUser(
            first_name = first_name,
            last_name = last_name,
            gender = gender,
            timezone = timezone,
            is_payment_enabled = is_payment_enabled,
            fb_userId = str(userID)
            )
        fb_user.save_to_db()
        return userInfo
