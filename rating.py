
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from selenium.webdriver.common.by import By
# import requests
# from bs4 import BeautifulSoup

import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

import requests
import os
import re
import pickle
from selenium.webdriver.chrome.options import Options



def Extract_userid(comment):
    a_tag = comment.find_element(By.CSS_SELECTOR, "a[href*='/users/show/']")
    href = a_tag.get_attribute('href')
    
    # 使用正则表达式从 href 中提取数字
    match = re.search(r'/users/show/(\d+)', href)
    user_id = match.group(1)
    return user_id

def remove_empty_lines(text):
    # Splitting the text into lines
    lines = text.split('\n')

    # Filtering out empty or whitespace-only lines
    non_empty_lines = [line for line in lines if line.strip()]

    # Joining the non-empty lines back into a single string
    return '\n'.join(non_empty_lines)

# 读取 CSV 文件
df = pd.read_csv('src/rws4scrape.csv')

# 提取 'listing_url' 列并去重
unique_urls = df['listing_url'].unique()

# 将结果转换为列表
url_list = unique_urls.tolist()


# 创建一个WebDriver实例，使用Chrome浏览器
# driver = webdriver.Chrome()


options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1920x1080") 
driver = webdriver.Chrome(options=options)


# driver.get("https://www.airbnb.com/users/show/927861")
# with open("C:/Users/zxh/web22/cookies_rating.pkl", "rb") as file:
#     cookies = pickle.load(file)
#     for cookie in cookies:
#         driver.add_cookie(cookie)
# with open("data2.txt",'w',encoding='utf-8')as file2:
script = """
var div1 = document.querySelector('div.dq3izqp.atm_7l_12u4tyr.atm_cs_atq67q.atm_l8_1s5ai0k.dir.dir-ltr'); // 定位到第一个div
var text = div1.nextSibling.textContent; // 获取第一个div后的下一个兄弟节点的文本内容
return text;
"""


# 解析文本数据并存储到列表中
def parse(data):
    parsed_data = []
    for line in data:
        parts = line.split('。 ')
        record = {}
        for part in parts:
            key, value = part.split('：')
            record[key.strip()] = value.strip()
        parsed_data.append(record)
    return parsed_data
    
