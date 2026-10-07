import json


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(value, maximum))


def score_demand(product):
    commerce = product.get("commerce", {})

    sold = commerce.get("item_sold", 0)
    rating = commerce.get("item_rating", 0)
    likes = commerce.get("like_count", 0)

    sold_score = min(sold / 10, 40)
    rating_score = max(
        0,
        (rating - 3.0) * 20
    )
    like_score = min(likes / 10, 20)

    return clamp(
        sold_score
        + rating_score
        + like_score
    )


def score_content(product):
    ai = product.get("ai_analysis", {})

    hook_count = len(
        ai.get("hook_angles", [])
    )

    demo_count = len(
        ai.get("demo_angles", [])
    )

    problem_count = len(
        ai.get("problem_solution_angles", [])
    )

    base = ai.get(
        "content_potential",
        0
    )

    structure_score = (
        min(hook_count * 10, 30)
        + min(demo_count * 10, 30)
        + min(problem_count * 10, 20)
    )

    return clamp(
        base * 0.5
        + structure_score
    )


def score_visual(product):
    ai = product.get("ai_analysis", {})

    return clamp(
        ai.get(
            "visual_potential",
            0
        )
    )


def score_problem(product):
    ai = product.get("ai_analysis", {})

    problem_angles = len(
        ai.get(
            "problem_solution_angles",
            []
        )
    )

    pain_point = ai.get(
        "pain_point",
        ""
    )

    score = (
        problem_angles * 20
    )

    if pain_point:
        score += 30

    return clamp(score)


def score_impulse(product):
    ai = product.get("ai_analysis", {})

    return clamp(
        ai.get(
            "impulse_potential",
            0
        )
    )


def score_price(product):
    commerce = product.get("commerce", {})

    price = commerce.get(
        "sale_price",
        0
    )

    discount = commerce.get(
        "discount_percentage",
        0
    )

    score = 0

    if price > 0:

        if price <= 20:
            score += 50

        elif price <= 50:
            score += 40

        elif price <= 100:
            score += 30

        elif price <= 200:
            score += 20

        else:
            score += 10

    score += min(
        discount,
        40
    )

    return clamp(score)


def score_competition(product):
    """
    Current datafeed does not provide
    reliable market-wide competition data.

    Use neutral score for now.
    Replace with real competition analysis later.
    """

    return 50


def calculate_total(scores):
    total = (
        scores["demand"] * 0.20
        + scores["content"] * 0.20
        + scores["visual"] * 0.15
        + scores["problem"] * 0.15
        + scores["impulse"] * 0.10
        + scores["price"] * 0.10
        + scores["competition"] * 0.10
    )

    return round(
        clamp(total),
        2
    )


def score_product(product):

    scores = {
        "demand": round(
            score_demand(product),
            2
        ),

        "content": round(
            score_content(product),
            2
        ),

        "visual": round(
            score_visual(product),
            2
        ),

        "problem": round(
            score_problem(product),
            2
        ),

        "impulse": round(
            score_impulse(product),
            2
        ),

        "price": round(
            score_price(product),
            2
        ),

        "competition": round(
            score_competition(product),
            2
        )
    }

    scores["total"] = calculate_total(
        scores
    )

    product["scores"] = scores

    product["system"]["status"] = (
        "scored"
    )

    return product


if __name__ == "__main__":

    with open(
        "intelligence_products.json",
        "r",
        encoding="utf-8"
    ) as file:

        products = json.load(file)

    scored_products = [
        score_product(product)
        for product in products
    ]

    scored_products.sort(
        key=lambda x: x["scores"]["total"],
        reverse=True
    )

    with open(
        "scored_products.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            scored_products,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("=== SCORER ===")

    print(
        "Products scored:",
        len(scored_products)
    )

    print(
        "Output:",
        "scored_products.json"
    )

    print(
        "\n=== RANKING ==="
    )

    for index, product in enumerate(
        scored_products,
        start=1
    ):

        print(
            f"{index}. "
            f"{product['product']['title']} "
            f"→ "
            f"{product['scores']['total']}"
        )

    print(
        "\nScoring: OK"
    )
