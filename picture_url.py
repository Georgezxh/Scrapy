from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import re
import csv
import pickle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def format_data(data):
    parsed_data=[]
    for line in data:
        parts = line.split('。 ')
        record = {}
        for part in parts:
            try:
                key, value = part.split('：')
                record[key.strip()] = value.strip()
            except:
                print(part)
        parsed_data.append(record)
        
    
    # 写入CSV文件
    with open('guest_comments2.csv', 'a+', newline='', encoding='utf-8') as file3:
        writer = csv.DictWriter(file3, fieldnames=['reviewer_id', 'reviewer_name', 'reviewer_url', 'reviewer_pictureurl', 'review_text','review_from', 'review_from_username', 'review_from_ID', 'response_text'])
        writer.writeheader()
        for row in parsed_data:
            print(row)
            writer.writerow(row)

def Extract_userid(comment):
    a_tag = comment.find_element(By.CSS_SELECTOR, "a[href*='/users/show/']")
    href = a_tag.get_attribute('href')
    
    # 使用正则表达式从 href 中提取数字
    match = re.search(r'/users/show/(\d+)', href)
    reviewer_id = match.group(1)
    return reviewer_id

def process_data(comments,data,current_page):
    for comment in comments:
        review_from_ID = Extract_userid(comment)
        # 提取评论的 reviewer_id
        reviewer_from_username = comment.find_element(By.CSS_SELECTOR, "div.t126ex63").text
        # 提取评论的文本
        comment_text = comment.find_element(By.CSS_SELECTOR, "div.c1um7q2x").text
        # if comment_text in data or comment_text=="":
        #     continue
            # data.add(comment_text)
            # print(f"reviewer_name：{reviewer_name}, reviewer_id：{reviewer_id}, Text：{comment_text}")

        response_index = comment.text.find("Response from")
        # 如果找到了 "Response from"
        if response_index != -1 and comment.text.find('\n', response_index)!=-1:
            # 查找紧随其后的第一个换行符的位置
            newline_index = comment.text.find('\n', response_index)

            # 如果找到了换行符
            # if newline_index != -1:
                # 提取该换行符之后的所有内容（即日期之后的文本）
            response_content = comment.text[newline_index + 1:]
            index=response_content.find('\n')
            res=response_content[index+1:]
            last_index=res.find('\n')
            res=res[:last_index]
            s="review_from_ID："+review_from_ID+", response_text："+res
            # if s not in data:
            data.add(f"reviewer_name：{name}。 reviewer_id：{host_id}。 reviewer_url：{guest_urls[i]}。 reviewer_pictureurl：{avatar_url}。 review_text：{comment_text}。 review_from：{current_page}。 review_from_username：{reviewer_from_username}。 review_from_ID：{review_from_ID}。 response_text：{res}")
            # print(f"reviewer_name： Response from {name}, User_id：{host_id}, Adressed to：{reviewer_id}, Text：{res}")
                # print(f"reviewer_name：{name}。 reviewer_id：{host_id}。 reviewer_url：{guest_urls[i]}。 reviewer_pictureurl：{avatar_url}。 review_text：{comment_text}。 review_from：{current_page}。 review_from_username：{reviewer_from_username}。 review_from_ID：{review_from_ID}。 response_text：{res}")
            # else:
                # print("未找到换行符")
        else:
            # print("未找到 'Response from'")
            # if res not in data and review_from_ID not in data:
            data.add(f"reviewer_name：{name}。 reviewer_id：{host_id}。 reviewer_url：{guest_urls[i]}。 reviewer_pictureurl：{avatar_url}。 review_text：{comment_text}。 review_from：{current_page}。 review_from_username：{reviewer_from_username}。 review_from_ID：{review_from_ID}。 response_text： ")
            # print(f"reviewer_name：{name}。 reviewer_id：{host_id}。 reviewer_url：{guest_urls[i]}。 reviewer_pictureurl：{avatar_url}。 review_text：{comment_text}。 review_from：{current_page}。 review_from_username：{reviewer_from_username}。 review_from_ID：{review_from_ID}。 response_text： ")
            # else:

# 读取文件的前 100 行
df = pd.read_csv('src\guests.csv', nrows=100)

# 分别将 'reviewer_name' 和 'guest_url' 存储到两个列表中
reviewer_names = df['reviewer_name'].tolist()
guest_urls = df['guest_url'].tolist()

# 现在 reviewer_names 和 guest_urls 分别包含了前 100 个名字和网址

# 创建浏览器对象
# options = webdriver.ChromeOptions()
# chrome_options = Options()
# chrome_options.add_argument(“)
# driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome()

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome()


