import requests
import creds
from strawberry_app import urls


def create_session():
    s = requests.Session()  # session object
    s.headers.update(
        {
            # "X-Shopify-Access-Token": creds.token,
            "Content-Type": "application-json"
        }
    )
    return s


def main():
    sess = create_session()
    resp = sess.get(creds.url + "/q-саджанці-полуниці/?currency=UAH")
    # resp = sess.get(creds.url + "/admin/api/2023-04/products.json?limit=10")
    print(resp.json)


if __name__ == "__main__":
    main()


# 1. use a session object
# 2. add all headers that we want to be sent with every request to be made with the session
# 3. add all headers that we want to be sent with every request to be made with the session
# 4.
# 5.
