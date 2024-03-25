import re

from playwright.sync_api import sync_playwright

import pandas as pd

def run(playwright):

    data = []

    browser = playwright.chromium.launch(headless=False,
                                         args=["--disable-blink-features=AutomationControlled", "--start-maximized"])

    context = browser.new_context(no_viewport=True)

    page = context.new_page()

    page.goto("https://movie.douban.com/explore", timeout=1000000)

    page.wait_for_timeout(10000)

    for xx in range(0, 21):

        page.locator('//*[@id="app"]/div/div[2]/div/button').click()

        page.mouse.wheel(0, 10000)

        page.wait_for_timeout(2000)

    lilist = page.query_selector_all('//*[@id="app"]/div/div[2]/ul/li')

    for li in lilist:
        href = li.query_selector('//a').get_attribute('href')

        page1 = context.new_page()

        page1.goto(href, timeout=300000)

        page1.wait_for_load_state("domcontentloaded")

        title = page1.query_selector('//span[@property="v:itemreviewed"]').text_content()

        yue = page1.query_selector('//span[@class="year"]').text_content().replace('(', '').replace(')', '')

        try:

            page1.locator('//a[@class="more-actor"]').click(timeout=1000)

        except:

            pass

        page1.wait_for_timeout(1000)

        html = page1.query_selector('//*[@id="info"]').inner_text()

        dy = re.findall('导演:(.*?)编剧:', html, re.DOTALL)

        dy = ''.join(dy)

        zy = re.findall('主演:(.*?)类型:', html, re.DOTALL)

        zy = ''.join(zy)

        gj = re.findall('制片国家/地区:(.*?)语言: ', html, re.DOTALL)

        gj = ''.join(gj)

        try:

            lx = re.findall('类型:(.*?)官方网站:|类型:(.*?)制片国家', html, re.DOTALL)[0]

            lx = ''.join(lx)

        except:

            lx = re.findall('类型:(.*?)官方网站:|类型:(.*?)制片国家', html, re.DOTALL)[-1]

            lx = ''.join(lx)

        dit = {
            '名称': title,
            '年份': yue,
            '导演': dy,
            '主演': zy,
            '国家': gj,
            '类型': lx
        }

        print(dit)

        data.append(dit)

        ff = pd.DataFrame(data)

        ff.to_excel('豆瓣动漫数据.xlsx', index=False)

        page1.close()

with sync_playwright() as playwright:
    run(playwright)