# 打开目标网页
driver.get("https://www.airbnb.com/users/show/927861")
# 定位手机号码输入框
# phone_input = driver.find_element(By.ID, "phoneInputphone-login")

# 向输入框发送手机号码
# phone_input.send_keys("88854655")  # 替换为您实际要输入的手机号码

# 定位“发送验证码”按钮，这里需要替换为正确的定位方式
# 例如: find_element_by_id, find_element_by_name, find_element_by_xpath等
# send_code_btn = driver.find_element(By.CLASS_NAME, "atm_9s_1ulexfb")

# 点击按钮以发送验证码
# send_code_btn.click()

# 暂停，等待用户手动输入验证码
# 这里的时间可以根据需要进行调整
# time.sleep(3)  # 暂停3秒

with open("C:/Users/zxh/web22/cookies.pkl", "rb") as file:
    cookies = pickle.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)

for i in range(0,1):
    driver.get(guest_urls[i]+"/?locale=en")
    name=reviewer_names[i]
    # 给页面加载留出足够的时间
    time.sleep(2)  # 可以根据网页的实际加载时间调整

    except_cnt=0
    match = re.search(r'/users/show/(\d+)', guest_urls[i])
    host_id = match.group(1)
    avatar_url=0
    # 查找包含头像URL的<img>元素
    try:
        # 使用特定类名定位到<img>标签
        img_tags = driver.find_elements(By.CSS_SELECTOR, 'img.itu7ddv')
        for img_tag in img_tags:
            if 'User Profile' in img_tag.get_attribute('alt'):
                avatar_url = img_tag.get_attribute('src')
                print(f"Found avatar URL for {name}(id：{host_id})：{avatar_url}")
                break
        else:
            except_cnt=except_cnt+1
            print(f"No matching img tag found for {name}")
    except Exception as e:
        print(f"Error processing {name}：{e}")

    wait = WebDriverWait(driver,3 )
    try:
        btn2=driver.find_element(By.XPATH,"//button[contains(text(),'review')]")
        print(btn2.text)
        btn2.click()
    except Exception as e:
        except_cnt=except_cnt+1
        print("该页面不可用")
        with open('guest_comments.csv', 'a+', newline='', encoding='utf-8') as file4:
            file4.write(name+" is invalid")
        if except_cnt==2:
            continue
    html_after_click = driver.page_source
    time.sleep(2)
    wait = WebDriverWait(driver,3)

    # while True:
    #     # more_btn = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'Show more')]")))
    #     more_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Show more')]")
    #     print(more_btn)
    #     print("点击查看更多")
    #     driver.execute_script("arguments[0].click();",more_btn)       
    #     driver.execute_script("arguments[0].scrollIntoView(true);", more_btn)

    #     # more_btn.click()
    #     time.sleep(1)

    
    # 初始化一个集合用来跟踪已处理的评论ID
    while True:
        try:
            more_btn = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'Show more')]")))
            print("点击查看更多")
            more_btn.click()
            time.sleep(1)
        except:
            print("！！！！")
            break

    comments = driver.find_elements(By.CSS_SELECTOR, "div.cwt93ug")
    reviews = driver.find_elements(By.CSS_SELECTOR, "div.cu8gfs0")

    current_page=""
    guest_page=0
    host_page=0
    flag=0
    try:
        guests_btn = driver.find_element(By.ID, "tab--user-profile-review-tabs--0")
        if guests_btn.get_attribute("aria-selected") == "true":
            current_page="guests"
            flag=1
            print("当前页面: From guests")
        else:
            print("未在 'From guests' 页面")
        guest_page=1
    except NoSuchElementException:
        print("未找到 'From guests' 按钮")

    try:
        hosts_btn = driver.find_element(By.ID, "tab--user-profile-review-tabs--1")
        if hosts_btn.get_attribute("aria-selected") == "true":
            current_page="hosts"
            flag=2
            print("当前页面: From hosts")
        else:
            print("未在 'From hosts' 页面")
        host_page=1
    except NoSuchElementException:
        print("未找到 'From hosts' 按钮")

    
    # 初始化一个集合用来跟踪已处理的评论ID
    data = set()
    print(f"From {current_page} ")
    for comment in comments:
        review_from_ID = Extract_userid(comment)

        # 提取评论的 review_from_ID
        reviewer_from_username = comment.find_element(By.CSS_SELECTOR, "div.t126ex63").text
        # 提取评论的文本
        comment_text = comment.find_element(By.CSS_SELECTOR, "div.c1um7q2x").text
        if comment_text not in data and comment_text!="":
            # data.add(comment_text)
            # print(f"reviewer_name：{name}。 reviewer_id：{host_id}。 reviewer_url：{guest_urls[i]}。 reviewer_pictureurl：{avatar_url}。 review_text：{comment_text}。 review_from: guest。 review_from_username：{reviewer_from_username}。 review_from_ID：{review_from_ID}")

            response_index = comment.text.find("Response from")
            # 如果找到了 "Response from"
            if response_index != -1 and comment.text.find('\n', response_index)!=-1:
                # 查找紧随其后的第一个换行符的位置
                newline_index = comment.text.find('\n', response_index)

                # 如果找到了换行符
                # if newline_index != -1:
                    # 提取该换行符之后的所有内容（即日期之后的文本）
                response_content = comment.text[newline_index + 1:]
                index=response_content.find('\n')
                res=response_content[index+1:]
                last_index=res.find('\n')
                res=res[:last_index]
                data.add(f"reviewer_name：{name}。 reviewer_id：{host_id}。 reviewer_url：{guest_urls[i]}。 reviewer_pictureurl：{avatar_url}。 review_text：{comment_text}。 review_from：{current_page}。 review_from_username：{reviewer_from_username}。 review_from_ID：{review_from_ID}。 response_text：{res}")
                # print(f"reviewer_name: Response from {name}, User_id：{host_id}, Adressed to：{reviewer_id}, Text：{res}")
                # print(f"reviewer_name：{name}。 reviewer_id：{host_id}。 reviewer_url：{guest_urls[i]}。 reviewer_pictureurl：{avatar_url}。 review_text：{comment_text}。 review_from：{current_page}。 review_from_username：{reviewer_from_username}。 review_from_ID：{review_from_ID}。 response_text：{res}")
            else: 
                data.add(f"reviewer_name：{name}。 reviewer_id：{host_id}。 reviewer_url：{guest_urls[i]}。 reviewer_pictureurl：{avatar_url}。 review_text：{comment_text}。 review_from：{current_page}。 review_from_username：{reviewer_from_username}。 review_from_ID：{review_from_ID}。 response_text： ")
                # print(f"reviewer_name：{name}。 reviewer_id：{host_id}。 reviewer_url：{guest_urls[i]}。 reviewer_pictureurl：{avatar_url}。 review_text：{comment_text}。 review_from：{current_page}。 review_from_username：{reviewer_from_username}。 review_from_ID：{review_from_ID}。 response_text: ")
            

    length=len(data)
    # print(f"flag：{flag}")
    print(f"guest_page：{guest_page}")
    print(f"host_page：{host_page}")
    print(f"{current_page} has "+str(length)+" reviews" )
    if(flag==1 and host_page==1):
        btn2=driver.find_element(By.XPATH,"//button[contains(text(),'From hosts')]")
        btn2.click()
        current_page="hosts"
        print("到了host页面")
    elif ((flag==2 and host_page==0) or (flag==2 and guest_page==0)):
        format_data(data)
        continue
    elif (flag==1 and host_page==0):
        format_data(data)
        continue

    # try:
    #     btn2=driver.find_element(By.XPATH,"//button[contains(text(),'From hosts')]")
    #     btn2.click()
    # except Exception as e:
    #     print("From hosts not found")
        # parsed_data = []
        # for line in data:
        #     parts = line.split('。 ')
        #     record = {}
        #     for part in parts:
        #         key, value = part.split(': ')
        #         record[key.strip()] = value.strip()
        # parsed_data.append(record)

        # with open('guest_comments.csv', 'w', newline='', encoding='utf-8') as file3:
        #     writer = csv.DictWriter(file3, fieldnames=['reviewer_id', 'reviewer_name', 'reviewer_url', 'reviewer_picture_url', 'review_text','review_from', 'review_from_username', 'review_from_ID', 'reponse_text'])
        #     writer.writeheader()
        # for row in parsed_data:
        #     print(row)
        #     writer.writerow(row)
        # continue
        # break
    while True:
        try:
            more_btn = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'Show more')]")))
            # more_btn = driver.find_element(By.CSS_SELECTOR, "button[role='button'][type='button']:contains('显示更多评价')")
            print("第二个页面点击查看更多")
            more_btn.click()
            # WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Show more')]")))
            time.sleep(1)

        except:
            print("第二个！！！")
            break
    # comments = driver.find_elements(By.CSS_SELECTOR, "div.cwt93ug")
    print(f"From {current_page} ")
    data2 = set()
    process_data(comments,data2,current_page)
    format_data(data2)

    print("Hosts has "+str(len(data)-length)+" reviews" )


# 关闭浏览器
driver.quit()

