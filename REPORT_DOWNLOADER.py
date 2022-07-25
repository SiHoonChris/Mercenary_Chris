# 국내주식, 미국주식 공시/보고서 다운로더
#    1) 보유종목과 관심종목에 대한 공시/보고서를 사이트에 들어가서 일일이 확인하기 귀찮음
#    2) 공시/보고서가 언제 올라올지도 모르는데 매일 들어가서 확인하기도 번거로움

from bs4 import BeautifulSoup
headers="Mozilla/5.0"
from selenium import webdriver
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent="+headers)
import time
import datetime

class Date_Sequence_Error(Exception):
    def __init__(self, msg):
        self.msg=msg
    def __str__(self):
        return self.msg


while True:
    try:
        example="<입력 예시>\n\n(시작) 연 : 2021\n(시작) 월 : 12\n(시작) 일 : 20\n(종료) 연 : 2022\n(종료) 월 : 3\n(종료) 일 : 5"
        print(example+"\n-----------------")
        fy=input("(시작) 연 : ")
        fm=input("(시작) 월 : ")
        fd=input("(시작) 일 : ")
        ty=input("(종료) 연 : ")
        tm=input("(종료) 월 : ")
        td=input("(종료) 일 : ")
        From_date=datetime.date(int(fy),int(fm),int(fd))
        To_date=datetime.date(int(ty),int(tm),int(td))
        Today=datetime.date.today()

        if str(To_date) < str(From_date) :
            raise Date_Sequence_Error("*** '시작 날짜'가 '종료 날짜' 보다 늦음 ***\n")
        if str(Today) < str(From_date):
            raise Date_Sequence_Error("*** '시작 날짜'가 '오늘' 이후 임 ***\n")
        if str(Today) < str(To_date):
            raise Date_Sequence_Error("*** '종료 날짜'가 '오늘' 이후 임 ***\n")

        break
    except ValueError:
        print("*** 입력 내용 다시 확인! - 문자나 기호 X / <입력 예시> 참고 ***")
    except Date_Sequence_Error as err:
        print(err)


def us_report(*CIKs):

    browser=webdriver.Chrome(options=options)
    CNTs=0

    for CIK in CIKs:
        url = "https://www.sec.gov/edgar/browse/?CIK={}&owner=exclude".format(CIK)
        browser.get(url)
        time.sleep(2)
        browser.find_element_by_xpath("//*[@id='btnViewAllFilings']").click()
        time.sleep(2)

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

        idx=0
        for i in range(0, len(number_of_lists)):
            form_types=soup.find("tbody").find_all("td", attrs={"class":"dtr-control"})[i].get_text()
            form_descriptions=soup.find("tbody").find_all("a", attrs={"class":"document-link"})[i].get_text().replace("Open document", "")
            links=soup.find("tbody").find_all("a", attrs={"class":"document-link"})[i]["href"]
            filing_dates=soup.find("tbody").find_all("td", attrs={"class":"sorting_1"})[i].get_text()
            if str(From_date) <= filing_dates <= str(To_date):
                idx += 1
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


def kr_report(*CODEs):

    browser=webdriver.Chrome(options=options)
    if_num=0
    else_num=0

    for CODE in CODEs:
        url="https://dart.fss.or.kr/"
        browser.get(url)
        time.sleep(2)
        browser.find_element_by_xpath("//*[@id='textCrpNm2']").send_keys(CODE)
        browser.find_element_by_xpath("//*[@id='searchForm2']/div[1]/div[3]/a").click()
        time.sleep(2)
        Start_date=str(From_date).replace("-", "")
        End_date=str(To_date).replace("-", "")
        browser.find_element_by_xpath("//*[@id='startDate']").clear()
        browser.find_element_by_xpath("//*[@id='startDate']").send_keys(Start_date)
        browser.find_element_by_xpath("//*[@id='endDate']").clear()
        browser.find_element_by_xpath("//*[@id='endDate']").send_keys(End_date)
        browser.find_element_by_xpath("//*[@id='maxResultsCb']/option[4]").click()
        browser.find_element_by_xpath("//*[@id='searchForm']/div[2]/div[2]/a[1]").click()
        time.sleep(2)

        soup = BeautifulSoup(browser.page_source, "lxml")
        name = soup.find("span", attrs={"class":"innerWrap"}).find("a").get_text().strip()
        pages=soup.find("div", attrs={"class":"pageSkip"}).find_all("li")

        if len(pages) <= 1:
            number_of_lists=soup.find("tbody").find_all("tr")
            print("[{0}]({1})".format(name, len(number_of_lists)))

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
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, "lxml")
            lists_on_lastpg=soup.find("tbody").find_all("tr")
            list_num=(len(pages)-1)*100+len(lists_on_lastpg)
            print("[{0}]({1})".format(name, list_num))

            for pg in range(1, len(pages)+1):
                browser.find_element_by_xpath(f"//*[@id='psWrap']/div[2]/ul/li[{pg}]/a").click()
                time.sleep(2)
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


def Report_Downloader():
    start_time=time.time()
    us_report("320193", "1018724", "1652044", "200406", "21344", "936468", "789019")  # AAPL, AMZN, GOOGL, JNJ, KO, LMT, MSFT
    kr_report("000660", "005930", "051910")  # SK하이닉스, 삼성전자, LG화학
    end_time=time.time()
    time_spent = end_time - start_time
    print(f"({str(round((time_spent), 4))} sec.)")


if __name__=="__main__":
    Report_Downloader()