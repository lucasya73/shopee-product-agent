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

10-13 seconds:
Highlight the main product benefit.
Benefit: {benefit}

13-15 seconds:
Show the product clearly with a clean final shot.
Display the price SGD {price} and call to action: {cta}

Visual requirements:
- Keep the product as the main subject.
- Preserve the product's actual appearance, packaging, shape and proportions.
- Use clean backgrounds with minimal visual clutter.
- Smooth camera movement.
- Clear product close-ups.
- No unrelated objects.
- No exaggerated or unrealistic product claims.
- No distorted packaging or logos.
- Vertical 9:16 composition.
- Total duration: 15 seconds.
"""

    return prompt.strip()


def build_content(product: dict) -> dict:
    strategy = product.get("content_strategy", {})

    product_images = select_product_images(product)

    product_tags = build_product_tags(
        product,
        strategy
    )

    video_prompt = build_video_prompt(
        product,
        strategy
    )

    return {
        "product_id": product.get(
            "product_id",
            ""
        ),

        "title": product.get(
            "product",
            {}
        ).get("title", ""),

        "affiliate_url": product.get(
            "identity",
            {}
        ).get("affiliate_url", ""),

        "product_images": product_images,

        "product_tags": product_tags,

        "video_prompt": video_prompt,

        "status": "content_ready"
    }


if __name__ == "__main__":

    with open(
        "content_strategy.json",
        "r",
        encoding="utf-8"
    ) as file:

        products = json.load(file)

    contents = [
        build_content(product)
        for product in products
    ]

    with open(
        "content_factory.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            contents,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("=== CONTENT FACTORY ===")

    print(
        "Products processed:",
        len(contents)
    )

    print(
        "Output:",
        "content_factory.json"
    )

    if contents:

        first = contents[0]

        print(
            "\n=== FIRST CONTENT ==="
        )

        print(
            "Product ID:",
            first["product_id"]
        )

        print(
            "Images:",
            len(first["product_images"])
        )

        print(
            "Tags length:",
            len(first["product_tags"])
        )

        print(
            "Video prompt:",
            "OK"
            if first["video_prompt"]
            else "EMPTY"
        )

        print(
            "Status:",
            first["status"]
        )

    print(
        "\nContent Factory: OK"
    )
