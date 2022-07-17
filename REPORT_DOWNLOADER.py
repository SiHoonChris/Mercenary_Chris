# 0. 모듈/패키지
from bs4 import BeautifulSoup
headers=" "

from selenium import webdriver
options = webdriver.ChromeOptions()
options.headless = False
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent="+headers)
browser=webdriver.Chrome(options=options)
import time

import datetime
From_date=datetime.date(2022,4,1)
To_date=datetime.date(2022,7,1)
# 개선1 : input 활용하여, 프로그램 작동 시 사용자가 원하는 날짜 입력할 수 있도록 수정


def us_report(*CIKs):
    for CIK in CIKs:
        url = "https://www.sec.gov/edgar/browse/?CIK={}&owner=exclude".format(CIK)
        browser.get(url)
        time.sleep(3)
        browser.find_element_by_xpath("//*[@id='btnViewAllFilings']").click()  # seleium으로 웹페이지 세팅
        time.sleep(3)

        soup = BeautifulSoup(browser.page_source, "lxml")  # beautifulsoup으로 웹페이지 정보 가져오기
        name=soup.find("span", attrs={"id":"name"})  # 종목명 가져오기
        print("[{0}]".format(name.get_text()))

        number_of_lists=soup.find("tbody").find_all("tr")  # Filings내 table의 row들 갯수 파악 
        for i in range(0, len(number_of_lists)):  # table의 row들 갯수 바탕으로 넘버 부여(i)
            form_types=soup.find("tbody").find_all("td", attrs={"class":"dtr-control"})[i].get_text()  # 내용 타입
            form_descriptions=soup.find("tbody").find_all("a", attrs={"class":"document-link"})[i].get_text().replace("Open document", "")  #  내용 제목
            links=soup.find("tbody").find_all("a", attrs={"class":"document-link"})[i]["href"]  # 내용에 대한 링크
            filing_dates=soup.find("tbody").find_all("td", attrs={"class":"sorting_1"})[i].get_text()  # 파일링된 날짜 출력
            if str(From_date) <= filing_dates <= str(To_date):
                print("   [{0}]{1:<3}".format(form_types, ""), form_descriptions, " ({0})".format(filing_dates))
                print("   https://www.sec.gov/"+links)
            else:
                continue

        print("-"*100)
# 개선2 : 출력문 관련
#         1) 종목명 옆에 가져온 파일 갯수 표시, 예시 : [Apple Inc.](5)
#         2) 가져온 파일 정보 앞에 번호 붙이기, 예시 : 1.  [8-K]    Current report  (2022-06-03)
#         3) form_type, description, filing date 정렬


# CIKs : 320193 AAPL /  1018724 AMZN / 1652044 GOOGL / 200406 JNJ / 21344 KO / 936468 LMT / 789019 MSFT
us_report("320193", "1018724", "1652044", "200406", "21344", "936468", "789019")
# 문제 1) : CIK가 320193만 출력되고, 그 다음부터는 에러남. 나머지 CIK에 대한 내용 출력 불가
# 해결 1) : time.sleep 사용 // 인터넷 속도에 비해 프로그램 작동 속도가 더 빠름(페이지가 제대로 뜨기 전에 프로그램 작동)


# 2. 국내 주식
# 3. 다 끌어오기

