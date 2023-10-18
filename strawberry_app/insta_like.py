from instagrapi import Client
import insta_auth
import time
import random


cl = Client()
cl.login(insta_auth.login, insta_auth.password)


class LikePosts:
    def __init__(self, client):
        self.cl = client
        self.tags = ["Mykolaiv"]  # , 'Nikolaev', 'Niko', 'Миколаїв', 'Николаев', 'Ніко']
        self.liked_medias = []
        self.elapsed_time = 0

    def wait_time(self, delay):
        time.sleep(delay)

    def get_post_id(self):
        while True:
            try:
                medias = cl.hashtag_medias_recent(random.choice(self.tags), amount=1)
                media_dict = medias_dict = medias[0].dict()
                return str(media_dict["id"])
            except (IndexError, TypeError):
                print("Couldn't get post ID, retrying...")
                continue
            except Exception as e:
                print(f"Unknown error: {str(e)}")
                break

    def like_post(self, amount):
        tag = random.choice(self.tags)
        medias = self.cl.hashtag_medias_recent(tag, amount=amount)
        for media in medias:
            media_id = media.dict()["id"]
            if media_id in self.liked_medias:
                continue
            try:
                self.cl.media_like(media_id)
                self.liked_medias.append(media_id)
                random_delay = random.randint(60, 240)
                self.elapsed_time += random_delay
                print(
                    f"Liked {len(self.liked_medias)} posts, time elapsed {self.elapsed_time / 60}, now waiting for "
                    f"{random_delay}"
                )
                self.wait_time(random_delay)
            except (IndexError, TypeError):
                print("Couldn't like the post")
                continue
            except Exception as e:
                print(f"Unknown error: {str(e)}")
                break


start = LikePosts(cl)
start.like_post(599)
