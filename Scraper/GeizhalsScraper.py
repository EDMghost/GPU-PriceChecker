from playwright.sync_api import sync_playwright
import re

from Runner.Delay import human_delay


class GeizhalsScraper():
    def __init__(self, headless=False):
        self.headless = headless

    def scrape_gpu(self, gpu_model: str, target_price: int):
        """Scrape Geizhals.de for a GPU and return top 10 closest matches."""
        search_query = gpu_model.replace(" ", "+")
        if (search_query.startswith("RX")) :
            url = f"https://geizhals.de/?cat=gra16_512&xf=9809_05+16+-+{search_query}"
        else:
            url = f"https://geizhals.de/?cat=gra16_512&xf=9816_03+05+18+-+{search_query}"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            page.goto(url)
            human_delay(2, 5)

            # Wait a little for JS to load
            page.wait_for_timeout(2000)

            # Grab product containers
            product_elements = page.query_selector_all("article.galleryview__item.card")

            products_list = []
            for product in product_elements:
                human_delay(0.05, 0.15)
                name_el = product.query_selector("a.galleryview__name-link")
                price_el = product.query_selector("span.price")
                if not name_el or not price_el:
                    continue

                name = name_el.inner_text().strip()
                price_text = price_el.inner_text().strip()
                price_clean = re.sub(r"[^\d,\.]", "", price_text)  # remove everything except digits, comma, dot
                price = int(float(price_clean.replace(".", "").replace(",", ".")))

                products_list.append((name, price))

            browser.close()

        if not products_list:
            return gpu_model, target_price, []

        # Sort by closest to target price
        products_list.sort(key=lambda x: abs(x[1] - target_price))

        return gpu_model, target_price, products_list[:10]
