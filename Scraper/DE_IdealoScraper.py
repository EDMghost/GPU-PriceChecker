from playwright.sync_api import sync_playwright
import re


class IdealoScraper():
    def __init__(self, headless=True):
        self.headless = headless

    def scrape_gpu(self, gpu_model: str, target_price: int):
        """Scrape Price.ro for a GPU and return top 10 closest matches."""
        url = f"https://www.idealo.de/preisvergleich/ProductCategory/16073F1309393-{gpu_model}.html?sortKey=minPrice"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            page.goto(url)

            # Wait a little for JS to load
            page.wait_for_timeout(2000)

            # Grab product containers
            product_elements = page.query_selector_all("")

            products_list = []
            for product in product_elements:
                name_el = product.query_selector("")
                price_el = product.query_selector("")
                if not name_el or not price_el:
                    continue

                name = name_el.inner_text().strip()
                price_text = price_el.inner_text().strip()  # "2.640,99lei"
                price_clean = re.sub(r"[^\d,\.]", "", price_text)  # remove everything except digits, comma, dot
                price = int(float(price_clean.replace(".", "").replace(",", ".")))

                products_list.append((name, price))

            browser.close()

        if not products_list:
            return gpu_model, target_price, []

        # Sort by closest to target price
        products_list.sort(key=lambda x: abs(x[1] - target_price))

        return gpu_model, target_price, products_list[:10]
