from datetime import datetime


def normalize_product(raw_data: dict) -> dict:
    now = datetime.utcnow().isoformat()

    product = {
        "product_id": str(raw_data.get("product_id", "")),
        "source": "shopee",
        "product_url": raw_data.get("product_url", ""),
        "affiliate_url": raw_data.get("affiliate_url", ""),

        "product": {
            "name": raw_data.get("name", ""),
            "category": raw_data.get("category", ""),
            "subcategory": raw_data.get("subcategory", ""),
            "brand": raw_data.get("brand", ""),
            "description": raw_data.get("description", "")
        },

        "commerce": {
            "price": raw_data.get("price", 0),
            "original_price": raw_data.get("original_price", 0),
            "discount": raw_data.get("discount", 0),
            "currency": raw_data.get("currency", "SGD"),
            "sold_count": raw_data.get("sold_count", 0),
            "rating": raw_data.get("rating", 0),
            "review_count": raw_data.get("review_count", 0),
            "commission_rate": raw_data.get("commission_rate", 0)
        },

        "audience": {
            "target_customer": raw_data.get("target_customer", ""),
            "use_case": raw_data.get("use_case", ""),
            "pain_point": raw_data.get("pain_point", "")
        },

        "features": raw_data.get("features", []),
        "benefits": raw_data.get("benefits", []),
        "selling_points": raw_data.get("selling_points", []),

        "content": {
            "hook_angles": raw_data.get("hook_angles", []),
            "demo_angles": raw_data.get("demo_angles", []),
            "problem_solution_angles": raw_data.get(
                "problem_solution_angles", []
            ),
            "visual_potential": raw_data.get(
                "visual_potential", 0
            ),
            "viral_potential": raw_data.get(
                "viral_potential", 0
            )
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

        "status": "normalized",
        "created_at": raw_data.get("created_at", now),
        "updated_at": now
    }

    return product


if __name__ == "__main__":
    test_data = {
        "product_id": "TEST001",
        "product_url": "https://shopee.sg/",
        "name": "Test Product",
        "category": "Test"
    }

    result = normalize_product(test_data)

    import json

    print(json.dumps(
        result,
        indent=2,
        ensure_ascii=False
    ))
