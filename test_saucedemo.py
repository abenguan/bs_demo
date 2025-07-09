import pytest
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def test_saucedemo_products():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 可改为True
        page = browser.new_page()
        page.goto("https://www.saucedemo.com/")
        page.fill('input[data-test="username"]', "standard_user")
        page.fill('input[data-test="password"]', "secret_sauce")
        page.click('input[data-test="login-button"]')
        # 等待跳转到商品页
        page.wait_for_url("**/inventory.html")
        # 获取商品页HTML
        html = page.content()
        browser.close()

    # 用 BeautifulSoup 解析商品数据
    soup = BeautifulSoup(html, "html.parser")
    products = soup.find_all("div", class_="inventory_item")
    result_lines = []
    for product in products:
        name = product.find("div", class_="inventory_item_name").get_text(strip=True)
        price = product.find("div", class_="inventory_item_price").get_text(strip=True)
        result_lines.append(f"{name}｜{price}")

    # 写入本地文件
    with open("products.txt", "w", encoding="utf-8") as f:
        for line in result_lines:
            f.write(line + "\n")

    # 断言
    assert len(result_lines) > 0, "未抓取到任何商品,请确认！22225555"