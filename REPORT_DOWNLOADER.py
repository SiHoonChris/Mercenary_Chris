# 국내주식, 미국주식 공시/보고서 다운로더
# 1) 보유종목과 관심종목에 대한 공시/보고서를 사이트에 들어가서 일일이 확인하기 귀찮음
# 2) 공시/보고서가 언제 올라올지도 모르는데 매일 들어가서 확인하기도 번거로움
#    1), 2)를 해결하기 위해...
#       a). 원하는 기간 입력하여 해당 기간에 대한 데이터 다 가져오기
#       b). 중요한 내용(10-K, 10-Q, 사업보고서, 분기/반기 보고서, 연결재무제표 등)은 링크 다운로드 
# * CIK, 종목코드 검색 가능하게 만들기??? / 보유 종목에 대한 내용 하나하나 기록해두기 귀찮음


# 0. 모듈/패키지
from bs4 import BeautifulSoup
headers=" "

from selenium import webdriver
options = webdriver.ChromeOptions()
options.headless = False
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent="+headers)
browser=webdriver.Chrome(options=options)

import datetime
From_date=datetime.date(2021,1,1)
To_date=datetime.date(2022,1,1)
# 개선1 : input 활용하여, 프로그램 작동 시 사용자가 원하는 날짜 입력할 수 있도록 수정


# 1. 미국 주식
def us_report(*CIKs):
    for CIK in CIKs:
        url = "https://www.sec.gov/edgar/browse/?CIK={}&owner=exclude".format(CIK)
        browser.get(url)
        browser.find_element_by_xpath("//*[@id='btnViewAllFilings']").click()  # seleium으로 웹페이지 세팅

        soup = BeautifulSoup(browser.page_source, "lxml")  # beautifulsoup으로 웹페이지 정보 가져오기
        name=soup.find("span", attrs={"id":"name"})  # 종목명 가져오기
        print(name.get_text())
        number_of_lists=soup.find("tbody").find_all("tr")  # Filings내 table의 row들 갯수 파악 
        for i in range(0, len(number_of_lists)):  # table의 row들 갯수 바탕으로 넘버 부여(i)
            filing_dates=soup.find("tbody").find_all("td", attrs={"class":"sorting_1"})[i].get_text()  # filing date 열 내용(날짜) 출력
            if str(From_date) <= filing_dates <= str(To_date):
                print(filing_dates)
            else:
                # print("out of preiod-range")
                continue
        
        print("-"*100)

us_report("320193", "1652044", "320193", "789019", "1018724", "1326801")
# 문제!!! : CIK가 320193만 출력되고, 그 다음부터는 에러남. 나머지 CIK에 대한 내용 출력 불가


# 2. 국내 주식


# 3. 다 끌어오기

