import sys
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0 Safari/537.36"
    )
}


def fetch_product_page(url: str):
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20,
        allow_redirects=True
    )

    response.raise_for_status()

    return {
        "status_code": response.status_code,
        "final_url": response.url,
        "html": response.text
    }


def inspect_html(html: str, product_id: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    html_lower = html.lower()

    return {
        "product_id_found": product_id in html,
        "next_data_found": "__next_data__" in html_lower,
        "product_keyword_found": "product" in html_lower,
        "name_keyword_found": '"name"' in html_lower,
        "price_keyword_found": "price" in html_lower,
        "html_length": len(html),
        "script_count": len(soup.find_all("script"))
    }


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python parser.py <shopee_product_url>")
        sys.exit(1)

    url = sys.argv[1]

    try:
        page = fetch_product_page(url)

        result = {
            "status_code": page["status_code"],
            "final_url": page["final_url"],
            **inspect_html(
                page["html"],
                "21692161576"
            )
        }

        print(result)

    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)
