# 원/달러 환율 데이터 정리
# a) 환율 정보 끌어와서 엑셀로 정리, 차트 만들기
#    (엑셀자료는 웹페이지에서도 받을 수 있음. 내가 원하는건 한 번에 차트까지 만들어지는거)
# b) open/close/high/low/end price 다 갖고 와서 캔들차트 만들기 / 일, 주, 월봉

from bs4 import BeautifulSoup
headers="Mozilla/5.0"
from selenium import webdriver
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent="+headers)
browser=webdriver.Chrome(options=options)
from datetime import datetime
import time

# a)
url = "https://kr.investing.com/currencies/usd-krw-historical-data"
browser.get(url)
browser.find_element_by_xpath("//*[@id='flatDatePickerCanvasHol']").click()
browser.find_element_by_id("startDate").clear()
browser.find_element_by_id("startDate").send_keys("2022/01/01")
browser.find_element_by_id("endDate").clear()
today=datetime.now().date()
browser.find_element_by_id("endDate").send_keys(str(today))
browser.find_element_by_xpath("//*[@id='applyBtn']").click()
time.sleep(3)

soup = BeautifulSoup(browser.page_source, "lxml")
all_lists=soup.find("tbody").find_all("tr")
for i in range(0, len(all_lists)):
    dates=all_lists[i].find_all("td")[0].get_text().replace("년 ", "-").replace("월 ", "-").replace("일", "")
    day_fx=all_lists[i].find_all("td")[1].get_text().replace(",", "")
    print(f"[{dates}]  {day_fx}")
# 문제 : 프로그램 작동 중에 마우스 움직임 감지되면 로그인 팝업 뜸
