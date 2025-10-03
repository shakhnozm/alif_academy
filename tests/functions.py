import requests

# Базовый URL Alif Shop API
base_url = "https://gw.alifshop.uz"


# Получение активных предложений
def get_active_items():
    response = requests.get(f"{base_url}/web/client/events/active")
    return response


# Получение подробной информации о товаре по slug
def get_item(item_slug: str):
    response = requests.get(f"{base_url}/web/client/moderated-offers/{item_slug}")
    return response


# Поиск товаров по названию (используется для нахождения slug / id)
def search_items(item_name: str):
    body = {"query": item_name}
    response = requests.post(f"{base_url}/web/client/search/full-text", json=body)
    return response


# Получение информации о корзине (и доставке)
def get_cart(cookie: str = None):
    if cookie is None:
        response = requests.get(f"{base_url}/web/client/cart/view-cart/duplicate")
    else:
        headers = {
            "Cookie": f"cart={cookie};"
        }
        response = requests.get(
            f"{base_url}/web/client/cart/view-cart/duplicate",
            headers=headers
        )
    return response


# Добавление товара в корзину
def add_to_cart(cookie: str, offer_id: str, condition_id: int, quantity: int = 1):
    headers = {
        "Cookie": f"cart={cookie};"
    }
    body = {
        "moderated_offer_id": offer_id,
        "condition_id": condition_id,
        "quantity": quantity
    }
    response = requests.post(
        f"{base_url}/web/client/cart/moderated-items",
        json=body,
        headers=headers
    )
    return response


#  Получение популярных товаров (/offers/v2)
def get_popular_offers():
    response = requests.get(f"{base_url}/web/client/offers/v2")
    return response


# Получение отзывов по offer_id
def get_reviews(offer_id: int):
    response = requests.get(f"{base_url}/web/client/{offer_id}/reviews")
    return response
