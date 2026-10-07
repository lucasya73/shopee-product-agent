import json
import sys
from datetime import datetime
from urllib.parse import urlparse


def create_product_record(product_url: str, affiliate_url: str = ""):
    parsed_url = urlparse(product_url)

    product_id = ”UNKNOWN"

    return {
        "product_id": product_id,
        "source": "shopee",
        "product_url": product_url,
        "affiliate_url": affiliate_url,

        "product": {
            "name": "",
            "category": "",
            "subcategory": "",
            "brand": "",
            "description": ""
        },

        "commerce": {
            "price": 0,
            "original_price": 0,
            "discount": 0,
            "currency": "SGD",
            "sold_count": 0,
            "rating": 0,
            "review_count": 0,
            "commission_rate": 0
        },

        "audience": {
            "target_customer": "",
            "use_case": "",
            "pain_point": ""
        },

        "features": [],
        "benefits": [],
        "selling_points": [],

        "content": {
            "hook_angles": [],
            "demo_angles": [],
            "problem_solution_angles": [],
            "visual_potential": 0,
            "viral_potential": 0
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

        "status": "raw",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python collector.py <shopee_product_url>")
        sys.exit(1)

    product_url = sys.argv[1]

    product = create_product_record(product_url)

    print(json.dumps(product, indent=2, ensure_ascii=False))
