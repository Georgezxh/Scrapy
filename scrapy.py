# # # import requests
# # # from bs4 import BeautifulSoup

# # # # 用户个人中心的URL列表
# # # urls = [
# # #     # "https://www.airbnb.com.sg/users/show/213502742",
# # #     # "https://www.airbnb.com.sg/users/show/46807714",
# # #     # "https://www.airbnb.com.sg/users/show/211678505"
# # #     "https://www.airbnb.com.sg/users/show/46807714"
# # # ]



# # # # 遍历URL列表，提取每个页面中的头像URL

# # # for url in urls:
# # #     response = requests.get(url)
# # #     soup = BeautifulSoup(response.text, 'html.parser')
# # #     print(soup)
# # #     # 查找包含头像URL的元素
# # #     picture_tag = soup.find('picture')
# # #     # print(picture_tag)
# # #     if picture_tag:
# # #         source_tag = picture_tag.find('source')
# # #         if source_tag and 'srcset' in source_tag.attrs:
# # #             avatar_url = source_tag['srcset'].split(' ')[0]
# # #             print(f"Found avatar URL for {url}: {avatar_url}")
# # #         else:
# # #             print(f"No avatar URL found in source tag for {url}")
# # #     else:
# # #         print(f"No picture tag found for {url}")



# # # import requests

# # # # 第一步：自动发送验证码
# # # def send_verification_code(phone_number):
# # #     url = 'https://www.airbnb.com.sg/api/v2/phone_one_time_passwords?key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=SGD&locale=en-SG'
# # #     data = {
# # #         'phone': phone_number,  # 可能需要根据网站的实际要求调整字段名称
# # #     }
# # #     response = requests.post(url, data=data)
# # #     return response

# # # # 第二步：手动输入验证码
# # # def manual_login(phone_number, verification_code):
# # #     login_url = 'https://www.airbnb.com.sg/users/show/46807714'
# # #     login_data = {
# # #         'phone': phone_number,
# # #         'code': verification_code,  # 根据网站的字段进行调整
# # #     }
# # #     response = requests.post(login_url, data=login_data)
# # #     return response

# # # # 使用示例
# # # phone_number=88854655
# # # # phone_number = input("请输入手机号码: ")
# # # send_verification_code(phone_number)

# # # verification_code = input("请输入收到的验证码: ")
# # # response = manual_login(phone_number, verification_code)

# # # if response.ok:
# # #     print("登录成功")
# # # else:
# # #     print("登录失败")


from selenium import webdriver
# from selenium.webdriver.common.by import By
# import requests
# from bs4 import BeautifulSoup

# import time
# import pandas as pd

# # 读取文件的前 100 行
# df = pd.read_csv('src\guests1k.csv', nrows=100)

# # 分别将 'reviewer_name' 和 'guest_url' 存储到两个列表中
# reviewer_names = df['reviewer_name'].tolist()
# guest_urls = df['guest_url'].tolist()

# # 现在 reviewer_names 和 guest_urls 分别包含了前 100 个名字和网址


# # 创建浏览器对象
# driver = webdriver.Chrome()

# # 打开目标网页
# driver.get("https://www.airbnb.com/users/show/927861")

# # 定位手机号码输入框
# phone_input = driver.find_element(By.ID, "phoneInputphone-login")

# # 向输入框发送手机号码
# phone_input.send_keys("88854655")  # 替换为您实际要输入的手机号码


# # 定位“发送验证码”按钮，这里需要替换为正确的定位方式
# # 例如: find_element_by_id, find_element_by_name, find_element_by_xpath等
# # 下面的例子使用的是假设的元素ID "send_code_btn"
# # send_code_btn = driver.find_element_by_id("send_code_btn")
# # send_code_btn = driver.find_element_by_class_name("atm_9s_1ulexfb")
# send_code_btn = driver.find_element(By.CLASS_NAME, "atm_9s_1ulexfb")




# # 点击按钮以发送验证码
# send_code_btn.click()

# # 暂停，等待用户手动输入验证码
# # 这里的时间可以根据需要进行调整
# time.sleep(20)  # 暂停30秒

# # 在此处继续你的脚本，执行验证码输入后的操作
# # ...


# # 用户个人中心的URL列表


# # urls = [
# #     # "https://www.airbnb.com.sg/users/show/213502742",
# #     # "https://www.airbnb.com.sg/users/show/46807714",
# #     "https://www.airbnb.com.sg/users/show/211678505",
# #     "https://www.airbnb.com.sg/users/show/46807714"
# # ]

# for i in range(0,100):
#     driver.get(guest_urls[i])
#     name=reviewer_names[i]
#     # 给页面加载留出足够的时间
#     time.sleep(5)  # 可以根据网页的实际加载时间调整

#     # 查找包含头像URL的<img>元素
#     try:
#         # 使用特定类名定位到<img>标签
#         img_tags = driver.find_elements(By.CSS_SELECTOR, 'img.itu7ddv')
#         for img_tag in img_tags:
#             if '个人资料' in img_tag.get_attribute('alt'):
#                 avatar_url = img_tag.get_attribute('src')
#                 print(f"Found avatar URL for {name}: {avatar_url}")
#                 break
#         else:
#             print(f"No matching img tag found for {name}")
#     except Exception as e:
#         print(f"Error processing {name}: {e}")



# # 关闭浏览器
# driver.quit()

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 创建一个WebDriver实例，使用Chrome浏览器
driver = webdriver.Chrome()

# 打开网页
driver.get('https://zh.airbnb.com/rooms/2708?_set_bev_on_new_domain=1705246965_ZDhmNjNlODM0Y2M3&source_impression_id=p3_1705506457_S9U%2Fx1IzhjD%2BQb62')

# 使用WebDriverWait等待按钮可见
# wait = WebDriverWait(driver, 10)
# button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-testid="pdp-show-all-reviews-button"]')))

# 模拟点击按钮
# button.click()

# 获取点击按钮后的HTML内容
html_after_click = driver.page_source

# 关闭WebDriver
driver.quit()

# 现在，html_after_click中包含了点击按钮后的HTML内容
print(html_after_click)



