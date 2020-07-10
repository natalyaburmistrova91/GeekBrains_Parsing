# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstafolowerItem, InstafolowItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy


class InstagramSpider(scrapy.Spider):
    #атрибуты класса
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = '**'
    insta_pwd = '**'
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_users = ['veshkisport', 'if.not.model'] #Пользователи, у которых собираем подписчиков
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    followers_hash = 'c76146de99bb02f6415203be841dd25a'     #hash для получения данных по подписчиках с главной страницы
    follows_hash = 'd04b0a864b4b54837c0d870b0e77e076'  #hash для получения данных о подписках с главной страницы
    hashs = [followers_hash, follows_hash]

    def parse(self, response:HtmlResponse):             #Первый запрос на стартовую страницу
        csrf_token = self.fetch_csrf_token(response.text)   #csrf token забираем из html
        yield scrapy.FormRequest(                   #заполняем форму для авторизации
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username':self.insta_login, 'enc_password':self.insta_pwd},
            headers={'X-CSRFToken':csrf_token}
        )

    def user_parse(self, response:HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']: #Проверяем ответ после авторизации
            print("Авторизовались!")
            for parse_user in self.parse_users:
                yield response.follow(   #Переходим на желаемую страницу пользователя
                    f'/{parse_user}',
                    callback= self.user_data_parse,
                    cb_kwargs={'parse_user':parse_user}
                )


    def user_data_parse(self, response:HtmlResponse, parse_user):
        # Получаем id пользователя
        user_id = self.fetch_user_id(response.text, parse_user)
        # Формируем словарь для передачи даных в запрос
        variables={'id':user_id,
                   'include_reel': 'true',
                   'fetch_mutual': 'true',
                   'first':24}          #24 фоловера
        for types_follow in self.hashs:
            url_follow = f'{self.graphql_url}query_hash={types_follow}&{urlencode(variables)}'    #Формируем ссылку для получения данных о фоловерах
            yield response.follow(
                url_follow,
                callback=self.user_follow_parse,
                cb_kwargs={'parse_user':parse_user,
                           'user_id':user_id,
                           'variables':deepcopy(variables),
                           'types_follow':types_follow} #variables ч/з deepcopy во избежание гонок
        )

    def user_follow_parse(self, response:HtmlResponse,parse_user,user_id,variables,types_follow):   #Принимаем ответ. Не забываем про параметры от cb_kwargs
        j_data = json.loads(response.text)
        if types_follow == self.hashs[0]:
            page_info = j_data.get('data').get('user').get(f'edge_followed_by').get('page_info')
            if page_info.get('has_next_page'):      #Если есть следующая страница
                variables['after'] = page_info['end_cursor']  #Новый параметр для перехода на след. страницу
                url_follow = f'{self.graphql_url}query_hash={types_follow}&{urlencode(variables)}'
                yield response.follow(
                    url_follow,
                    callback=self.user_follow_parse,
                    cb_kwargs={'parse_user':parse_user,
                               'user_id': user_id,
                               'variables': deepcopy(variables),
                               'types_follow': types_follow}
                )
            followers = j_data.get('data').get('user').get('edge_followed_by').get('edges')     #Сами фолловеры
            for follower in followers:            #Перебираем фолловеров, собираем данные
                item = InstafolowerItem(
                    user_id = user_id,
                    username = parse_user,
                    follower_id = follower['node']['id'],
                    follower_username = follower['node']['username'],
                    follower_fullname = follower['node']['full_name'],
                    follower_photo = follower['node']['profile_pic_url']
                )
                yield item                  #В пайплайн
        else:
            page_info = j_data.get('data').get('user').get(f'edge_follow').get('page_info')
            if page_info.get('has_next_page'):  # Если есть следующая страница
                variables['after'] = page_info['end_cursor']  # Новый параметр для перехода на след. страницу
                url_follow = f'{self.graphql_url}query_hash={types_follow}&{urlencode(variables)}'
                yield response.follow(
                    url_follow,
                    callback=self.user_follow_parse,
                    cb_kwargs={'parse_user':parse_user,
                               'user_id': user_id,
                               'variables': deepcopy(variables),
                               'types_follow': types_follow}
                )
            followers = j_data.get('data').get('user').get('edge_follow').get('edges')  # Сами фолловеры
            for follower in followers:  # Перебираем фолловеров, собираем данные
                item = InstafolowItem(
                    user_id=user_id,
                    username=parse_user,
                    user_follow_id=follower['node']['id'],
                    user_follow_username=follower['node']['username'],
                    user_follow_fullname=follower['node']['full_name'],
                    user_follow_photo=follower['node']['profile_pic_url']
                )
                yield item  # В пайплайн

    #Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    #Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
