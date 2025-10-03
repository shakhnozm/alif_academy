import requests

base_url = "https://gw.alifshop.uz/"


def get_active_items():
    response = requests.get(url=f"{base_url}/web/client/events/active")
    return response


def get_item(item_slug: str):
    response = requests.get(url=f"{base_url}/web/client/moderated-offers/{item_slug}")
    return response


def search_items(item_name: str):
    body = {
        "query": item_name
    }
    response = requests.post(url=f"{base_url}/web/client/search/full-text", json=body)
    return response


def get_cart(cookie=None):
    if cookie is None:
        response = requests.get(f"{base_url}/web/client/cart/view-cart/duplicate")
    else:
        headers = {
            'Cookie': f"cart={cookie};"
        }
        response = requests.get(
            url=f"{base_url}/web/client/cart/view-cart/duplicate",
            headers=headers
        )
    return response


def add_to_cart(cookie: str, offer_id: str, condition_id: int, quantity=1):
    headers = {
        'Cookie': f"cart={cookie};"
    }
    body = {
        "moderated_offer_id": offer_id,
        "condition_id": condition_id,
        "quantity": quantity
    }
    response = requests.post(
        url=f"{base_url}/web/client/cart/moderated-items",
        json=body,
        headers=headers
    )
    return response


def get_popular_offers():
    """Получение популярных офферов (страница популярных товаров)"""
    response = requests.get(url=f"{base_url}/web/client/offers/popular")
    return response


def get_reviews(item_slug: str):
    """Получение отзывов по товару (по слагу)"""
    response = requests.get(url=f"{base_url}/web/client/moderated-offers/{item_slug}/reviews")
    return response
