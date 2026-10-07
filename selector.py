import json


MIN_TOTAL_SCORE = 50
MIN_CONTENT_SCORE = 40
MIN_VISUAL_SCORE = 30
MIN_DEMAND_SCORE = 20

TOP_N = 10


def is_selectable(product: dict) -> bool:
    scores = product.get(
        "scores",
        {}
    )

    total = scores.get(
        "total",
        0
    )

    content = scores.get(
        "content",
        0
    )

    visual = scores.get(
        "visual",
        0
    )

    demand = scores.get(
        "demand",
        0
    )

    return (
        total >= MIN_TOTAL_SCORE
        and content >= MIN_CONTENT_SCORE
        and visual >= MIN_VISUAL_SCORE
        and demand >= MIN_DEMAND_SCORE
    )


def select_products(products: list) -> list:

    selected = [
        product
        for product in products
        if is_selectable(product)
    ]

    selected.sort(
        key=lambda product:
        product.get(
            "scores",
            {}
        ).get("total", 0),
        reverse=True
    )

    return selected[:TOP_N]


if __name__ == "__main__":

    with open(
        "scored_products.json",
        "r",
        encoding="utf-8"
    ) as file:

        products = json.load(file)

    selected_products = select_products(
        products
    )

    for product in selected_products:

        product["system"]["status"] = (
            "selected"
        )

    with open(
        "selected_products.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            selected_products,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("=== SELECTOR ===")

    print(
        "Products evaluated:",
        len(products)
    )

    print(
        "Products selected:",
        len(selected_products)
    )

    print(
        "Output:",
        "selected_products.json"
    )

    print(
        "\n=== SELECTED PRODUCTS ==="
    )

    for index, product in enumerate(
        selected_products,
        start=1
    ):

        scores = product.get(
            "scores",
            {}
        )

        print(
            f"{index}. "
            f"{product['product']['title']} "
            f"→ "
            f"{scores.get('total', 0)}"
        )

    print(
        "\nSelection: OK"
    )
