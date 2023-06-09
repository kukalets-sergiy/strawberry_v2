import insta_auth
from instagrapi import Client
from instagrapi.types import Usertag, Location
import time
import random
import os
from instagrapi.exceptions import ClientError

from django_strawberry import settings
import json

cl = Client()
cl.login(insta_auth.login, insta_auth.password)


class MakePost:
    def __init__(self, client):
        self.cl = client
        self.tags = ['#strawberry', '#summer', '#fantastic']
        self.used_pictures = []
        self.used_text = []
        self.picture_index = 0
        self.text_index = 0
        self.post_count = 0

    def get_current_time(self):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(current_time)
        return current_time


    def choice_text(self):
        text_list = []
        for root, dirs, files in os.walk('/home/sergiy/domains/strawberry/django_strawberry/Text'):
            if 'City_Attractions_From_CheapTrip.Guru' in root and any(file.endswith('.json') for file in files):
                text_list.extend(os.path.join(root, file) for file in files if file.endswith('.json'))

        if not text_list:
            raise FileNotFoundError('No files found in Text directory')

        if self.text_index >= len(text_list):
            self.text_index = 0

        with open(text_list[self.text_index], 'r') as f:
            data = json.load(f)
            tex = data['description']
        self.text_index += 1

        if tex in self.used_text:
            return self.choice_text()
        else:
            self.used_text.append(tex)
            return tex

    def choice_pictures(self):
        pic_list = []  # List to store the file paths
        for root, dirs, files in os.walk('/home/sergiy/domains/strawberry/django_strawberry/Pictures'):
            for file in files:
                if file.endswith('.jpg'):
                    pic_list.append(os.path.join(settings.MEDIA_ROOT,
                                                 os.path.relpath(os.path.join(root, file), settings.MEDIA_ROOT)))

        if not pic_list:
            raise FileNotFoundError('No pictures found in Pictures directory')

        pic = pic_list[self.picture_index]
        self.picture_index += 1

        if pic in self.used_pictures:
            return self.choice_pictures()
        else:
            self.used_pictures.append(pic)
            return pic

    def make_post(self, picture, max_posts=20):
        try:
            user = cl.user_info_by_username("kukalets2023")
            tags_list = random.sample(self.tags, 3)
            media = cl.photo_upload(
                path=picture,
                caption=f'{self.choice_text()} \n {" ".join(tags_list)}',  # description of the post
                usertags=[Usertag(user=user, x=0.5, y=0.5)],
                # location=Location(name='Ukraine, Mykolaiv', lat=46.68203973105657, lng=31.974916177311727),
                extra_data={
                    'custom_accessibility_caption': 'alt text example',
                    'like_and_view_counts_disabled': False,
                    'disable_comments': False,
                }
            )
            self.post_count += 1  
        except Exception as e:
            print(f"Error occurred while posting: {e}")

    def wait_for_time(self, max_posts=3):
        while self.post_count < max_posts:
            current_time = self.get_current_time()
            time_list = ['21:09:00', '20:28:00', '17:19:00']

            if current_time in time_list:
                pic = self.choice_pictures()
                self.make_post(pic)
                continue
            else:
                pass


start = MakePost(cl)
start.wait_for_time(3)




# autentification
# import os
# from datetime import datetime
# from pathlib import Path
#
# from django_strawberry.settings import BASE_DIR
# from strawberry_app import insta_auth
# from insta_auth import login, password
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# import time, random

# def login_firefox_chrome(_browser, login, password):
#     if _browser == "Chrome":
#         browser = webdriver.Chrome()
#     else:
#         browser = webdriver.Firefox()
#     browser.implicitly_wait(5)
#     browser.get('https://www.instagram.com')
#     time.sleep(random.randrange(2, 7))
#
#     _login = browser.find_element(By.NAME, "username")
#     _login.clear()
#     _login.send_keys(login)
#
#     time.sleep(random.randrange(1, 2))
#
#     _password = browser.find_element(By.NAME, "password")
#     _password.clear()
#     _password.send_keys(password)
#
#     time.sleep(random.randrange(1, 2))
#
#     _password.send_keys(Keys.ENTER)
#
#     time.sleep(250)


    # login_firefox_chrome("Chrome", login, password)





