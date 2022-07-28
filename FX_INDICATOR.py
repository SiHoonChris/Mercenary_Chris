# 원/달러 환율 데이터 정리
# a) 환율 정보 끌어와서 엑셀로 정리, 차트 만들기
#    (엑셀자료는 웹페이지에서도 받을 수 있음. 내가 원하는건 한 번에 차트까지 만들어지는거)
# b) open/close/high/low/end price 다 갖고 와서 캔들차트 만들기 / 일, 주, 월봉

# a)
from datetime import datetime
import time
start_time=time.time()

from bs4 import BeautifulSoup
headers="Mozilla/5.0"
from selenium import webdriver
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent="+headers)
browser=webdriver.Chrome(options=options)

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Side, Font
import subprocess
import pyautogui


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
print("=> OPEN THE WEB PAGE")

file_today=str(today).replace("-",".")
wb=Workbook()
ws_a=wb.active
ws_a.title=f"2022.01.01~{file_today}"
ws_b=wb.create_sheet("Chart")
ws_a.append(["DATE", "FX RATE"])
ws_a.column_dimensions["A"].width=11
ws_a.column_dimensions["B"].width=9
print("=> OPEN THE EXCEL - PRIMARY SETTING")

soup = BeautifulSoup(browser.page_source, "lxml")
all_lists=soup.find("tbody").find_all("tr")
for i in range(0, len(all_lists)):
    dates=all_lists[i].find_all("td")[0].get_text().replace("년 ", "-").replace("월 ", "-").replace("일", "")
    day_fx=all_lists[i].find_all("td")[1].get_text().replace(",", "")
    ws_a.cell(row=(len(all_lists)+1)-i, column=1).value=dates
    ws_a.cell(row=(len(all_lists)+1)-i, column=2).value=day_fx
for column in ws_a.columns:
    for cell in column:
        cell.alignment = Alignment(horizontal="center", vertical="center")
thin_border = Border(left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"), bottom=Side(style="thin"))
for row in ws_a.iter_rows():
    for cell in row:
        cell.border=thin_border
ws_a["A1"].font=Font(bold=True)
ws_a["B1"].font=Font(bold=True)
print("=> WEB SCRAPPING - FILL IN THE CELLS")

wb.save(f"2022.01.01~{file_today} , FX(WON-DOLLAR).xlsx")
print("=> SAVE THE FILE")
subprocess.Popen([f"2022.01.01~{file_today} , FX(WON-DOLLAR).xlsx"], shell=True)
# 엑셀파일 작성(스크래핑) 끝나면, 바로 파일 열어서 내용 확인
time.sleep(1)
pyautogui.hotkey("ctrl", "s")  # 저장
print("=> OPEN THE FILE")
end_time=time.time()
time_spent = end_time - start_time
print(f"=> FIN. ({str(round((time_spent), 4))} sec.)")

# 문제1 : 프로그램 작동 중에 마우스 움직임 감지되면 로그인 팝업 뜸
# 문제2 : 데이터를 가져올 때, 날짜 순서가 내림차순(가장 최근이 맨위에, 시작일이 맨아래에)임. 반대로 뒤집어야 함
# 해결2 : row의 위치를 len(all_lists)+1 에서 i를 뺌으로서 역순으로 채우지게 함
# 문제3 : 날짜 중간중간 비어있는 날짜 있음. 해당 날짜 채우고, 그 날에 대한 FX는 전날 값 복붙

# => OPEN THE WEB PAGE
# => OPEN THE EXCEL - PRIMARY SETTING
# => WEB SCRAPPING - FILL IN THE CELLS
# => SAVE THE FILE
# => OPEN THE FILE
# => FIN. (14.1364 sec.)