import requests
from urllib.parse import urlparse


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0 Safari/537.36"
    )
}


def resolve_url(url: str) -> dict:
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20,
        allow_redirects=True
    )

    final_url = response.url

    return {
        "original_url": url,
        "final_url": final_url,
        "status_code": response.status_code
    }


def extract_product_id(url: str) -> dict:
    parts = [
        part
        for part in urlparse(url).path.split("/")
        if part
    ]

    result = {
        "shop_id": "",
        "product_id": ""
    }

    if "product" in parts:
        index = parts.index("product")

        if len(parts) > index + 2:
            result["shop_id"] = parts[index + 1]
            result["product_id"] = parts[index + 2]

    return result


if __name__ == "__main__":
    url = input("Enter Shopee URL: ").strip()

    try:
        resolved = resolve_url(url)
        ids = extract_product_id(resolved["final_url"])

        result = {
            **resolved,
            **ids
        }

        print(result)

    except Exception as error:
        print(f"Error: {error}")
