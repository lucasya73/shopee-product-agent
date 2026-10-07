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
        "content_type": response.headers.get("content-type", ""),
        "html": response.text
    }


def parse_basic_info(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    description = ""
    description_tag = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if description_tag:
        description = description_tag.get(
            "content",
            ""
        ).strip()

    return {
        "page_title": title,
        "page_description": description,
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
        product_info = parse_basic_info(page["html"])

        print({
            "status_code": page["status_code"],
            "final_url": page["final_url"],
            "content_type": page["content_type"],
            **product_info
        })

    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)
