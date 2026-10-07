import json


REQUIRED_FIELDS = [
    "product_id",
    "source",
    "market",
    "identity",
    "product",
    "commerce",
    "shop",
    "media",
    "attributes",
    "ai_analysis",
    "scores",
    "system"
]


def validate_product(product: dict) -> dict:
    errors = []

    # Top-level fields
    for field in REQUIRED_FIELDS:
        if field not in product:
            errors.append(
                f"Missing field: {field}"
            )

    # Identity
    identity = product.get(
        "identity",
        {}
    )

    if not identity.get("item_id"):
        errors.append(
            "identity.item_id cannot be empty"
        )

    if not identity.get("shop_id"):
        errors.append(
            "identity.shop_id cannot be empty"
        )

    if not identity.get("product_url"):
        errors.append(
            "identity.product_url cannot be empty"
        )

    if not identity.get("affiliate_url"):
        errors.append(
            "identity.affiliate_url cannot be empty"
        )

    # Product
    product_data = product.get(
        "product",
        {}
    )

    if not product_data.get("title"):
        errors.append(
            "product.title cannot be empty"
        )

    # Commerce
    commerce = product.get(
        "commerce",
        {}
    )

    if commerce.get("price", 0) < 0:
        errors.append(
            "commerce.price cannot be negative"
        )

    if commerce.get("sale_price", 0) < 0:
        errors.append(
            "commerce.sale_price cannot be negative"
        )

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
        if field not in scores:
            errors.append(
                f"Missing score: {field}"
            )

    # System
    system = product.get(
        "system",
        {}
    )

    if system.get("status") not in [
        "raw",
        "normalized",
        "validated"
    ]:
        errors.append(
            "Invalid system.status"
        )

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

    with open(
        "normalized_products.json",
        "r",
        encoding="utf-8"
    ) as file:

        products = json.load(file)

    valid_products = []
    invalid_products = []

    for product in products:

        result = validate_product(
            product
        )

        if result["valid"]:

            product["system"]["status"] = "validated"

            valid_products.append(product)

        else:

            invalid_products.append({
                "product_id": product.get(
                    "product_id",
                    ""
                ),
                "errors": result["errors"]
            })

    with open(
        "validated_products.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            valid_products,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("=== VALIDATOR ===")

    print(
        "Products checked:",
        len(products)
    )

    print(
        "Valid:",
        len(valid_products)
    )

    print(
        "Invalid:",
        len(invalid_products)
    )

    print(
        "Output:",
        "validated_products.json"
    )

    if invalid_products:

        print(
            "\n=== ERRORS ==="
        )

        print(
            json.dumps(
                invalid_products,
                ensure_ascii=False,
                indent=2
            )
        )

        raise SystemExit(1)

    print(
        "Validation: OK"
    )
