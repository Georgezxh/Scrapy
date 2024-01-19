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
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# 读取文件的前 100 行
df = pd.read_csv('src\guests1k.csv', nrows=100)

# 分别将 'reviewer_name' 和 'guest_url' 存储到两个列表中
reviewer_names = df['reviewer_name'].tolist()
guest_urls = df['guest_url'].tolist()

# 现在 reviewer_names 和 guest_urls 分别包含了前 100 个名字和网址


# 创建浏览器对象
driver = webdriver.Chrome()

# 打开目标网页
driver.get("https://www.airbnb.com/users/show/927861")

# 定位手机号码输入框
phone_input = driver.find_element(By.ID, "phoneInputphone-login")

# 向输入框发送手机号码
phone_input.send_keys("88854655")  # 替换为您实际要输入的手机号码


# 定位“发送验证码”按钮，这里需要替换为正确的定位方式
# 例如: find_element_by_id, find_element_by_name, find_element_by_xpath等
# 下面的例子使用的是假设的元素ID "send_code_btn"
# send_code_btn = driver.find_element_by_id("send_code_btn")
# send_code_btn = driver.find_element_by_class_name("atm_9s_1ulexfb")
send_code_btn = driver.find_element(By.CLASS_NAME, "atm_9s_1ulexfb")




# 点击按钮以发送验证码
send_code_btn.click()

# 暂停，等待用户手动输入验证码
# 这里的时间可以根据需要进行调整
time.sleep(20)  # 暂停30秒

# 在此处继续你的脚本，执行验证码输入后的操作
# ...


# 用户个人中心的URL列表


# urls = [
#     # "https://www.airbnb.com.sg/users/show/213502742",
#     # "https://www.airbnb.com.sg/users/show/46807714",
#     "https://www.airbnb.com.sg/users/show/211678505",
#     "https://www.airbnb.com.sg/users/show/46807714"
# ]

