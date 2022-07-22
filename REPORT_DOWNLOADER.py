# 국내주식, 미국주식 공시/보고서 다운로더
# 1) 보유종목과 관심종목에 대한 공시/보고서를 사이트에 들어가서 일일이 확인하기 귀찮음
# 2) 공시/보고서가 언제 올라올지도 모르는데 매일 들어가서 확인하기도 번거로움
#    1), 2)를 해결하기 위해...
#       a). 원하는 기간을 입력하여 해당 기간에 대한 내용 다 가져오기
#       b). 필요한 내용은 바로 확인할 수 있도록 링크 다운로드

# 개선할 점 1 : 프로그램 실행 시 사용자가 원하는 날짜 입력할 수 있도록 코드 작성
# 개선할 점 2 : us_report 실행될 때 idx 출력값이 종종 잘못나옴(1이 아니라 다른 숫자에서 시작)
# 개선할 점 3 : time.sleep을 많이 써서 그런지, 불필요한 코드가 있어서 그런지, selenium 때문인지, 솔직히 좀 느리다.



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
From_date=datetime.date(2022,1,1)
To_date=datetime.date(2022,7,21)


# 1. 미국 주식
def us_report(*CIKs):

    browser=webdriver.Chrome(options=options)
    CNTs=0

    for CIK in CIKs:
        url = "https://www.sec.gov/edgar/browse/?CIK={}&owner=exclude".format(CIK)
        browser.get(url)
        time.sleep(3)
        browser.find_element_by_xpath("//*[@id='btnViewAllFilings']").click()
        time.sleep(3)

        soup = BeautifulSoup(browser.page_source, "lxml")
        name=soup.find("span", attrs={"id":"name"})
        number_of_lists=soup.find("tbody").find_all("tr")

        CNT=0
        for i in range(0, len(number_of_lists)):
            filing_dates=soup.find("tbody").find_all("td", attrs={"class":"sorting_1"})[i].get_text()
            if str(From_date) <= filing_dates <= str(To_date):
                CNT+=1
        print("[{0}]({1})".format(name.get_text(), CNT))
        CNTs += CNT

        for idx, i in enumerate(range(0, len(number_of_lists)), start=1):
            form_types=soup.find("tbody").find_all("td", attrs={"class":"dtr-control"})[i].get_text()
            form_descriptions=soup.find("tbody").find_all("a", attrs={"class":"document-link"})[i].get_text().replace("Open document", "")
            links=soup.find("tbody").find_all("a", attrs={"class":"document-link"})[i]["href"]
            filing_dates=soup.find("tbody").find_all("td", attrs={"class":"sorting_1"})[i].get_text()
            if str(From_date) <= filing_dates <= str(To_date):
                print("   {0}. [{1}] ".format(idx, form_types), form_descriptions, " ({0})".format(filing_dates))
                if idx < 10:
                    print("      https://www.sec.gov"+links)
                else:
                    print("       https://www.sec.gov"+links)
            else:
                continue
        
        print("-"*100)

    print(f"----- END ( 종목 : {len(CIKs)}, 내용 : {CNTs} ) -----\n")
    browser.quit()


# 2. 국내 주식
def kr_report(*CODEs):

    browser=webdriver.Chrome(options=options)
    if_num=0
    else_num=0

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
        pages=soup.find("div", attrs={"class":"pageSkip"}).find_all("li")

        if len(pages) <= 1:
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
                elif 10 <= idx < 100:
                    print("       https://dart.fss.or.kr"+links)
                else:
                    print("        https://dart.fss.or.kr"+links)

            if_num += len(number_of_lists)
            print("-"*100)

        else:
            browser.find_element_by_xpath(f"//*[@id='psWrap']/div[2]/ul/li[{len(pages)}]/a").click()
            time.sleep(3)
            soup = BeautifulSoup(browser.page_source, "lxml")
            lists_on_lastpg=soup.find("tbody").find_all("tr")
            list_num=(len(pages)-1)*100+len(lists_on_lastpg)
            print("[{0}]({1})".format(name, list_num))  # [종목명](조건에 맞는 파일 수)

            for pg in range(1, len(pages)+1):
                browser.find_element_by_xpath(f"//*[@id='psWrap']/div[2]/ul/li[{pg}]/a").click()
                time.sleep(3)
                soup = BeautifulSoup(browser.page_source, "lxml")

                number_of_lists=soup.find("tbody").find_all("tr")
                
                for idx, i in enumerate(range(0, len(number_of_lists)), start=1):
                    file_name=soup.find("tbody").find_all("tr")[i].find_all("td", attrs={"class":"tL"})[1].find("a")
                    file_names=file_name.get_text().strip()
                    filing_dates=soup.find("tbody").find_all("tr")[i].find_all("td")[4].get_text()
                    links=file_name["href"]

                    if pg <= 1:
                        print("   {0:<3} {1}  ({2})".format(str(idx)+".", file_names, filing_dates))
                        if idx < 10:
                            print("      https://dart.fss.or.kr"+links)
                        elif 10 <= idx < 100:
                            print("       https://dart.fss.or.kr"+links)
                        else:
                            print("        https://dart.fss.or.kr"+links)

                    else:
                        print("   {0:<3} {1}  ({2})".format(str((pg-1)*100+idx)+".", file_names, filing_dates))
                        print("        https://dart.fss.or.kr"+links)

            else_num += list_num
            print("-"*100)

    total_num = if_num + else_num
    print(f"----- END ( 종목 : {len(CODEs)}, 내용 : {total_num} ) -----\n")
    browser.quit()
# 문제 !!!! : 종목명 옆에 가져온 파일 갯수가 실제 파일 갯수와 다름   * [종목명](파일 갯수)
#             *** 이거 해결하면서 불필요한 코드도 줄이기 ***
# 해결 !!!! : 종목별 웹페이지 상의 분량 다름. 페이지가 - '1 이하' 와 '1 초과'로 나눠서 조건문 작성
#             각 조건문 상에서 출력 내용 갯수 추출, total_num으로 합산
# 개선2 : "--- END ---" 이후에, 총합 1)몇 개의 종목과, 2) 몇 개의 파일을 가져왔는지 표시/출력
# 해결2 : 1) CIKs, CODEs 내의 변수 갯수 반환(len), 2) 함수 내에 출력된 파일 갯수 세는 변수(CNTs, total_num)


# 3. 다 끌어오기
def Report_Downloader():
    start_time=time.time()
    us_report("320193", "1018724", "1652044", "200406", "21344", "936468", "789019")
    kr_report("000660", "005930", "051910")
    # CIKs : 320193 AAPL /  1018724 AMZN / 1652044 GOOGL / 200406 JNJ / 21344 KO / 936468 LMT / 789019 MSFT
    # CODE : 005930 삼성전자  /  000660 SK하이닉스  /  051910 LG화학
    end_time=time.time()
    time_spent = end_time - start_time
    print(f"({str(round((time_spent), 4))} sec.)")



if __name__=="__main__":
    Report_Downloader()