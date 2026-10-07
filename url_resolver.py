import requests
from urllib.parse import urlparse, urlunparse


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

    parsed = urlparse(response.url)

    final_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        "",
        "",
        ""
    ))

    return {
        "original_url": url,
        "final_url": final_url,
        "status_code": response.status_code
    }


def extract_product_id(url: str) -> dict:
    path = urlparse(url).path.strip("/")
    parts = path.split("/")

    result = {
        "shop_id": "",
        "product_id": ""
    }

    if len(parts) >= 3:
        if parts[0] == "opaanlp":
            result["shop_id"] = parts[1]
            result["product_id"] = parts[2]

        elif parts[0] == "product":
            result["shop_id"] = parts[1]
            result["product_id"] = parts[2]

    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python url_resolver.py <shopee_url>")
        sys.exit(1)

    url = sys.argv[1]

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
        sys.exit(1)
