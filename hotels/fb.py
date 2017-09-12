import os
import logging
import requests
import json

class FB(object):
    """
    Create Facebook Responses
    """

    def __init__ (self, body):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("Facebook")
        self.logger.info("Initialized Facebook Class")
        self.source = body['originalRequest']['source']
        self.logger.info("%s", body)
        self.logger.info("Source is : %s", self.source)
        self.page_access_token = os.environ.get("PAGE_ACCESS_TOKEN")
        self.facebook_url = "https://graph.facebook.com/v2.10/me/messages"
        self.sender_id = 0
        self.recipient_id = 0

    def isFacebook (self):
        if self.source == "facebook":
            self.logger.info("Source IS facebook")
            self.sender_id = body['originalRequest']['sender']['id']
            self.recipient_id = body['originalRequest']['recipient']['id']
            return True
        else:
            self.logger.info("Source is NOT facebook")
        return False

    def independantTextMessage(self, senderId, text):
        headers = {"Content-Type":"application/json"}
        params = {"access_token":self.page_access_token}
        data = json.dumps({"recipient":{"id":senderId}, "message":{"text":text}})

        status = requests.post(self.facebook_url,params=params,headers=headers,data=data)
        self.logger.info("status_code = %s, status_text = %s", status.status_code, status.text)

    def textMessage(self, messages, text):
        """
        Simple Text message Response
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

        self.logger.info("Appended FB card messages")
        # response = {
        #     "messages" : messages
        # }
        # self.logger.info("Response : %s", response)
        return messages
