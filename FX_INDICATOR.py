# 원/달러 환율 데이터 정리
# a) 환율 정보 끌어와서 엑셀로 정리, 차트 만들기
#    (엑셀자료는 웹페이지에서도 받을 수 있음. 내가 원하는건 한 번에 차트까지 만들어지는거)
# b) open/close/high/low/end price 다 갖고 와서 캔들차트 만들기 / 일, 주, 월봉

# a)
import datetime
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
ref_date=datetime.date(2022,1,1)
today=datetime.date.today()
browser.find_element_by_id("endDate").send_keys(str(today))
browser.find_element_by_xpath("//*[@id='applyBtn']").click()
time.sleep(2)
print("=> OPEN THE WEB PAGE")

file_today=str(today).replace("-",".")
wb=Workbook()
ws_a=wb.active
ws_a.title=f"2022.01.01~{file_today}"
ws_b=wb.create_sheet("Chart")
ws_a.append(["DATE", "", "FX RATE"])
ws_a.column_dimensions["A"].width=11
ws_a.column_dimensions["B"].width=11  # only two column needed
ws_a.column_dimensions["C"].width=9

timedelta=today-ref_date
rows_date=timedelta.days+1
td=datetime.timedelta(days=1)
for d in range(2, rows_date+2):
    ws_a["A{}".format(d)]=ref_date
    ref_date += td
print("=> OPEN THE EXCEL - PRIMARY SETTING")

soup = BeautifulSoup(browser.page_source, "lxml")
all_lists=soup.find("tbody").find_all("tr")
for i in range(0, len(all_lists)):
    dates=all_lists[i].find_all("td")[0].get_text().replace("년 ", "-").replace("월 ", "-").replace("일", "")
    day_fx=all_lists[i].find_all("td")[1].get_text().replace(",", "")
    ws_a.cell(row=(len(all_lists)+1)-i, column=2).value=dates
    ws_a.cell(row=(len(all_lists)+1)-i, column=3).value=day_fx

# !!!!!!!!!!!!!!!!!!
# for i in range(0+2, (len(all_lists)+1)+2):
idx=2  # 3, 4, 5, 6, 7, 8, 9, 10
idxx=1  # 2, 3, ,  ,  ,  ,  , 4
while idx != rows_date+1:
    if ws_a.cell(row=idx, column=1).value != ws_a.cell(row=idx, column=2).value:
        ws_a.move_range("B{0}:C{1}".format(idx, len(all_lists)+idxx), rows=1)
        idx += 1
        idxx += 1
    else:
        idx += 1

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
time.sleep(1)
pyautogui.hotkey("ctrl", "s")
print("=> OPEN THE FILE")
end_time=time.time()
time_spent = end_time - start_time
print(f"=> FIN. ({str(round((time_spent), 4))} sec.)")


# 문제1 : 프로그램 작동 중에 마우스 움직임 감지되면 로그인 팝업 뜸
# 문제3 : 날짜 중간중간 비어있는 날짜 있음. 해당 날짜 채우고, 그 날에 대한 FX는 전날 값 복붙
# 생각3 : 웹페이지에서 가져온 날짜(dates)와 환율 데이터(day_fx)를 각 리스트에 append하고,
#         빠지는 날이 없는 ref_date와 day_fx[n]을 비교해서, 서로 같을 때는 날짜와 환율을
#         같지 않을 때는 날짜만 입력
#         아니면 반복문 활용해서, 날짜가 같지 않은 부분부터 제일 마지막까지 블록지정하고 칸 옮기기
# 고민3 : 리스트에 넣어놓고, 그걸 꺼내서 각 셀이랑 비교하는 건 못하겠다. 내 능력치의 한계겠지
#         엑셀 파일 내에서, column 내의 셀끼리 비교해서 옮기는 건 해볼만 할 것 같은데
#         그럴싸하게 코드를 작성해도 원한는 결과가 안나온다. (max_row를 활용해 본다?!?!)
# 고민3' : 차트 만드는데, 굳이 날짜가 다 필요한가???