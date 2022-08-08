# 1. CONVERSION LINE (CL)
#    전환선 ; (과거 9일 동안 최고가 + 과거 9일 동안 최저가)/2 
# 2. BASE LINE (BL)
#    기준선 ; (과거 26일 동안 최고가 + 과거 26일 동안 최저가)/2
# 3. LEADING SPAN A(1) (LS_1)
#    선행스팬A(1) ; (당일 기준선 + 당일 전환선)/2 를 26일 선행해서 배치
# 4. LEADING SPAN B(2) (LS_2)
#    선행스팬B(2) ; {(최근 52일 동안 최고가 + 최근 52일 동안 최저가)}/2 를 26일 선행해서 배치
# 5. LAGGING SPAN (LP)
#    후행스팬 ; 당일의 종가를 당일 포함 26일 전의 위치에 나타낸 선
# 선행2가 선행1 보다 위에 있으면 음운 / 선행1이 선행2 보다 위에 있으면 양운

# 목표/방향
# 1. IVV(iShares Core S&P 500 ETF)의 2021년 데이터 활용 (일봉 차트)
# 2. 출처 : https://kr.investing.com/etfs/ishares-s-p-500
# 3. 종가와 선행스팬1, 선행스팬2를 활용하여, 당일 종목의 추세(상향/하향)를 확인한다.
# 4. 종가가 선행스팬1과 선행스팬2 보다 높으면 상향추세
#    종가가 선행스팬1과 선행스팬2 보다 낮으면 하향추세
#    종가가 선행스팬1과 선행스팬2 사이에 있으면(선행스팬1 > 선행스팬2) 하향추세 전환 예상
#    종가가 선행스팬1과 선행스팬2 사이에 있으면(선행스팬1 < 선행스팬2) 상향추세 전환 예상

# 데이터 가공
import pandas as pd
df = pd.read_csv('IVV, 21.01.01~21.12.31.csv')
df.sort_index(ascending=False, inplace=True)
df.reset_index(drop=True, inplace=True)
df=df[['날짜', '종가']]

# 1. CONVERSION LINE (CL)
#    전환선 ; (과거 9일 동안 최고가 + 과거 9일 동안 최저가)/2 
df['전환선']=0
for i in range(0,  257):
    if i < 9:
        pass
    else:
        max_value=max(df.iloc[i-9:i , 1])
        min_value=min(df.iloc[i-9:i , 1])
        df.iloc[i,-1]=(max_value+min_value)/2

# 2. BASE LINE (BL)
#    기준선 ; (과거 26일 동안 최고가 + 과거 26일 동안 최저가)/2
df['기준선']=0
for i in range(0,  257):
    if i < 26:
        pass
    else:
        max_value=max(df.iloc[i-26:i , 1])
        min_value=min(df.iloc[i-26:i , 1])
        df.iloc[i,-1]=(max_value+min_value)/2

# 3. LEADING SPAN A(1) (LS_1)
#    선행스팬A(1) ; (당일 기준선 + 당일 전환선)/2 를 26일 선행해서 배치 *당일:0일, 26일 선행:25일
#    전환선, 기준선 모두 값이 0이 아닐 때부터 선행스팬의 값이 구해짐(전환선, 기준선 모두 0이 아닌 시점으로부터 26일 선행) 
df['선행스팬A(1)']=(df['전환선']+df['기준선'])/2

# 저장
print(df)
df.to_excel('ichimoku_a.xlsx')