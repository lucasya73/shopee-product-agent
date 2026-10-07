import json
from pathlib import Path


SCHEMA_FILE = Path(__file__).parent / "product_schema.json"


REQUIRED_FIELDS = [
    "product_id",
    "source",
    "product_url",
    "product",
    "commerce",
    "audience",
    "features",
    "benefits",
    "selling_points",
    "content",
    "scores",
    "status"
]


def validate_product(product: dict) -> dict:
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in product:
            errors.append(f"Missing field: {field}")

    if not product.get("product_url"):
        errors.append("product_url cannot be empty")

    if product.get("source") != "shopee":
        errors.append("source must be 'shopee'")

    if errors:
        return {
            "valid": False,
            "errors": errors
        }

    return {
        "valid": True,
        "errors": []
    }


if __name__ == "__main__":
    test_product = {
        "product_id": "TEST001",
        "source": "shopee",
        "product_url": "https://shopee.sg/",
        "product": {},
        "commerce": {},
        "audience": {},
        "features": [],
        "benefits": [],
        "selling_points": [],
        "content": {},
        "scores": {},
        "status": "raw"
    }

    result = validate_product(test_product)

    print(json.dumps(
        result,
        indent=2,
        ensure_ascii=False
    ))