for i in range(0,1):
    cnt=0
    data = set()
    # 打开网页
    except_cnt=0
    driver.get(url_list[i]+"/?locale=en")
    listing_id = url_list[i].split('/')[-1]  # 分割URL并获取最后一部分
    filename = 'rate_res.csv'
    fieldnames = ['listing_id', 'listing_url', 'reviewer_id', 'date', 'reviewer_name','review_id', 'location', 'rating', 'response']
    file_exists = os.path.exists(filename) and os.path.getsize(filename) > 0
    # 使用WebDriverWait等待按钮可见
    time.sleep(2)
    try:
        btn_close=driver.find_element(By.XPATH, "//button[@aria-label='Close']")
        btn_close.click()
        time.sleep(0.6)
    except:
        pass
    try:
        btn2=driver.find_element(By.XPATH,"//button[contains(text(),'review')]")
        print(btn2.text)
        # btn2=wait.until(EC.visibility_of_element_located((By.XPATH,"//button[contains(text(),'review')]")))
        btn2.click()
    except Exception as e:
        except_cnt=except_cnt+1
        print(url_list[i])
        print("No more reviews")
    html_after_click = driver.page_source
    time.sleep(0.4)
    wait = WebDriverWait(driver,3)

    try:
        panel = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="pdp-reviews-modal-scrollable-panel"]')
    except:
        except_cnt=except_cnt+1
        if(except_cnt==2):
            with open(filename, 'a+', newline='', encoding='utf-8') as file3:
                # writer = csv.DictWriter(file3, fieldnames=['listing_id', 'listing_url', 'reviewer_id', 'reviewer_name','review_id', 'location', 'rating', 'response'])
                # writer.writerow(url_list[i]+" is invalid")
                # continue
                # writer = csv.writer(file3,fieldnames=fieldnames)
                writer = csv.DictWriter(file3, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                # 注意：writerow接受一个list作为参数
                # writer.writerow([url_list[i], "is invalid"])
                comments = driver.find_elements(By.CSS_SELECTOR, "div.rijjzz2")
                for comment in comments:
                    element = driver.find_element(By.CLASS_NAME, "t11wgnhd")    
                    # 获取元素的id属性值
                    element_id = element.get_attribute("id")

                    # 使用正则表达式从id属性中提取数字ID
                    match = re.search(r'review_(\d+)_title', element_id)
                    if match:
                        review_id = match.group(1)
                        print(review_id)
                    else:
                        print("ID not found")
                    reviewer_id= Extract_userid(comment)
                    date_text = driver.execute_script(script)
                    name_element = comment.find_element(By.CSS_SELECTOR, "h3.hpipapi")
                    name = name_element.text
                    location = comment.find_element(By.CSS_SELECTOR, "div.s9v16xq").text
                    try:
                        rating = comment.find_element(By.CSS_SELECTOR, "span.a8jt5op").text  
                    except NoSuchElementException:
                        rating = ""
                    try:
                        response_element = comment.find_element(By.CSS_SELECTOR, "div.rzrvevs")
                        response = remove_empty_lines(response_element.text)
                    except NoSuchElementException:
                        response = ""
                    data.add((f"listing_id：{listing_id}。 listing_url：{url_list[i]}。 reviewer_id：{reviewer_id}。 date：{date_text}。 reviewer_name：{name}。 review_id：{review_id}。 location：{location}。 rating：{rating}。 response：{response}"))
                    
                    parsed_data=parse(data)
                   
                    # writer = csv.DictWriter(file3, fieldnames=fieldnames)
                    # 如果文件不存在或为空，则写入header
                    
                    for row in parsed_data:
                        writer.writerow(row)

    if(except_cnt==2):
        continue
    last_height = driver.execute_script("return arguments[0].scrollHeight", panel)
    actions = ActionChains(driver)
    page=0
    while True: 
        page=page+1
        actions.move_to_element(panel).click().send_keys(Keys.PAGE_DOWN).perform()
        new_height = driver.execute_script("return arguments[0].scrollHeight", panel)
        # print(new_height)
        time.sleep(0.4)
        # wait = WebDriverWait(driver, 3) 
        if(page==10):
            page=0
            if(new_height==last_height):
                
                break
            last_height=new_height


        

    #     print(last_height)
    # while True:
    #     print(666)
    #     driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", panel)
    #     time.sleep(3)  # 等待页面加载新内容

    #     new_height = driver.execute_script("return arguments[0].scrollHeight", panel)
    #     print(new_height)
    #     if new_height == last_height:
    #         break
    #     last_height = new_height

        # last_height = driver.execute_script("return document.body.scrollHeight")
        # print(last_height)
        # while True:
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(3)  # 更长的等待时间确保内容加载
        #     new_height = driver.execute_script("return document.body.scrollHeight")
        #     print(new_height)
        #     if new_height == last_height:
        #         break
        #     last_height = new_height


        # # 执行滚动到底部的操作
        # last_height = driver.execute_script("return document.body.scrollHeight")
        # print("初始高度:", last_height)
        # while True:
        #     # 滚动到页面底部
        #     for y in range(last_height, last_height + 1000, 200):
        #         driver.execute_script(f"window.scrollTo(0, {y});")
        #         time.sleep(0.5)  # 短暂等待
        #         print("执行了滚动")
        #     # 等待新内容加载
        #     time.sleep(3)

        #     # 计算新的滚动高度并比较
        #     new_height = driver.execute_script("return document.body.scrollHeight")
        #     print("新高度:", new_height)
        #     if new_height == last_height:
        #         print("到达页面底部")
        #         break
        #     last_height = new_height
            
                # 初始化一个集合用来跟踪已处理的评论ID
            # while True:
        #     try:
        #         more_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Show more')]")
        #         more_btn.click()
        #         time.sleep(1)
        #     except:
        #         break
        # try:
        #     # 尝试找到第一个按钮并点击
        #     button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-testid="pdp-show-all-reviews-button"]')))
        #     button.click()
        # except Exception:
        #     print("评价不需要展开")
        #     # # 如果第一个按钮找不到，尝试找第二个按钮
        #     # try:
        #     #     button2 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.atm_1y33qqm_1ggndnn_10saat9")))
        #     #     button2.click()
        #     # except Exception as e:
        #     #     print("第二个按钮也找不到: ", e)
        # # button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-testid="pdp-show-all-reviews-button"]')))
        # # button2 = driver.find_element_by_css_selector("button.atm_1y33qqm_1ggndnn_10saat9")

        # # # 模拟点击按钮
        # # button.click()

        # time.sleep(10)
        # wait = WebDriverWait(driver, 10)
        # 获取点击按钮后的HTML内容
    html_after_click = driver.page_source

        # with open("page2.html",'w',encoding='utf-8')as file:
        #     file.write(html_after_click)


        # 定位评论的容器元素
    reviews_container = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="pdp-reviews-modal-scrollable-panel"]')

        # 在该容器内寻找所有评论
    comments = reviews_container.find_elements(By.CSS_SELECTOR, "div.r1are2x1.atm_gq_1vi7ecw.dir.dir-ltr")

    
    

    for comment in comments:
        # 根据你提供的结构，找到用户名、位置和评分
        # 注意：这里的选择器需要根据实际网页结构进行调整
            # username = comment.find_element(By.CSS_SELECTOR, "h3.hpipapi").text  
        review_id = comment.get_attribute("data-review-id")
        location = comment.find_element(By.CSS_SELECTOR, "div.s9v16xq").text
        date_text = comment.execute_script(script)
            
        try:
            rating = comment.find_element(By.CSS_SELECTOR, "span.a8jt5op").text  
        except NoSuchElementException:
            rating = ""
        listing_id = url_list[i].split('/')[-1]  # 分割URL并获取最后一部分
        reviewer_id= Extract_userid(comment)

        name_element = comment.find_element(By.CSS_SELECTOR, "h3.hpipapi")
        name = name_element.text
        listing_url=url_list[i]
            
        try:
            response_element = comment.find_element(By.CSS_SELECTOR, "div.rzrvevs")
            response = remove_empty_lines(response_element.text)
        except NoSuchElementException:
            response = ""
        finally:
            data.add(f"listing_id：{listing_id}。 listing_url：{listing_url}。 reviewer_id：{reviewer_id}。 date：{date_text}。 reviewer_name：{name}。 review_id：{review_id}。 location：{location}。 rating：{rating}。 response：{response}")
                # file2.write(f"listing_id：{listing_id}。 listing_url：{listing_url}。 reviewer_id：{reviewer_id}。 reviewer_name：{name}。 review_id：{review_id}。 location：{location}。 rating：{rating}。 response：{response}\n")

        cnt=cnt+1
            # file2.write('\n')

    # 解析文本数据并存储到列表中
    # parsed_data = []
    # for line in data:
    #     parts = line.split('。 ')
    #     record = {}
    #     for part in parts:
    #         key, value = part.split('：')
    #         record[key.strip()] = value.strip()
    #     parsed_data.append(record)
    parsed_data=parse(data)
        
    # filename = 'rate_res.csv'
    # fieldnames = ['listing_id', 'listing_url', 'reviewer_id', 'date', 'reviewer_name','review_id', 'location', 'rating', 'response']
    # 检查文件是否存在且不为空
    file_exists = os.path.exists(filename) and os.path.getsize(filename) > 0
        # 写入CSV文件
    with open('rate_res.csv', 'a+', newline='', encoding='utf-8') as file3:
        writer = csv.DictWriter(file3, fieldnames=fieldnames)
        # 如果文件不存在或为空，则写入header
        if not file_exists:
            writer.writeheader()
        for row in parsed_data:
            writer.writerow(row)
        
    
    print(cnt)
# 关闭WebDriver
driver.quit()

# 现在，html_after_click中包含了点击按钮后的HTML内容