for i in range(0,3):
    driver.get(guest_urls[i]+"/?locale=en")
    name=reviewer_names[i]
    # 给页面加载留出足够的时间
    time.sleep(5)  # 可以根据网页的实际加载时间调整

    # 查找包含头像URL的<img>元素
    try:
        # 使用特定类名定位到<img>标签
        img_tags = driver.find_elements(By.CSS_SELECTOR, 'img.itu7ddv')
        for img_tag in img_tags:
            if '个人资料' in img_tag.get_attribute('alt'):
                avatar_url = img_tag.get_attribute('src')
                print(f"Found avatar URL for {name}: {avatar_url}")
                break
        else:
            print(f"No matching img tag found for {name}")
    except Exception as e:
        print(f"Error processing {name}: {e}")

    wait = WebDriverWait(driver,3 )

    btn2=driver.find_element(By.XPATH,"//button[contains(text(),'Show all')]")
    btn2.click()
    html_after_click = driver.page_source

    while True:
        try:
            # more_btn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "l1ovpqvx atm_1y33qqm_1ggndnn_10saat9 atm_17zvjtw_zk357r_10saat9 atm_w3cb4q_il40rs_10saat9 b1sef8f2 atm_9j_tlke0l atm_9s_1o8liyq atm_gi_idpfg4 atm_mk_h2mmj6 atm_r3_1h6ojuz atm_rd_glywfm atm_3f_97hwo atm_vy_1wugsn5 atm_tl_1gw4zv3 atm_9j_13gfvf7_1o5j5ji c3dg75g atm_bx_1ltc5j7 atm_c8_8ycq01 atm_g3_adnk3f atm_fr_rvubnj atm_cs_qo5vgd atm_5j_9l7fl4 atm_6h_t94yts atm_66_nqa18y atm_kd_glywfm atm_uc_1etn2gc atm_r2_1j28jx2 atm_jb_1fkumsa atm_4b_18pqv07 atm_26_1hbpp16 atm_7l_18pqv07 atm_l8_1vkzbvs atm_uc_glywfm__p88qr9 atm_kd_glywfm_1w3cfyq atm_uc_x37zl0_1w3cfyq atm_3f_glywfm_e4a3ld atm_l8_idpfg4_e4a3ld atm_gi_idpfg4_e4a3ld atm_3f_glywfm_1r4qscq atm_kd_glywfm_6y7yyg atm_uc_glywfm_1w3cfyq_p88qr9 atm_kd_glywfm_18zk5v0 atm_uc_x37zl0_18zk5v0 atm_3f_glywfm_6mgo84 atm_l8_idpfg4_6mgo84 atm_gi_idpfg4_6mgo84 atm_3f_glywfm_16p4kaz atm_kd_glywfm_17yx6rv atm_uc_glywfm_18zk5v0_p88qr9 atm_tr_18md41p_csw3t1 atm_k4_kb7nvz_1o5j5ji atm_4b_18pqv07_1w3cfyq atm_7l_18pqv07_1w3cfyq atm_70_216vci_1w3cfyq atm_4b_18pqv07_18zk5v0 atm_7l_18pqv07_18zk5v0 atm_70_216vci_18zk5v0 atm_4b_1otlplk_1nos8r_uv4tnr atm_26_1nh1gcj_1nos8r_uv4tnr atm_7l_18pqv07_1nos8r_uv4tnr atm_4b_161hw1_4fughm_uv4tnr atm_26_1hbpp16_4fughm_uv4tnr atm_7l_161hw1_4fughm_uv4tnr atm_4b_1otlplk_csw3t1 atm_26_1nh1gcj_csw3t1 atm_7l_18pqv07_csw3t1 atm_4b_161hw1_1o5j5ji atm_26_1hbpp16_1o5j5ji atm_7l_161hw1_1o5j5ji dir dir-ltr")))
            more_btn = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'Show more')]")))
            # more_btn = driver.find_element(By.CSS_SELECTOR, "button[role='button'][type='button']:contains('显示更多评价')")

            more_btn.click()
            # time.sleep(3)
            print(1)
        except:
            print("没找到按钮")
            break

    comments = driver.find_elements(By.CSS_SELECTOR, "div.cwt93ug")

    print("From guests:")
    for comment in comments:
        # 提取评论的 ID
        comment_id = comment.find_element(By.CSS_SELECTOR, "div.t126ex63").text
        # 提取评论的文本
        comment_text = comment.find_element(By.CSS_SELECTOR, "div.c1um7q2x").text

        print(f"ID: {comment_id}, Text: {comment_text}")


    btn2=driver.find_element(By.XPATH,"//button[contains(text(),'From hosts')]")
    btn2.click()
    while True:
        try:
            # more_btn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "l1ovpqvx atm_1y33qqm_1ggndnn_10saat9 atm_17zvjtw_zk357r_10saat9 atm_w3cb4q_il40rs_10saat9 b1sef8f2 atm_9j_tlke0l atm_9s_1o8liyq atm_gi_idpfg4 atm_mk_h2mmj6 atm_r3_1h6ojuz atm_rd_glywfm atm_3f_97hwo atm_vy_1wugsn5 atm_tl_1gw4zv3 atm_9j_13gfvf7_1o5j5ji c3dg75g atm_bx_1ltc5j7 atm_c8_8ycq01 atm_g3_adnk3f atm_fr_rvubnj atm_cs_qo5vgd atm_5j_9l7fl4 atm_6h_t94yts atm_66_nqa18y atm_kd_glywfm atm_uc_1etn2gc atm_r2_1j28jx2 atm_jb_1fkumsa atm_4b_18pqv07 atm_26_1hbpp16 atm_7l_18pqv07 atm_l8_1vkzbvs atm_uc_glywfm__p88qr9 atm_kd_glywfm_1w3cfyq atm_uc_x37zl0_1w3cfyq atm_3f_glywfm_e4a3ld atm_l8_idpfg4_e4a3ld atm_gi_idpfg4_e4a3ld atm_3f_glywfm_1r4qscq atm_kd_glywfm_6y7yyg atm_uc_glywfm_1w3cfyq_p88qr9 atm_kd_glywfm_18zk5v0 atm_uc_x37zl0_18zk5v0 atm_3f_glywfm_6mgo84 atm_l8_idpfg4_6mgo84 atm_gi_idpfg4_6mgo84 atm_3f_glywfm_16p4kaz atm_kd_glywfm_17yx6rv atm_uc_glywfm_18zk5v0_p88qr9 atm_tr_18md41p_csw3t1 atm_k4_kb7nvz_1o5j5ji atm_4b_18pqv07_1w3cfyq atm_7l_18pqv07_1w3cfyq atm_70_216vci_1w3cfyq atm_4b_18pqv07_18zk5v0 atm_7l_18pqv07_18zk5v0 atm_70_216vci_18zk5v0 atm_4b_1otlplk_1nos8r_uv4tnr atm_26_1nh1gcj_1nos8r_uv4tnr atm_7l_18pqv07_1nos8r_uv4tnr atm_4b_161hw1_4fughm_uv4tnr atm_26_1hbpp16_4fughm_uv4tnr atm_7l_161hw1_4fughm_uv4tnr atm_4b_1otlplk_csw3t1 atm_26_1nh1gcj_csw3t1 atm_7l_18pqv07_csw3t1 atm_4b_161hw1_1o5j5ji atm_26_1hbpp16_1o5j5ji atm_7l_161hw1_1o5j5ji dir dir-ltr")))
            more_btn = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), '显示更多评价')]")))
            # more_btn = driver.find_element(By.CSS_SELECTOR, "button[role='button'][type='button']:contains('显示更多评价')")

            more_btn.click()
            # time.sleep(3)
            print(1)
        except:
            print("没找到按钮")
            break

    print("From hosts:")
    for comment in comments:
        # 提取评论的 ID
        comment_id = comment.find_element(By.CSS_SELECTOR, "div.t126ex63").text
        # 提取评论的文本
        comment_text = comment.find_element(By.CSS_SELECTOR, "div.c1um7q2x").text
        print(f"ID: {comment_id}, Text: {comment_text}")



# 关闭浏览器
driver.quit()

