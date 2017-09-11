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

    def textMessage(self, messages, text, speech=""):
        """
        Simple Text message Response
        """
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
                "speech": text
            }

        messages.append(tempresp)
        # response = {
        #     "messages" : messages
        # }
        # self.logger.info("Response : %s", response)
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
