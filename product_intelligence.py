import json


def build_intelligence(product: dict) -> dict:
    product_data = product.get("product", {})
    commerce = product.get("commerce", {})
    shop = product.get("shop", {})
    attributes = product.get("attributes", {})

    title = product_data.get("title", "")
    description = product_data.get("description", "")
    category_l1 = product_data.get("category_l1", "")
    category_l2 = product_data.get("category_l2", "")
    category_l3 = product_data.get("category_l3", "")
    brand = product_data.get("brand", "")

    price = commerce.get("sale_price", 0)
    original_price = commerce.get("price", 0)
    sold = commerce.get("item_sold", 0)
    rating = commerce.get("item_rating", 0)
    likes = commerce.get("like_count", 0)

    text = (
        f"{title} "
        f"{description} "
        f"{category_l1} "
        f"{category_l2} "
        f"{category_l3} "
        f"{brand}"
    ).lower()

    benefits = []
    selling_points = []
    hook_angles = []
    demo_angles = []
    problem_solution_angles = []

    # Category-based signals
    if "health" in text or "supplement" in text:
        benefits.append("健康与日常保养")
        hook_angles.append("日常健康需求")
        problem_solution_angles.append(
            "针对日常健康管理需求提供解决方案"
        )

    if "home" in text:
        benefits.append("提升居家便利性")
        hook_angles.append("解决居家生活中的实际问题")

    if (
       "beauty" in category_l1
       or "beauty" in category_l2
       or "skin care" in category_l2
       or "skincare" in category_l2
    ):
       benefits.append("美容与个人护理")
       hook_angles.append("改善日常护理体验")

    # Product text signals
    if "waterproof" in text:
        selling_points.append("防水")
        demo_angles.append("防水实测")

    if "portable" in text or "compact" in text:
        selling_points.append("便携")
        demo_angles.append("便携尺寸展示")

    if "wireless" in text:
        selling_points.append("无线")
        demo_angles.append("无线使用场景")

    if "fireproof" in text:
        selling_points.append("防火")
        demo_angles.append("防火功能展示")

    if "non-acidic" in text:
        selling_points.append("非酸性配方")
        demo_angles.append("产品特点对比")

    # Price signal
    if original_price > 0 and price > 0:
        if price < original_price:
            hook_angles.append(
                "折扣价格带来的购买理由"
            )

    # Social proof
    if sold >= 100:
        hook_angles.append(
            "已有大量销量的社会证明"
        )

    if rating >= 4.5:
        hook_angles.append(
            "高评分带来的信任感"
        )

    if likes >= 100:
        hook_angles.append(
            "用户关注度高"
        )

    # Fallback
    if not benefits:
        benefits.append(
            "满足该商品核心使用需求"
        )

    if not selling_points:
        selling_points.append(
            "产品核心功能与用途"
        )

    if not hook_angles:
        hook_angles.append(
            "产品功能展示"
        )

    if not demo_angles:
        demo_angles.append(
            "产品实际使用演示"
        )

    if not problem_solution_angles:
        problem_solution_angles.append(
            "展示产品如何解决实际需求"
        )

    # Potential scores
    visual_potential = 0

    if demo_angles:
        visual_potential += 30

    if selling_points:
        visual_potential += 20

    if "portable" in text or "compact" in text:
        visual_potential += 20

    if "wireless" in text or "waterproof" in text:
        visual_potential += 20

    if "fireproof" in text:
        visual_potential += 10

    content_potential = 0

    content_potential += min(
        len(hook_angles) * 10,
        40
    )

    content_potential += min(
        len(demo_angles) * 10,
        30
    )

    content_potential += min(
        len(problem_solution_angles) * 10,
        30
    )

    impulse_potential = 0

    if price > 0 and price <= 50:
        impulse_potential += 40

    if commerce.get(
        "discount_percentage",
        0
    ) >= 20:
        impulse_potential += 30

    if sold >= 100:
        impulse_potential += 20

    if rating >= 4.5:
        impulse_potential += 10

    product["ai_analysis"] = {
        "target_customer": "",
        "use_case": "",
        "pain_point": "",
        "benefits": benefits,
        "selling_points": selling_points,
        "hook_angles": hook_angles,
        "demo_angles": demo_angles,
        "problem_solution_angles": problem_solution_angles,
        "visual_potential": min(
            visual_potential,
            100
        ),
        "content_potential": min(
            content_potential,
            100
        ),
        "impulse_potential": min(
            impulse_potential,
            100
        )
    }

    product["system"]["status"] = (
        "intelligence_ready"
    )

    return product


if __name__ == "__main__":

    with open(
        "validated_products.json",
        "r",
        encoding="utf-8"
    ) as file:

        products = json.load(file)

    analyzed_products = [
        build_intelligence(product)
        for product in products
    ]

    with open(
        "intelligence_products.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            analyzed_products,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("=== PRODUCT INTELLIGENCE ===")

    print(
        "Products analyzed:",
        len(analyzed_products)
    )

    print(
        "Output:",
        "intelligence_products.json"
    )

    if analyzed_products:

        first = analyzed_products[0]

        print(
            "\n=== FIRST PRODUCT ==="
        )

        print(
            "Title:",
            first["product"]["title"]
        )

        print(
            "Benefits:",
            first["ai_analysis"]["benefits"]
        )

        print(
            "Selling points:",
            first["ai_analysis"]["selling_points"]
        )

        print(
            "Hook angles:",
            first["ai_analysis"]["hook_angles"]
        )

        print(
            "Visual potential:",
            first["ai_analysis"]["visual_potential"]
        )

        print(
            "Content potential:",
            first["ai_analysis"]["content_potential"]
        )

        print(
            "Impulse potential:",
            first["ai_analysis"]["impulse_potential"]
        )
