# 4) Написать запрос к базе, который вернет список подписчиков только указанного пользователя
# 5) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь

from pymongo import MongoClient
from pprint import pprint


def followers_find(user):
    for fol in instagram.find({'$and':[{'username': user}, {'follower_id':{'$ne': None}}]}):
        pprint(fol)

def follows_find(user):
    for fol in instagram.find({'$and':[{'username': user}, {'user_follow_id':{'$ne': None}}]}):
        pprint(fol)


user = 'if.not.model'
client = MongoClient('localhost', 27017)
db = client['insta_scrapy']
instagram = db.instagram


## Примеры вывода:

#followers_find(user)

# {'_id': ObjectId('5efa53cf3055bcbf26afebe8'),
#  'follower_fullname': 'Эдуард',
#  'follower_id': '1674214866',
#  'follower_photo': 'https://scontent-arn2-1.cdninstagram.com/v/t51.2885-19/s150x150/60858618_408835943036405_282035985338859520_n.jpg?_nc_ht=scontent-arn2-1.cdninstagram.com&_nc_ohc=Z321MWEoXGAAX8SqK4-&oh=ad83b032aa9de229060a30af63410bfc&oe=5F241894',
#  'follower_username': 'serioussam5',
#  'user_id': '609617068',
#  'username': 'if.not.model'}

#follows_find(user)

# {'_id': ObjectId('5efa55f13055bcbf26aff8c0'),
#  'user_follow_fullname': 'Gina',
#  'user_follow_id': '364942235',
#  'user_follow_photo': 'https://scontent-arn2-1.cdninstagram.com/v/t51.2885-19/s150x150/101980054_626999317900501_7036181504084788855_n.jpg?_nc_ht=scontent-arn2-1.cdninstagram.com&_nc_ohc=PgAhPdRIeegAX_iTooe&oh=6f6c91a04e8fa76cb0e9d540f34d6bad&oe=5F2223E6',
#  'user_follow_username': 'ginasabai',
#  'user_id': '609617068',
#  'username': 'if.not.model'}

