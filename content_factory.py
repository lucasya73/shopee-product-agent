import json


def build_content(product: dict) -> dict:
    product_data = product.get("product", {})
    commerce = product.get("commerce", {})
    strategy = product.get("content_strategy", {})

    title = product_data.get("title", "")
    price = commerce.get("sale_price", 0)
    affiliate_url = product.get(
        "identity",
        {}
    ).get("affiliate_url", "")

    hook = strategy.get(
        "primary_hook",
        "发现一个值得关注的产品"
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

    script = {
        "0-3s": {
            "scene": "Hook",
            "voiceover": hook,
            "visual": "快速展示产品与核心卖点",
            "text": hook
        },

        "3-6s": {
            "scene": "Problem",
            "voiceover": pain_point,
            "visual": "展示用户可能遇到的问题或需求",
            "text": pain_point
        },

        "6-10s": {
            "scene": "Demo",
            "voiceover": demo,
            "visual": "展示产品实际使用方式",
            "text": selling_point
        },

        "10-13s": {
            "scene": "Benefit",
            "voiceover": benefit,
            "visual": "展示使用后的核心价值",
            "text": benefit
        },

        "13-15s": {
            "scene": "CTA",
            "voiceover": cta,
            "visual": "产品 + 价格 + 行动引导",
            "text": (
                f"SGD {price}｜{cta}"
            )
        }
    }

    content = {
        "product_id": product.get(
            "product_id",
            ""
        ),

        "title": title,

        "affiliate_url": affiliate_url,

        "content_type": "short_video",

        "platforms": [
            "TikTok",
            "Instagram Reels",
            "YouTube Shorts",
            "Shopee Video"
        ],

        "duration": 15,

        "aspect_ratio": "9:16",

        "script": script,

        "production": {
            "style": "UGC product demonstration",
            "language": "Chinese",
            "music": "fast paced",
            "visual_priority": [
                "product",
                "problem",
                "demo",
                "benefit",
                "cta"
            ]
        },

        "status": "script_ready"
    }

    return content


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
            "Title:",
            first["title"]
        )

        print(
            "Type:",
            first["content_type"]
        )

        print(
            "Duration:",
            first["duration"],
            "seconds"
        )

        print(
            "Aspect ratio:",
            first["aspect_ratio"]
        )

        print(
            "Status:",
            first["status"]
        )

        print(
            "Scenes:",
            len(first["script"])
        )

    print(
        "\nContent Factory: OK"
    )
