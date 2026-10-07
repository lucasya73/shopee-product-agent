import csv
import json
import sys
from datetime import datetime


def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0


def to_int(value):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def to_bool(value):
    if isinstance(value, bool):
        return value

    return str(value).strip().lower() in {
        "true",
        "1",
        "yes"
    }


def split_list(value):
    if not value:
        return []

    if isinstance(value, list):
        return value

    return [
        item.strip()
        for item in str(value).split(",")
        if item.strip()
    ]


def create_product_record(row, source_file=""):
    now = datetime.utcnow().isoformat()

    item_id = str(row.get("itemid", "")).strip()
    shop_id = str(row.get("shopid", "")).strip()

    return {
        "product_id": item_id,

        "source": "shopee_affiliate_datafeed",

        "market": "SG",

        "identity": {
            "item_id": item_id,
            "shop_id": shop_id,
            "product_url": row.get("product_link", ""),
            "affiliate_url": row.get("product_short link", "")
        },

        "product": {
            "title": row.get("title", ""),
            "model_names": row.get("model_names", ""),
            "description": row.get("description", ""),
            "condition": row.get("condition", ""),
            "brand": row.get("global_brand", ""),
            "category_l1": row.get("global_category1", ""),
            "category_l2": row.get("global_category2", ""),
            "category_l3": row.get("global_category3", ""),
            "category_id_l1": row.get("global_catid1", ""),
            "category_id_l2": row.get("global_catid2", ""),
            "category_id_l3": row.get("global_catid3", "")
        },

        "commerce": {
            "price": to_float(row.get("price")),
            "sale_price": to_float(row.get("sale_price")),
            "discount_percentage": to_float(
                row.get("discount_percentage")
            ),
            "item_sold": to_int(row.get("item_sold")),
            "item_rating": to_float(row.get("item_rating")),
            "like_count": to_int(row.get("like")),
            "stock": to_int(row.get("stock")),
            "currency": "SGD"
        },

        "shop": {
            "shop_name": row.get("shop_name", ""),
            "seller_name": row.get("seller_name", ""),
            "shop_rating": to_float(row.get("shop_rating")),
            "shop_sku_count": to_int(
                row.get("shop_sku_count")
            ),
            "is_official_shop": to_bool(
                row.get("is_official_shop")
            ),
            "is_preferred_shop": to_bool(
                row.get("is_preferred_shop")
            ),
            "shopee_verified_flag": row.get(
                "shopee_verified_flag",
                ""
            ),
            "has_lowest_price_guarantee": to_bool(
                row.get("has_lowest_price_guarantee")
            )
        },

        "media": {
            "image": row.get("image_link", ""),
            "image_2": "",
            "image_3": row.get("image_link_3", ""),
            "image_4": row.get("image_link_4", ""),
            "image_5": row.get("image_link_5", ""),
            "additional_images": split_list(
                row.get("additional_image_link", "")
            )
        },

        "attributes": {
            "global_item_attributes": split_list(
                row.get("global_item_attributes", "")
            ),
            "model_ids": split_list(
                row.get("model_ids", "")
            ),
            "model_prices": split_list(
                row.get("model_prices", "")
            )
        },

        "ai_analysis": {
            "target_customer": "",
            "use_case": "",
            "pain_point": "",
            "benefits": [],
            "selling_points": [],
            "hook_angles": [],
            "demo_angles": [],
            "problem_solution_angles": [],
            "visual_potential": 0,
            "content_potential": 0,
            "impulse_potential": 0
        },

        "scores": {
            "demand": 0,
            "content": 0,
            "visual": 0,
            "problem": 0,
            "impulse": 0,
            "price": 0,
            "competition": 0,
            "total": 0
        },

        "system": {
            "status": "raw",
            "source_file": source_file,
            "created_at": now,
            "updated_at": now
        }
    }


def collect_products(csv_file, limit=None):
    products = []

    with open(
        csv_file,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            products.append(
                create_product_record(
                    row,
                    source_file=csv_file
                )
            )

            if limit and len(products) >= limit:
                break

    return products


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(
            "Usage: python csv_collector.py "
            "<csv_file> [limit]"
        )
        sys.exit(1)

    csv_file = sys.argv[1]

    limit = None

    if len(sys.argv) >= 3:
        limit = int(sys.argv[2])

    try:
        products = collect_products(
            csv_file,
            limit
        )

        print("=== CSV COLLECTOR ===")
        print("Products collected:", len(products))

        if products:
            print("\n=== FIRST PRODUCT ===")
            print(
                json.dumps(
                    products[0],
                    ensure_ascii=False,
                    indent=2
                )
            )

    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)
