import os
import logging

class FB(object):
    """
    Create Facebook Responses
    """

    def __init__ (self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("Facebook")
        self.logger.info("Initialized Facebook Class")

    def textMessage(self, text, speech=""):
        """
        Simple Text message Response
        """
        messages = []
        if speech:
            self.logger.info("Speech Response present")
            tempresp = {
                "type": 0,
                "speech": speech,
                "text": text
            }
        else:
            self.logger.info("No Speech Response")
            tempresp = {
                "type": 0,
                "text": text
            }

        messages.append(tempresp)
        response = {
            "messages" : messages
        }
        self.logger.info("Response : %s", response)
        return response

    def cardMessage(self, restaurant_list):
        """
        Facebook Cards Response
        """
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
        self.logger.info("Response : %s", response)
        return response
