import sys
from playwright.sync_api import sync_playwright


def fetch_rendered_page(url: str) -> dict:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            viewport={
                "width": 1280,
                "height": 900
            }
        )

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(5000)

        result = {
            "title": page.title(),
            "url": page.url,
            "text_length": len(page.locator("body").inner_text()),
            "body_text": page.locator("body").inner_text()[:3000]
        }

        browser.close()

        return result


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python parser.py <shopee_product_url>")
        sys.exit(1)

    url = sys.argv[1]

    try:
        result = fetch_rendered_page(url)

        print("=== PLAYWRIGHT RESULT ===")
        print("TITLE:", result["title"])
        print("URL:", result["url"])
        print("TEXT LENGTH:", result["text_length"])

        print("\n=== PAGE TEXT ===")
        print(result["body_text"])

    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)
