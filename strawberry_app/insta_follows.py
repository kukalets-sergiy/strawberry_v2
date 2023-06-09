from instapy import InstaPy
from instapy import smart_run
import import insta_auth
import time

insta_username = ''
insta_password = ''
session = InstaPy(username=insta_username, password=insta_password)
with smart_run(session):
    delay = 600  
    session.set_action_delays(enabled=True, follow=delay, like=delay, unfollow=delay)

    session.set_do_follow(enabled=True, percentage=100)
    session.set_dont_like(['naked', 'nsfw'])
    session.set_ignore_users(['user1', 'user2', 'user3'])

    session.follow_user_followers(['114747490274679'], amount=20, randomize=False, sleep_delay=delay)

    for user in session.grab_following(username=insta_username):
        if user.username == 'target_username':
            print('You are following target_username')
            break
    else:
        print('You are not following target_username')
