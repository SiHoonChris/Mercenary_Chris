# 단순이동평균선(SMA-L) - 당일 포함 최근 300일
# 단순이동평균선 상단밴드(SMA-UL) - SMA-L의 +1% 값을 연결한 선
# 단순이동평균선 하단밴드(SMA-LL) - SMA-L의 -1% 값을 연결한 선
# End-Price가 SMA-UL 위에 있으면 'Sell'
# End-Price가 SMA-LL 아래 있으면 'Buy'
# End-Price가 SMA-UL과 SMA-LL 사이에 있으면 'Hold'
# Median - 당일 포함 최근 100일에 대한 중위값
# Mean - 당일 포함 최근 100일에 대한 산술평균값
# 변동성(Vlt. ; Volatility) -  " Vlt. = |Median - Mean| "
# Column Title : Date,  End-Price,  SMA-L,  SMA-UL,  SMA-LL,  Buy-Sell-Hold,  Median, Mean, Vlt.


import pandas as pd

df = pd.read_csv('USD_KRW 내역 (19.8.21~22.8.21).csv')
df.sort_index(ascending=False, inplace=True)
df.reset_index(drop=True, inplace=True)

print(df)

# '종가' 데이터를 str로 인식함, int냐 float으로 데이터 바꿔줘야 함