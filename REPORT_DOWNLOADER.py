# 국내주식, 미국주식 공시/보고서 다운로더
# 1) 보유종목과 관심종목에 대한 공시/보고서를 사이트에 들어가서 일일이 확인하기 귀찮음
# 2) 공시/보고서가 언제 올라올지도 모르는데 매일 들어가서 확인하기도 번거로움
#    1), 2)를 해결하기 위해...
#       a). 원하는 기간 입력하여 해당 기간에 대한 데이터 다 가져오기
#       b). 중요한 내용(10-K, 10-Q, 사업보고서, 분기/반기 보고서, 연결재무제표 등)은 링크 다운로드 
# * CIK, 종목코드 검색 가능하게 만들기??? / 보유 종목에 대한 내용 하나하나 기록해두기 귀찮음



# 0. 모듈/패키지
from bs4 import BeautifulSoup
headers="Mozilla/5.0"

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
        number_of_lists=soup.find("tbody").find_all("tr")  # Filings내 table의 row들 갯수 파악

        cnt=0
        for i in range(0, len(number_of_lists)):
            filing_dates=soup.find("tbody").find_all("td", attrs={"class":"sorting_1"})[i].get_text()  # 파일링된 날짜 출력
            if str(From_date) <= filing_dates <= str(To_date):
                cnt+=1
        print("[{0}]({1})".format(name.get_text(), cnt))

        for idx, i in enumerate(range(0, len(number_of_lists)), start=1):  # table의 row들 갯수 바탕으로 넘버 부여(i)
            form_types=soup.find("tbody").find_all("td", attrs={"class":"dtr-control"})[i].get_text()  # 내용 타입
            form_descriptions=soup.find("tbody").find_all("a", attrs={"class":"document-link"})[i].get_text().replace("Open document", "")  #  내용 제목
            links=soup.find("tbody").find_all("a", attrs={"class":"document-link"})[i]["href"]  # 내용에 대한 링크
            filing_dates=soup.find("tbody").find_all("td", attrs={"class":"sorting_1"})[i].get_text()  # 파일링된 날짜 출력
            if str(From_date) <= filing_dates <= str(To_date):
                print("   {0}. [{1}] ".format(idx, form_types), form_descriptions, " ({0})".format(filing_dates))
                print("      https://www.sec.gov/"+links)
            else:
                continue
        
        print("-"*100)
# 개선2 : 출력문 관련
#         1) 종목명 옆에 가져온 파일 갯수 표시, 예시 : [Apple Inc.](5)
#         2) 가져온 파일 정보 앞에 번호 붙이기, 예시 : 1.  [8-K]    Current report  (2022-06-03)
#         3) form_type, description, filing date 정렬
# 해결2 : 출력문 관련
#         1) 새 변수 cnt 부여
#         2) len(number_of_lists)에 대한 enumerate 사용, start=1
#         3) Example)
#            1. [S-8]  Securities to be offered to employees in employee benefit plans  (2022-04-29) 
#               https://www.sec.gov//Archives/edgar/data/0000320193/000119312522128368/d332661ds8.htm

# 개선3 : 출력문 관련
#         1) 출력된 파일이 9개가 넘어가니까 원하는 출력문 형식이 살짝 깨짐

# CIKs : 320193 AAPL /  1018724 AMZN / 1652044 GOOGL / 200406 JNJ / 21344 KO / 936468 LMT / 789019 MSFT
us_report("320193", "1018724", "1652044", "200406", "21344", "936468", "789019")
# 문제!!! : GOOGL은 3번부터, LMT는 2번부터 파일 번호 출력. 왜???



# 2. 국내 주식
# 3. 다 끌어오기