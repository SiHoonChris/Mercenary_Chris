from statistics import mean, pstdev
import matplotlib.pyplot as plt
import pandas as pd
def trim(df):
    df.sort_index(ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.drop(columns=df.columns[5:], inplace=True) # 거래량, 등락률 제거
    return df.index[-1]
def SMA_ATR(period, last_idx): # period=250
    TR=[]
    for i in range(0, last_idx+1):
        if i==0:
            TR.append(abs(df.loc[i,'High']-df.loc[i,'Low']))
        else:
            TR1=abs(df.loc[i,'High']-df.loc[i,'Low'])
            TR2=abs(df.loc[i,'High']-df.loc[i-1,'Price'])
            TR3=abs(df.loc[i,'Low']-df.loc[i-1,'Price'])
            TR.append(max(TR1, TR2, TR3))
    ATR=[]
    for i in range(0, last_idx+1):
        if i < (period-1):
            ATR.append("")
        else:
            ATR.append(mean(TR[i-(period-1):(i+1)]))
    for i in range(0, last_idx+1):
        if i < (period-1):
            pass
        else:
            df.loc[i,'SMA-ML']=df.loc[i-(period-1):i, 'Price'].mean()
            df.loc[i,'SMA-UL']=df.loc[i-(period-1):i, 'Price'].mean()+ATR[i]*2
            df.loc[i,'SMA-LL']=df.loc[i-(period-1):i, 'Price'].mean()-ATR[i]*2
class Ichimoku():
    def __init__(self, CL, BL, LS_B, last_idx):  # CL=9, BL=26, LS_B=52, last_idx=(df.index[-1], before its expansion)
        self.CL=CL-1
        self.BL=BL-1
        self.LS_B=LS_B-1
        self.last_idx=last_idx
    def ConversionLine(self):
        for i in df.index:
            if self.CL <= i <= self.last_idx:
                max_value=max(max(df.loc[i-self.CL:i, 'Price']), max(df.loc[i-self.CL:i, 'Open']),\
                     max(df.loc[i-self.CL:i,'High']), max(df.loc[i-self.CL:i, 'Low']))
                min_value=min(min(df.loc[i-self.CL:i, 'Price']), min(df.loc[i-self.CL:i, 'Open']),\
                     min(df.loc[i-self.CL:i, 'High']), min(df.loc[i-self.CL:i, 'Low']))
                df.loc[i,'CL']=(max_value+min_value)/2
    def BaseLine(self):
        for i in df.index:
            if self.BL <= i <= self.last_idx:
                max_value=max(max(df.loc[i-self.BL:i, 'Price']), max(df.loc[i-self.BL:i, 'Open']),\
                     max(df.loc[i-self.BL:i, 'High']), max(df.loc[i-self.BL:i, 'Low']))
                min_value=min(min(df.loc[i-self.BL:i, 'Price']), min(df.loc[i-self.BL:i, 'Open']),\
                     min(df.loc[i-self.BL:i, 'High']), min(df.loc[i-self.BL:i, 'Low']))
                df.loc[i,'BL']=(max_value+min_value)/2
    def LeadingSpan_A(self):  # 당일 포함해서 26일 선행
        CL_dict={}
        for i in df.index:
            if self.CL <= i <= self.last_idx:
                max_value=max(max(df.loc[i-self.CL:i, 'Price']), max(df.loc[i-self.CL:i, 'Open']),\
                     max(df.loc[i-self.CL:i, 'High']), max(df.loc[i-self.CL:i, 'Low']))
                min_value=min(min(df.loc[i-self.CL:i, 'Price']), min(df.loc[i-self.CL:i, 'Open']),\
                     min(df.loc[i-self.CL:i, 'High']), min(df.loc[i-self.CL:i, 'Low']))
                CL_dict[i]=(max_value+min_value)/2
        BL_dict={}
        for i in df.index:
            if self.BL <= i <= self.last_idx:
                max_value=max(max(df.loc[i-self.BL:i, 'Price']), max(df.loc[i-self.BL:i, 'Open']),\
                     max(df.loc[i-self.BL:i, 'High']), max(df.loc[i-self.BL:i, 'Low']))
                min_value=min(min(df.loc[i-self.BL:i, 'Price']), min(df.loc[i-self.BL:i, 'Open']),\
                     min(df.loc[i-self.BL:i, 'High']), min(df.loc[i-self.BL:i, 'Low']))
                BL_dict[i]=(max_value+min_value)/2
        for i in df.index:
            if self.BL <= i <= self.last_idx:
                df.loc[i+25,'LS_A']=(CL_dict.get(i)+BL_dict.get(i))/2
    def LeadingSpan_B(self):  # 당일 포함해서 26일 선행
        for i in df.index:
            if self.LS_B <= i <= self.last_idx:
                max_value=max(max(df.loc[i-self.LS_B:i, 'Price']), max(df.loc[i-self.LS_B:i, 'Open']),\
                     max(df.loc[i-self.LS_B:i, 'High']), max(df.loc[i-self.LS_B:i, 'Low']))
                min_value=min(min(df.loc[i-self.LS_B:i, 'Price']), min(df.loc[i-self.LS_B:i, 'Open']),\
                     min(df.loc[i-self.LS_B:i, 'High']), min(df.loc[i-self.LS_B:i, 'Low']))
                df.loc[i+25, 'LS_B']=(max_value+min_value)/2
def BB_Band(period, n, last_idx):  # period=20, n=2, 표준편차는 모집단(Population)에 대한 표준편차 사용
    TP=[]
    for i in range(0, last_idx+1):
        tp=(df.loc[i,'High']+df.loc[i,'Low']+df.loc[i,'Price'])/3
        TP.append(tp)
    for i in range(0, last_idx+1):
        if i < (period-1):
            pass
        else:
            df.loc[i,'BOLM']=mean(TP[i-(period-1):(i+1)])
            df.loc[i,'BOLU']=df.loc[i,'BOLM'] + pstdev(TP[i-(period-1):(i+1)])*n
            df.loc[i,'BOLD']=df.loc[i,'BOLM'] - pstdev(TP[i-(period-1):(i+1)])*n
def color_column(last_idx):
    red_start=[]
    red_end_prev=[]
    red_end=[]
    blue_start=[]
    blue_end_prev=[]
    blue_end=[]

    for idx in range(1, last_idx):
        if df.loc[idx,'Price'] > df.loc[idx,'LS_B'] > df.loc[idx-1,'Price'] > df.loc[idx,'LS_A'] or\
            df.loc[idx,'Price'] > df.loc[idx,'LS_B'] > df.loc[idx,'LS_A'] > df.loc[idx-1,'Price'] or\
            df.loc[idx,'Price'] > df.loc[idx,'LS_A'] > df.loc[idx-1,'Price'] > df.loc[idx,'LS_B'] or\
            df.loc[idx,'Price'] > df.loc[idx,'LS_A'] > df.loc[idx,'LS_B'] > df.loc[idx-1,'Price']:
            red_start.append(idx)
        elif df.loc[idx,'LS_A'] > df.loc[idx-1,'Price'] > df.loc[idx,'LS_B'] > df.loc[idx,'Price'] or\
            df.loc[idx-1,'Price'] > df.loc[idx,'LS_A'] > df.loc[idx,'LS_B'] > df.loc[idx,'Price'] or\
            df.loc[idx,'LS_B'] > df.loc[idx-1,'Price'] > df.loc[idx,'LS_A'] > df.loc[idx,'Price'] or\
            df.loc[idx-1,'Price'] > df.loc[idx,'LS_B'] > df.loc[idx,'LS_A'] > df.loc[idx,'Price']:
            blue_start.append(idx)
        elif df.loc[idx,'BOLU'] > df.loc[idx-1,'BOLU'] and df.loc[idx,'BOLU'] > df.loc[idx+1,'BOLU']:
            red_end_prev.append(idx)
        elif df.loc[idx,'BOLD'] < df.loc[idx-1,'BOLD'] and df.loc[idx,'BOLD'] < df.loc[idx+1,'BOLD']:
            blue_end_prev.append(idx)
        else:
            pass

    if red_start[-1] < red_end_prev[-1]:
        for i in range(0, len(red_start)):
            n=0
            while red_start[i] >= red_end_prev[n]:
                n+=1
                if red_start[i] < red_end_prev[n]:
                    red_end.append(red_end_prev[n])
    else:
        for i in range(0, len(red_start)-1):
            n=0
            while red_start[i] >= red_end_prev[n]:
                n+=1
                if red_start[i] < red_end_prev[n]:
                    red_end.append(red_end_prev[n])
        red_end.append(red_start[len(red_start)-1])

    if blue_start[-1] < blue_end_prev[-1]:
        for i in range(0, len(blue_start)):
            n=0
            while blue_start[i] >= blue_end_prev[n]:
                n+=1
                if blue_start[i] < blue_end_prev[n]:
                    blue_end.append(blue_end_prev[n])
    else:
        for i in range(0, len(blue_start)-1):
            n=0
            while blue_start[i] >= blue_end_prev[n]:
                n+=1
                if blue_start[i] < blue_end_prev[n]:
                    blue_end.append(blue_end_prev[n])
        blue_end.append(blue_start[len(blue_start)-1])

    return red_start, red_end, blue_start, blue_end


# 데이터 생성
file='GOOGL 19.09.13~22.09.12'  # investing.com
df = pd.read_excel(file+'.xlsx')
last_idx = trim(df)
for i in range(1, 26):
        df.loc[last_idx+i] = ['', '', '', '', '']

column_heads=['SMA-ML', 'SMA-UL', 'SMA-LL', 'Decision', 'LS_A', 'LS_B', 'BOLM', 'BOLU', 'BOLD']
for col in column_heads:
    df[col]=''
    df[col]=pd.to_numeric(df[col])

SMA_ATR(250, last_idx)
ichimoku=Ichimoku(9, 26, 52, last_idx)
ichimoku.LeadingSpan_A()
ichimoku.LeadingSpan_B()
BB_Band(20, 2, last_idx)
red_start, red_end, blue_start, blue_end = color_column(last_idx)

print(df)
df.to_excel('for graph, '+file+'.xlsx')


# 데이터 시각화
plt.figure(figsize=(20, 10))

date=df['Date'][:last_idx+1]
plt.plot(date, df['Price'][:last_idx+1], label='Price', color='navy')
plt.plot(date, df['SMA-ML'][:last_idx+1], label='SMA-ML', color='green', linestyle='--')
plt.plot(date, df['SMA-UL'][:last_idx+1], label='SMA-UL', color='red')
plt.plot(date, df['SMA-LL'][:last_idx+1], label='SMA-LL', color='blue')

LS_A=df['LS_A'][:last_idx+1]
LS_B=df['LS_B'][:last_idx+1]
plt.plot(date, LS_A, label='ICMK_LS_A', color='orange', lw=0.6)
plt.plot(date, LS_B, label='ICMK_LS_B', color='skyblue', lw=0.6)
plt.fill_between(date, LS_A, LS_B, where=(LS_A >= LS_B), color='orange', alpha=0.3, interpolate=True)
plt.fill_between(date, LS_A, LS_B, where=(LS_A < LS_B), color='skyblue', alpha=0.3, interpolate=True)

plt.plot(date, df['BOLM'][:last_idx+1], label='BB_M', color='green', ls="--", lw=0.4, alpha=0.6)
plt.plot(date, df['BOLU'][:last_idx+1], label='BB_U', color='red', lw=0.4)
plt.plot(date, df['BOLD'][:last_idx+1], label='BB_D', color='blue', lw=0.4)

for i in range(0, len(red_start)):
    plt.axvspan(date[red_start[i]], date[red_end[i]], alpha=0.3, color='red')
    plt.hlines(max(df.loc[red_start[i]:red_end[i], 'Price']), date[red_start[i]], date[red_end[i]], color='green')
    plt.text(date[red_start[i]], max(df.loc[red_start[i]:red_end[i], 'Price'])+1, max(df.loc[red_start[i]:red_end[i], 'Price']),\
         ha='left', alpha=0.5)
for i in range(0, len(blue_start)):
    plt.axvspan(date[blue_start[i]], date[blue_end[i]], alpha=0.3, color='blue')
    plt.hlines(min(df.loc[blue_start[i]:blue_end[i], 'Price']), date[blue_start[i]], date[blue_end[i]], color='yellow')
    plt.text(date[blue_start[i]], min(df.loc[blue_start[i]:blue_end[i], 'Price'])-2.5, min(df.loc[blue_start[i]:blue_end[i], 'Price']),\
         ha='center', alpha=0.5)

plt.title(f'GOOGL, for {last_idx+1}days', fontsize=20)
# plt.xticks([0, last_idx])
plt.grid(axis='y')
plt.legend()

plt.savefig('for graph, '+file+'.png', dpi=150)



# APPENDIX.
# 0. 왜 이름이 FX_automation인가?
#    코드를 처음 작성할 때, 환전(FX) 자동화를 목표로 구상했음
#    근데 막상 만들면서 생각해보니 어느 자산에든 적용이 가능함
#    TRADE_automation이 더 적절할 듯
# 1. ATR을 활용한 SMA-Line
#    SMA-ML은 특정 기간에 대한 단순이동평균선, SMA-UL/LL은 SMA-ML에서 동일 기간의 ATR을 가감한 것
#    종가가 SMA-UL 위에 형성되면 기간(250일) 평균보다 비쌈, SMA-LL 아래 형성되면 기간 평균보다 저렴함을 의미
#    SMA 밴드의 폭은 가격의 변동성을 의미. 즉, 그 폭이 넓다는 건 가격의 변동성이 크다는 것
#    SMA가 우상향하는데, 밴드의 폭이 좁고 일정하다? => 장기간 안정적으로 가격이 상승했음을 의미
#    왜 250일인가? => 365일 중 주말(2일*52주) 빼고, 기타 휴무일(11일 정도로 가정) 빼고. 그럼 250일
#    SQUENTIAL ATR(이전 ATR에 당일 TR을 더하는 방식)을 적용했었는데 그 모양이 가시성이 매우 떨어져서, SIMPLE ATR 적용
# 2. 일목균형표와 볼린저밴드를 활용한 RED/BLUE AREA
#    종가가 일목균형표의 구름을 돌파하는 시점과 볼린저밴드 상/하단선의 피크가 발생하는 시점 사이의 구간을 의미
#    RED는 상승으로의 추세전환, BLUE는 하락으로의 추세전환을 나타냄
#    그 구간 안에서 최고가/최저가를 가로선(기준 가격)으로 표시 => AREA 이후, 다음 AREA 발생 전, 기준 가격을 돌파하면 추세의 확정으로 판단 
# 3. 활용
#    ( 차트와 보조지표는 과거의 정보들을 통해 현재의 상태를 보여줄 뿐, 절대 미래의 기대치를 보여주지 않는다.
#      또한, 매매에 있어 각 개인의 전략과 가치관에 따른 가장 합리적인 기준점을 제시한다.
#      그렇기에 매매를 하기에 앞서, 해당 종목에 대한 정확한 이해와 분석이 선행되어야 한다. )
#    운용 예시)
#    - 1) SMA-UL 위에서 RED AREA 기준 가격 발생, 이후 기준 가격 돌파 : 추가 소량 매수
#         (가격이 고평가 된 상태이나 더 상승할 것으로 판단. 보유 비중을 높일 필요가 있음)
#    - 2) SMA-UL 위에서 BLUE AREA 기준 가격 발생, 이후 기준 가격 돌파 : 분할 소량 매도
#         (가격이 고평가 된 상태이며, 향후 저평가로 전환될 가능성이 있음. 상대적으로 높은 가격 매도하여 시세차익의 일부를 실현함과
#          동시에 보유 비중은 줄일 필요가 있음)
#    - 3) SMA 밴드 내에서 RED/BLUE AREA 기준 가격 발생 : 매매 보류
#    - 4) SMA-LL 아래에서 RED AREA 기준 가격 발생, 이후 기준 가격 돌파 : 추가 대량 매수
#         (가격이 저평가 된 상태이며, 향후 고평가로 전환될 가능성이 있음. 상대적으로 낮은 가격에 매수하여 보유 비중을 높일 필요가 있음)
#    - 5) SMA-LL 아래에서 BLUE AREA 기준 가격 발생, 이후 기준 가격 돌파 : 분할 대량 매도
#         (가격이 저평가 된 상태이나 더 하락할 것으로 판단, 보유 비중을 대폭 줄일 필요가 있음)