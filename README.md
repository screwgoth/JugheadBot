JugheadBot
==========
This facebook-manual branch contains code which was used to figure out how Facebook Bots work, by doing everything manually, which means without using 3rd party platforms like API.AI or WIT.AI , etc.

Currently this code works with the Jughead - Test2 - API.ai (https://developers.facebook.com/apps/498060987194122/dashboard/) Facebook Messenger Test App.

It works as a Heroku App : https://jugheadbotapp.herokuapp.com/api/v1/hotels/
Some Heroku commands :
* heroku logs --tail
* git push heroku master
* git push heroku facebook-manual:master
* heroku config
