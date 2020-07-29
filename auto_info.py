"""
考题要求采集易车网大众品牌汽车信息http://car.bitauto.com/xuanchegongju/?l=8&mid=8
通过完善爬虫功能，抓取了易车网所有品牌所有车型的信息
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pandas import DataFrame


def AutoInfoSpider(url):
    # 启动服务
    c_service = Service('C:/Users/gusisong/AppData/Local/Continuum/anaconda3/chromedriver.exe')
    c_service.command_line_args()
    c_service.start()

    # 功能配置
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--disable-gpu')
    option.add_argument('--disable-images')
    option.add_argument('--disable-javascript')
    option.add_argument('--disable-plugins')
    option.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=option)

    driver.get(url)
    output = []

    for letter_index in range(1, 25):
        # 按品牌抓取
        brand_list = driver.find_elements_by_xpath(
            '/html/body/div[8]/div[1]/div[2]/div/div[{}]//a/div'.format(letter_index))
        for brand_index in range(2, len(brand_list) + 2):
            # 记录品牌名称
            brand_name = driver.find_element_by_xpath(
                '/html/body/div[8]/div[1]/div[2]/div/div[{0}]/div[{1}]/a/div'.format(letter_index, brand_index)).text
            # 进入车型目录
            driver.find_element_by_xpath(
                '/html/body/div[8]/div[1]/div[2]/div/div[{0}]/div[{1}]/a/div'.format(letter_index, brand_index)).click()

            # 按页码抓取
            page_list = driver.find_elements_by_xpath('/html/body/div[8]/div[4]/div[5]/div/div/div/a')
            for page_index in range(1, len(page_list) + 1):

                if page_index > 1:
                    driver.find_element_by_xpath(
                        '/html/body/div[8]/div[4]/div[5]/div/div/div/a[{}]'.format(page_index)).click()

                model_list = driver.find_elements_by_xpath('/html/body/div[8]/div[4]/div[3]/div')
                for model_index in range(1, len(model_list) + 1):
                    # 记录车型名称
                    model_name = driver.find_element_by_xpath(
                        '/html/body/div[8]/div[4]/div[3]/div[{}]/a/p[1]'.format(model_index)).text

                    # 记录车型价格
                    price_range = driver.find_element_by_xpath(
                        '/html/body/div[8]/div[4]/div[3]/div[{}]/a/p[2]'.format(model_index)).text

                    if '-' in price_range:
                        min_price = price_range[:-1].split('-')[0] + '万'
                        max_price = price_range[:-1].split('-')[1] + '万'

                    elif '暂无' in price_range:
                        min_price = '暂无'
                        max_price = '暂无'

                    else:
                        min_price = price_range
                        max_price = price_range

                    # 记录图片链接
                    pic_link = driver.find_element_by_xpath(
                        '/html/body/div[8]/div[4]/div[3]/div[{}]/a/img'.format(model_index)).get_attribute("src")

                    print(brand_name, model_name, min_price, max_price, pic_link)
                    output.append([brand_name, model_name, min_price, max_price, pic_link])

    # 写入文件
    df = DataFrame(output)
    df.columns = ['品牌名', '车型', '最低价', '最高价', '图片链接']
    df.to_csv('auto_info.csv', encoding='utf_8_sig')

    # 后台完全关闭
    driver.close()
    driver.quit()
    c_service.stop()


def main():
    url = 'http://car.bitauto.com/xuanchegongju'
    AutoInfoSpider(url)


if __name__ == '__main__':
    main()
