import pytest
from utils.mainpage.api import (
    get_active_items,
    get_item,
    get_popular_offers,
    get_reviews,
    get_cart
)


# ✅ /web/client/events/active
def test_get_active_items():
    resp = get_active_items()
    assert resp.status_code == 200, f"Статус-код не 200, а {resp.status_code}"

    data = resp.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    if data:
        first_event = data[0]
        assert "id" in first_event, "Нет ключа id у события"
        assert "offers" in first_event, "Нет ключа offers у события"
        assert isinstance(first_event["offers"], list), "offers должен быть списком"

        if first_event["offers"]:
            first_offer = first_event["offers"][0]
            assert "name" in first_offer, "Нет ключа name у первого оффера"


# ✅ /web/client/moderated-offers/{slug} — slug получаем динамически
def test_get_item():
    active_items = get_active_items().json()
    slug = None
    for event in active_items:
        for offer in event.get("offers", []):
            if offer.get("slug"):
                slug = offer["slug"]
                break
        if slug:
            break

    if not slug:
        pytest.skip("Нет slug для проверки get_item")

    resp = get_item(slug)
    assert resp.status_code == 200, f"Статус-код не 200, а {resp.status_code}"
    data = resp.json()
    assert isinstance(data, dict), "Ответ должен быть словарём"
    assert "id" in data or "slug" in data, "Некорректная структура ответа get_item"


# ✅ /web/client/offers/popular
def test_get_popular_offers():
    resp = get_popular_offers()
    assert resp.status_code == 200, f"Статус-код не 200, а {resp.status_code}"
    data = resp.json()

    assert isinstance(data, list), "Ответ должен быть списком"
    if data:
        offer = data[0]
        assert "id" in offer or "slug" in offer, "Нет ключа id или slug у популярного оффера"


# ✅ /{id}/reviews — offer_id динамически (active -> popular fallback)
def test_offer_reviews_structure():
    offer_id = next(
        (
            offer.get("offer_id")
            for event in get_active_items().json()
            for offer in event.get("offers", [])
            if offer.get("offer_id")
        ),
        None
    )

    if not offer_id:
        popular = get_popular_offers().json()
        if popular and "id" in popular[0]:
            offer_id = popular[0]["id"]

    if not offer_id:
        pytest.skip("Нет offer_id для проверки отзывов")

    resp = get_reviews(offer_id)
    assert resp.status_code == 200, f"Статус-код не 200, а {resp.status_code}"

    data = resp.json()
    assert "offer_reviews" in data, "Нет ключа 'offer_reviews'"
    assert isinstance(data["offer_reviews"], list), "'offer_reviews' должен быть списком"


# ✅ /web/client/cart
@pytest.mark.parametrize("cookie", [None])
def test_get_cart(cookie):
    resp = get_cart(cookie)
    assert resp.status_code == 200, f"Статус-код не 200, а {resp.status_code}"

    data = resp.json()
    assert isinstance(data, dict), "Ответ корзины должен быть словарём"
    assert "items" in data, "В ответе нет ключа 'items'"
    assert isinstance(data["items"], list), "'items' должен быть списком"
