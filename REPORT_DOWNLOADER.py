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
import time

import datetime
From_date=datetime.date(2022,4,1)
To_date=datetime.date(2022,7,1)
# 개선1 : input 활용하여, 프로그램 작동 시 사용자가 원하는 날짜 입력할 수 있도록 수정


def us_report(*CIKs):

    browser=webdriver.Chrome(options=options)

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
        print("[{0}]({1})".format(name.get_text(), cnt))  # [종목명](조건에 맞는 파일 수)

        for idx, i in enumerate(range(0, len(number_of_lists)), start=1):  # table의 row들 갯수 바탕으로 넘버 부여(i)
            form_types=soup.find("tbody").find_all("td", attrs={"class":"dtr-control"})[i].get_text()  # 내용 타입
            form_descriptions=soup.find("tbody").find_all("a", attrs={"class":"document-link"})[i].get_text().replace("Open document", "")  #  내용 제목
            links=soup.find("tbody").find_all("a", attrs={"class":"document-link"})[i]["href"]  # 내용에 대한 링크
            filing_dates=soup.find("tbody").find_all("td", attrs={"class":"sorting_1"})[i].get_text()  # 파일링된 날짜 출력
            if str(From_date) <= filing_dates <= str(To_date):
                print("   {0}. [{1}] ".format(idx, form_types), form_descriptions, " ({0})".format(filing_dates))
                if idx < 10:
                    print("      https://www.sec.gov"+links)
                else:
                    print("       https://www.sec.gov"+links)
            else:
                continue
        
        print("-"*100)

    print("--- END ---\n")
    browser.quit()
# 문제!!! : GOOGL은 3번부터, LMT는 2번부터 파일 번호 출력. 왜???


# 2. 국내 주식
def kr_report(*CODEs):

    browser=webdriver.Chrome(options=options)

    for CODE in CODEs:
        url="https://dart.fss.or.kr/"
        browser.get(url)
        time.sleep(3)
        browser.find_element_by_xpath("//*[@id='textCrpNm2']").send_keys(CODE)
        browser.find_element_by_xpath("//*[@id='searchForm2']/div[1]/div[3]/a").click()
        time.sleep(3)
        Start_date=str(From_date).replace("-", "")
        End_date=str(To_date).replace("-", "")
        browser.find_element_by_xpath("//*[@id='startDate']").clear()
        browser.find_element_by_xpath("//*[@id='startDate']").send_keys(Start_date)
        browser.find_element_by_xpath("//*[@id='endDate']").clear()
        browser.find_element_by_xpath("//*[@id='endDate']").send_keys(End_date)
        browser.find_element_by_xpath("//*[@id='maxResultsCb']/option[4]").click()  # 조회건수 100으로 설정
        browser.find_element_by_xpath("//*[@id='searchForm']/div[2]/div[2]/a[1]").click()  # selenium으로 웹페이지 설정
        time.sleep(3)

        soup = BeautifulSoup(browser.page_source, "lxml")  # beautifulsoup으로 웹페이지 정보 가져오기
        name = soup.find("span", attrs={"class":"innerWrap"}).find("a").get_text().strip()
        number_of_lists=soup.find("tbody").find_all("tr")
        print("[{0}]({1})".format(name, len(number_of_lists)))  # [종목명](조건에 맞는 파일 수)

        for idx, i in enumerate(range(0, len(number_of_lists)), start=1):
            file_name=soup.find("tbody").find_all("tr")[i].find_all("td", attrs={"class":"tL"})[1].find("a")
            file_names=file_name.get_text().strip()
            filing_dates=soup.find("tbody").find_all("tr")[i].find_all("td")[4].get_text()
            links=file_name["href"]
            print("   {0:<3} {1}  ({2})".format(str(idx)+".", file_names, filing_dates))
            if idx < 10:
                print("      https://dart.fss.or.kr"+links)
            else:
                print("       https://dart.fss.or.kr"+links)

        print("-"*100)

    print("--- END ---\n")
    browser.quit()
# 문제!!! : 가져올 분량이 1페이지를 넘어갈 수도 있음(2,3, ...) / 모든 페이지의 내용 갖고 오기 위한 추가적인 코드 필요
# 개선2 : "--- END ---" 이후에, 총합 1)몇 개의 종목과, 2) 몇 개의 파일을 가져왔는지 표시/출력


# 3. 다 끌어오기
us_report("320193", "1018724", "1652044", "200406", "21344", "936468", "789019")
kr_report("005930", "000660")
# CIKs : 320193 AAPL /  1018724 AMZN / 1652044 GOOGL / 200406 JNJ / 21344 KO / 936468 LMT / 789019 MSFT
# CODE : 005930 삼성전자, 000660 SK하이닉스