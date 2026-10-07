import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0 Safari/537.36"
    )
}


def fetch_product_page(url: str) -> str:
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    return response.text


def parse_basic_info(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    title = soup.title.string.strip() if soup.title else ""

    description_tag = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    description = ""

    if description_tag:
        description = description_tag.get("content", "").strip()

    return {
        "page_title": title,
        "page_description": description
    }


if __name__ == "__main__":
    url = input("Enter Shopee product URL: ").strip()

    try:
        html = fetch_product_page(url)
        product_info = parse_basic_info(html)

        print("\nProduct Information:")
        print(product_info)

    except Exception as error:
        print(f"\nError: {error}")
