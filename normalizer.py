from datetime import datetime, timezone
import json


def normalize_product(raw_data: dict) -> dict:
    now = datetime.now(timezone.utc).isoformat()

    product = dict(raw_data)

    # Identity
    product["product_id"] = str(
        product.get("product_id", "")
    )

    product["source"] = "shopee_affiliate_datafeed"
    product["market"] = product.get("market", "SG")

    # Product
    product_data = product.get("product", {})

    product_data["title"] = str(
        product_data.get("title", "")
    ).strip()

    product_data["brand"] = str(
        product_data.get("brand", "")
    ).strip()

    product_data["category_l1"] = str(
        product_data.get("category_l1", "")
    ).strip()

    product_data["category_l2"] = str(
        product_data.get("category_l2", "")
    ).strip()

    product_data["category_l3"] = str(
        product_data.get("category_l3", "")
    ).strip()

    product["product"] = product_data

    # Commerce
    commerce = product.get("commerce", {})

    for field in [
        "price",
        "sale_price",
        "discount_percentage",
        "item_rating"
    ]:
        try:
            commerce[field] = float(
                commerce.get(field, 0)
            )
        except (TypeError, ValueError):
            commerce[field] = 0

    for field in [
        "item_sold",
        "like_count",
        "stock"
    ]:
        try:
            commerce[field] = int(
                float(commerce.get(field, 0))
            )
        except (TypeError, ValueError):
            commerce[field] = 0

    commerce["currency"] = commerce.get(
        "currency",
        "SGD"
    )

    product["commerce"] = commerce

    # Shop
    shop = product.get("shop", {})

    shop["shop_name"] = str(
        shop.get("shop_name", "")
    ).strip()

    shop["seller_name"] = str(
        shop.get("seller_name", "")
    ).strip()

    for field in [
        "shop_rating"
    ]:
        try:
            shop[field] = float(
                shop.get(field, 0)
            )
        except (TypeError, ValueError):
            shop[field] = 0

    for field in [
        "shop_sku_count"
    ]:
        try:
            shop[field] = int(
                float(shop.get(field, 0))
            )
        except (TypeError, ValueError):
            shop[field] = 0

    product["shop"] = shop

    # Attributes
    attributes = product.get(
        "attributes",
        {}
    )

    if not isinstance(
        attributes.get(
            "global_item_attributes",
            []
        ),
        list
    ):
        attributes["global_item_attributes"] = []

    if not isinstance(
        attributes.get("model_ids", []),
        list
    ):
        attributes["model_ids"] = []

    if not isinstance(
        attributes.get("model_prices", []),
        list
    ):
        attributes["model_prices"] = []

    product["attributes"] = attributes

    # AI Analysis
    ai_analysis = product.get(
        "ai_analysis",
        {}
    )

    for field in [
        "benefits",
        "selling_points",
        "hook_angles",
        "demo_angles",
        "problem_solution_angles"
    ]:
        if not isinstance(
            ai_analysis.get(field, []),
            list
        ):
            ai_analysis[field] = []

    product["ai_analysis"] = ai_analysis

    # Scores
    scores = product.get(
        "scores",
        {}
    )

    for field in [
        "demand",
        "content",
        "visual",
        "problem",
        "impulse",
        "price",
        "competition",
        "total"
    ]:
        try:
            scores[field] = float(
                scores.get(field, 0)
            )
        except (TypeError, ValueError):
            scores[field] = 0

    product["scores"] = scores

    # System
    system = product.get(
        "system",
        {}
    )

    system["status"] = "normalized"
    system["updated_at"] = now

    if not system.get("created_at"):
        system["created_at"] = now

    product["system"] = system

    return product


if __name__ == "__main__":

    with open(
        "products.json",
        "r",
        encoding="utf-8"
    ) as file:

        products = json.load(file)

    normalized_products = [
        normalize_product(product)
        for product in products
    ]

    with open(
        "normalized_products.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            normalized_products,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("=== NORMALIZER ===")
    print(
        "Products normalized:",
        len(normalized_products)
    )
    print(
        "Output:",
        "normalized_products.json"
    )
