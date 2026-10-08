import json


def select_product_images(product: dict) -> list:
    media = product.get("media", {})

    candidates = [
        media.get("image", ""),
        media.get("image_2", ""),
        media.get("image_3", ""),
        media.get("image_4", ""),
        media.get("image_5", "")
    ]

    candidates = [
        url for url in candidates
        if isinstance(url, str) and url.strip()
    ]

    # 优先使用前3张图片。
    # Datafeed中的图片顺序通常已经是商品主图及补充图。
    return candidates[:3]


def build_product_tags(product: dict, strategy: dict) -> str:
    product_data = product.get("product", {})
    commerce = product.get("commerce", {})

    title = product_data.get("title", "")
    brand = product_data.get("brand", "")
    category_l1 = product_data.get("category_l1", "")
    category_l2 = product_data.get("category_l2", "")
    category_l3 = product_data.get("category_l3", "")

    target_customer = strategy.get("target_customer", "")
    use_case = strategy.get("use_case", "")
    pain_point = strategy.get("pain_point", "")
    selling_point = strategy.get("primary_selling_point", "")

    tags = [
        title,
        brand,
        category_l1,
        category_l2,
        category_l3,
        target_customer,
        use_case,
        pain_point,
        selling_point,
        f"SGD {commerce.get('sale_price', 0)}"
    ]

    tags = [
        str(tag).strip()
        for tag in tags
        if str(tag).strip()
    ]

    result = "｜".join(tags)

    return result[:150]


def build_video_prompt(product: dict, strategy: dict) -> str:
    product_data = product.get("product", {})
    commerce = product.get("commerce", {})

    title = product_data.get("title", "")
    brand = product_data.get("brand", "")
    category = product_data.get("category_l2", "")
    price = commerce.get("sale_price", 0)

    hook = strategy.get(
        "primary_hook",
        "快速展示产品并吸引注意力"
    )

    demo = strategy.get(
        "primary_demo",
        "展示产品实际使用方式"
    )

    pain_point = strategy.get(
        "pain_point",
        ""
    )

    benefit = strategy.get(
        "primary_benefit",
        ""
    )

    selling_point = strategy.get(
        "primary_selling_point",
        ""
    )

    cta = strategy.get(
        "cta",
        "查看商品详情"
    )

    prompt = f"""
Create a 15-second vertical 9:16 product promotional video for:
Product: {title}
Brand: {brand}
Category: {category}

Video style:
UGC-style product demonstration, realistic, clean, modern, natural lighting, fast-paced social media advertising.

0-3 seconds:
Immediately show the product clearly and create a strong visual hook.
Hook: {hook}

3-6 seconds:
Visually present the user's problem or need.
Problem: {pain_point}

6-10 seconds:
Demonstrate the product clearly in a realistic use scenario.
Demonstration: {demo}
Key selling point: {selling_point}

10-
