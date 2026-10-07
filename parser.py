import sys
import requests

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0 Safari/537.36"
    )
}


def fetch_html(url: str) -> str:
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20,
        allow_redirects=True
    )
    response.raise_for_status()
    return response.text


def find_context(html: str, keyword: str, radius: int = 500) -> str:
    position = html.lower().find(keyword.lower())

    if position == -1:
        return ""

    start = max(0, position - radius)
    end = min(len(html), position + len(keyword) + radius)

    return html[start:end]


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python parser.py <shopee_product_url>")
        sys.exit(1)

    url = sys.argv[1]

    try:
        html = fetch_html(url)

        print("HTML LENGTH:", len(html))

        print("\n=== PRODUCT CONTEXT ===")
        print(find_context(html, '"product"', 800))

        print("\n=== NAME CONTEXT ===")
        print(find_context(html, '"name"', 800))

        print("\n=== PRICE CONTEXT ===")
        print(find_context(html, '"price"', 800))

    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)
