# 단순이동평균선(SMA-L) - 당일 포함 최근 300일
# 단순이동평균선 상단밴드(SMA-UL) - SMA-L의 +2% 값을 연결한 선
# 단순이동평균선 하단밴드(SMA-LL) - SMA-L의 -2% 값을 연결한 선
# End-Price가 SMA-UL 위에 있으면 'Sell'
# End-Price가 SMA-LL 아래 있으면 'Buy'
# End-Price가 SMA-UL과 SMA-LL 사이에 있으면 'Hold'
# Median - 당일 포함 최근 100일에 대한 중위값
# Mean - 당일 포함 최근 100일에 대한 산술평균값
# 변동성(Vlt. ; Volatility) -  " Vlt. = |Median - Mean| "
# * Vlt.가 커질수록, 해당 기간 동안 모집단 내 상대적 소수 집단과 다수 집단의 크기 차이가 크다, 즉 변동성이 높다고 판단   
# Column Head : Date,  End-Price,  SMA-L,  SMA-UL,  SMA-LL,  Buy-Sell-Hold,  Median, Mean, Vlt.



# from openpyxl import load_workbook
# from datetime import datetime
from statistics import median
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 가공 - 어제(22.8.25) 데이터 수정 후 같은 파일명으로 저장해서 openpyxl 사용 불필요
file='USD_KRW 내역 (19.8.21~22.8.21).xlsx'
# wb = load_workbook(file)
# ws = wb.active
# for i in range(2, ws.max_row+1):
#     cell=ws['A{}'.format(i)].value
#     dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + cell - 2)
#     ws['A{}'.format(i)]=dt
# 'pandas로 excel파일 끌어올 때 날짜 데이터가 5자리 숫자로 가져와짐' => 해결
# wb.save(file) # 환율 자료 출처 : kr.investing.com

# 데이터 순서 정리
df = pd.read_excel(file)
df.sort_index(ascending=False, inplace=True)
df.reset_index(drop=True, inplace=True)
# SMA-L , SMA-UL , SMA-LL
for i in range(0, df.index[-1]+1):
    if i < 299:
        pass
    else:
        df.loc[i,'SMA-L']=df.loc[i-299:i, '종가'].mean()
        df.loc[i,'SMA-UL']=(df.loc[i-299:i, '종가'].mean())*1.02
        df.loc[i,'SMA-LL']=(df.loc[i-299:i, '종가'].mean())*0.98
# Buy-Sell-Hold
for i in range(0, df.index[-1]+1):
    if i < 299:
        pass
    else:
        if df.loc[i,'종가'] > df.loc[i,'SMA-UL']:
            df.loc[i,'B-S-H']='Sell'
        elif df.loc[i,'종가'] < df.loc[i,'SMA-LL']:
            df.loc[i,'B-S-H']='Buy'
        else:
            df.loc[i,'B-S-H']='Hold'
# Median , Mean , Vlt.
for i in range(0, df.index[-1]+1):
    if i < 99:
        pass
    else:
        df.loc[i,'Median']=df.loc[i-99:i,'종가'].median()
        df.loc[i,'Mean']=df.loc[i-99:i,'종가'].mean()
        df.loc[i,'Vlt.']=abs(df.loc[i,'Median']-df.loc[i,'Mean'])        
# 저장
print(df)
df.to_excel('WON-DOLLAR CHART.xlsx')

# 그래프
fig,axs=plt.subplots(2, 1, figsize=(20, 12), gridspec_kw={'height_ratios': [3.5, 1]})
fig.suptitle('WON/DOLLAR', fontsize=30)
# 그래프 1; 종가 & SMA
axs[0].plot(df['날짜'], df['종가'], color='navy')
axs[0].plot(df['날짜'], df['SMA-L'], color='green', linestyle='--')
axs[0].plot(df['날짜'], df['SMA-UL'], color='red')
axs[0].plot(df['날짜'], df['SMA-LL'], color='blue')
axs[0].set_title(f'SMA +/-2%,  for {df.index[-1]}days', fontsize=20)
axs[0].grid(axis='x')
# 그래프 2; Volatility
axs[1].plot(df['날짜'], df['Vlt.'], color='navy')
axs[1].set_title('Volatility ;  | Median-Mean |', fontsize=20)
axs[1].grid(axis='y')
# 저장
plt.savefig('WON-DOLLAR CHART.png')