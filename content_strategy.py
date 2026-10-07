import json


def build_strategy(product: dict) -> dict:
    product_data = product.get("product", {})
    commerce = product.get("commerce", {})
    ai = product.get("ai_analysis", {})

    title = product_data.get("title", "")
    category_l1 = product_data.get("category_l1", "")
    category_l2 = product_data.get("category_l2", "")
    category_l3 = product_data.get("category_l3", "")

    price = commerce.get("sale_price", 0)
    discount = commerce.get(
        "discount_percentage",
        0
    )

    hook_angles = ai.get(
        "hook_angles",
        []
    )

    demo_angles = ai.get(
        "demo_angles",
        []
    )

    problem_angles = ai.get(
        "problem_solution_angles",
        []
    )

    benefits = ai.get(
        "benefits",
        []
    )

    selling_points = ai.get(
        "selling_points",
        []
    )

    # Target audience
    if category_l2:
        target_customer = (
            f"关注{category_l2}的消费者"
        )
    elif category_l1:
        target_customer = (
            f"关注{category_l1}的消费者"
        )
    else:
        target_customer = "有相关产品需求的消费者"

    # Use case
    if category_l3:
        use_case = (
            f"{category_l3}相关使用场景"
        )
    elif category_l2:
        use_case = (
            f"{category_l2}日常使用场景"
        )
    else:
        use_case = "日常使用场景"

    # Pain point
    if problem_angles:
        pain_point = problem_angles[0]
    elif benefits:
        pain_point = (
            f"用户需要更方便地解决{benefits[0]}"
        )
    else:
        pain_point = "用户存在实际使用需求"

    # Primary hook
    if hook_angles:
        primary_hook = hook_angles[0]
    elif selling_points:
        primary_hook = selling_points[0]
    else:
        primary_hook = "展示产品核心价值"

    # Primary demo
    if demo_angles:
        primary_demo = demo_angles[0]
    elif selling_points:
        primary_demo = (
            f"展示{selling_points[0]}"
        )
    else:
        primary_demo = "展示产品实际使用方式"

    # CTA
    if discount > 0:
        cta = "查看当前优惠价格"
    else:
        cta = "查看商品详情"

    # Content angle
    content_angle = {
        "topic": title,
        "target_customer": target_customer,
        "use_case": use_case,
        "pain_point": pain_point,
        "hook": primary_hook,
        "demo": primary_demo,
        "benefit": (
            benefits[0]
            if benefits
            else "产品核心价值"
        ),
        "selling_point": (
            selling_points[0]
            if selling_points
            else "产品核心卖点"
        ),
        "cta": cta
    }

    # Generate multiple content directions
    content_directions = []

    if hook_angles:
        for hook in hook_angles[:3]:
            content_directions.append({
                "angle": hook,
                "format": "problem_hook",
                "hook": hook,
                "demo": primary_demo,
                "cta": cta
            })

    if demo_angles:
        for demo in demo_angles[:2]:
            content_directions.append({
                "angle": demo,
                "format": "product_demo",
                "hook": primary_hook,
                "demo": demo,
                "cta": cta
            })

    if problem_angles:
        for problem in problem_angles[:2]:
            content_directions.append({
                "angle": problem,
                "format": "problem_solution",
                "hook": problem,
                "demo": primary_demo,
                "cta": cta
            })

    product["content_strategy"] = {
        "target_customer": target_customer,
        "use_case": use_case,
        "pain_point": pain_point,
        "primary_hook": primary_hook,
        "primary_demo": primary_demo,
        "primary_benefit": (
            benefits[0]
            if benefits
            else ""
        ),
        "primary_selling_point": (
            selling_points[0]
            if selling_points
            else ""
        ),
        "cta": cta,
        "content_directions": content_directions
    }

    product["system"]["status"] = (
        "strategy_ready"
    )

    return product


if __name__ == "__main__":

    with open(
        "selected_products.json",
        "r",
        encoding="utf-8"
    ) as file:

        products = json.load(file)

    strategy_products = [
        build_strategy(product)
        for product in products
    ]

    with open(
        "content_strategy.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            strategy_products,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("=== CONTENT STRATEGY ===")

    print(
        "Products processed:",
        len(strategy_products)
    )

    print(
        "Output:",
        "content_strategy.json"
    )

    if strategy_products:

        first = strategy_products[0]
        strategy = first[
            "content_strategy"
        ]

        print(
            "\n=== FIRST STRATEGY ==="
        )

        print(
            "Target:",
            strategy["target_customer"]
        )

        print(
            "Use case:",
            strategy["use_case"]
        )

        print(
            "Pain point:",
            strategy["pain_point"]
        )

        print(
            "Hook:",
            strategy["primary_hook"]
        )

        print(
            "Demo:",
            strategy["primary_demo"]
        )

        print(
            "CTA:",
            strategy["cta"]
        )

        print(
            "Directions:",
            len(
                strategy[
                    "content_directions"
                ]
            )
        )

    print(
        "\nContent Strategy: OK"
    )
