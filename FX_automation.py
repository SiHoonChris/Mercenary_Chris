import matplotlib.pyplot as plt
import pandas as pd
def trim(df):
    df.sort_index(ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.drop(columns=df.columns[5:], inplace=True) # 거래량, 변동만 제거
def SMA(last_idx):
    for i in range(0, last_idx+1):
        if i < 364:
            pass
        else:
            df.loc[i,'SMA-ML']=df.loc[i-364:i, 'Price'].mean()
            df.loc[i,'SMA-UL']=df.loc[i-364:i, 'Price'].mean()+df.loc[i,'ATR']
            df.loc[i,'SMA-LL']=df.loc[i-364:i, 'Price'].mean()-df.loc[i,'ATR']
def Decision(last_idx):
    for i in range(0, last_idx+1):
        if i < 299:
            pass
        else:
            if df.loc[i,'Price'] > df.loc[i,'SMA-UL']:
                df.loc[i,'Decision']='Sell'
            elif df.loc[i,'Price'] < df.loc[i,'SMA-LL']:
                df.loc[i,'Decision']='Buy'
            else:
                df.loc[i,'Decision']='Hold'
def ICMK_CL(last_idx):
    for i in df.index:
        if i < 8:
            df.loc[i,'CL']=''
            df['CL']=pd.to_numeric(df['CL'])
        elif 8 <= i <= last_idx:
            max_value=max(df.loc[i-8:i , 'Price'])
            min_value=min(df.loc[i-8:i , 'Price'])
            df.loc[i,'CL']=(max_value+min_value)/2
        else:
            df.loc[i,'CL']=''
def ICMK_BL(last_idx):
    for i in df.index:
        if i < 25:
            df.loc[i,'BL']=''
            df['BL']=pd.to_numeric(df['BL'])
        elif 25 <= i <= last_idx:
            max_value=max(df.loc[i-25:i , 'Price'])
            min_value=min(df.loc[i-25:i , 'Price'])
            df.loc[i,'BL']=(max_value+min_value)/2
        else:
            df.loc[i,'BL']=''
def ICMK_LS_A(last_idx):
    for i in df.index:
        if i < 25:
            df.loc[i,'LS_A']=''
            df.loc[i+26,'LS_A']=''
            df['LS_A']=pd.to_numeric(df['LS_A'])
        elif 25 <= i <= last_idx:
            df.loc[i+26,'LS_A']=(df.loc[i,'CL']+df.loc[i,'BL'])/2
        else:
            pass
def ICMK_LS_B(last_idx):
    for i in df.index:
        if i < 51:
            df.loc[i,'LS_B']=''
            df.loc[i+26,'LS_B']=''
            df['LS_B']=pd.to_numeric(df['LS_B'])
        elif 51 <= i <= last_idx:
            max_value=max(df.loc[i-51:i , 'Price'])
            min_value=min(df.loc[i-51:i , 'Price'])
            df.loc[i+26, 'LS_B']=(max_value+min_value)/2
        else:
            pass
def BB_Band(last_idx):
    for i in range(0, last_idx+1):
        if i > 18:
            df.loc[i,'ML']=df.loc[i-19:i,'Price'].mean()
            df.loc[i,'UL']=df.loc[i,'ML'] + df.loc[i-19:i,'Price'].std()*2
            df.loc[i,'LL']=df.loc[i,'ML'] - df.loc[i-19:i,'Price'].std()*2
        else:
            pass
def TR(last_idx):
    for i in range(0, last_idx+1):
        if i==0:
            df.loc[i,'TR']=abs(df.loc[i,'High']-df.loc[i,'Low'])
        else:
            TR1=abs(df.loc[i,'High']-df.loc[i,'Low'])
            TR2=abs(df.loc[i,'High']-df.loc[i-1,'Price'])
            TR3=abs(df.loc[i,'Low']-df.loc[i-1,'Price'])
            df.loc[i,'TR']=max(TR1, TR2, TR3)
def ATR(last_idx):
    for i in range(0, last_idx+1):
        if i < 364:
            pass
        elif i==364:
            df.loc[i,'ATR']=df.loc[i-364:i,'TR'].mean()
        else:
            df.loc[i,'ATR']=df.loc[i-1,'TR'].mean()*(364/365)+df.loc[i,'TR']*(1/365)

# 데이터 생성
file='BTC_USD Bitfinex Historical Data, 19.9.10~22.9.10'  # investing.com
df = pd.read_excel(file+'.xlsx')
trim(df)
last_idx=df.index[-1]
for i in range(1, 27):
        df.loc[last_idx+i] = ['', '', '', '', '']

column_heads=['SMA-ML', 'TR', 'ATR',  'SMA-UL', 'SMA-LL', 'Decision', 'CL', 'BL', 'LS_A', 'LS_B', 'ML', 'UL', 'LL', 'Cond.r', 'Cond.b']
for col in column_heads:
    df[col]=''
    df[col]=pd.to_numeric(df[col])

TR(last_idx)
ATR(last_idx)
SMA(last_idx)
Decision(last_idx)
ICMK_CL(last_idx)
ICMK_BL(last_idx)
ICMK_LS_A(last_idx)
ICMK_LS_B(last_idx)
BB_Band(last_idx)

red_start_list=[]
red_end_list=[]
for idx in range(1, last_idx):
    if df.loc[idx,'Price'] > df.loc[idx,'LS_B'] > df.loc[idx-1,'Price'] > df.loc[idx,'LS_A'] > df.loc[idx, 'LL'] or\
    df.loc[idx,'Price'] > df.loc[idx,'LS_A'] > df.loc[idx-1,'Price'] > df.loc[idx,'LS_B'] > df.loc[idx, 'LL']:
        df.loc[idx,'Cond.r']='red_start'
        red_start_list.append(idx)
    elif df.loc[idx,'UL'] > df.loc[idx-1,'UL'] and df.loc[idx,'UL'] > df.loc[idx+1,'UL']:
        df.loc[idx,'Cond.r']='red_end'
    else:
        pass
print(red_start_list)

red_start = df.loc[df['Cond.r']=='red_start'].index
red_end = df.loc[df['Cond.r']=='red_end'].index
if red_start[-1] < red_end[-1]:
    for i in range(0, len(red_start)):
        n=0
        while red_start[i] >= red_end[n]:
            n+=1
            if red_start[i] < red_end[n]:
                red_end_list.append(red_end[n])
else:
    for i in range(0, len(red_start)-1):
        n=0
        while red_start[i] >= red_end[n]:
            n+=1
            if red_start[i] < red_end[n]:
                red_end_list.append(red_end[n])
    red_end_list.append(red_start[len(red_start)-1])
print(red_end_list)


blue_start_list=[]
blue_end_list=[]
for idx in range(1, last_idx):
    if df.loc[idx, 'UL'] > df.loc[idx,'LS_A'] > df.loc[idx-1,'Price'] > df.loc[idx,'LS_B'] > df.loc[idx,'Price'] or\
    df.loc[idx, 'UL'] > df.loc[idx,'LS_B'] > df.loc[idx-1,'Price'] > df.loc[idx,'LS_A'] > df.loc[idx,'Price']:
        df.loc[idx,'Cond.b']='blue_start'
        blue_start_list.append(idx)
    elif df.loc[idx,'LL'] < df.loc[idx-1,'LL'] and df.loc[idx,'LL'] < df.loc[idx+1,'LL']:
        df.loc[idx,'Cond.b']='blue_end'
    else:
        pass
print(blue_start_list)

blue_start = df.loc[df['Cond.b']=='blue_start'].index
blue_end = df.loc[df['Cond.b']=='blue_end'].index
if blue_start[-1] < blue_end[-1]:
    for i in range(0, len(blue_start)):
        n=0
        while blue_start[i] >= blue_end[n]:
            n+=1
            if blue_start[i] < blue_end[n]:
                blue_end_list.append(blue_end[n])
else:
    for i in range(0, len(blue_start)-1):
        n=0
        while blue_start[i] >= blue_end[n]:
            n+=1
            if blue_start[i] < blue_end[n]:
                blue_end_list.append(blue_end[n])
    blue_end_list.append(blue_start[len(blue_start)-1])
print(blue_end_list)


print(df)
df.to_excel(file+', graph.xlsx')


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

plt.plot(date, df['ML'][:last_idx+1], label='BB_ML', color='green', ls="--", lw=0.4, alpha=0.6)
plt.plot(date, df['UL'][:last_idx+1], label='BB_UL', color='red', lw=0.4)
plt.plot(date, df['LL'][:last_idx+1], label='BB_LL', color='blue', lw=0.4)

red_s=red_start_list
red_e=red_end_list
blue_s=blue_start_list
blue_e=blue_end_list
for i in range(0, len(red_s)):
    plt.axvspan(date[red_s[i]], date[red_e[i]], alpha=0.3, color='red')
    plt.hlines(max(df.loc[red_s[i]:red_e[i], 'Price']), date[red_s[i]], date[red_e[i]], color='green')
    plt.text(date[red_s[i]], max(df.loc[red_s[i]:red_e[i], 'Price'])+1, max(df.loc[red_s[i]:red_e[i], 'Price']), ha='left', alpha=0.5)
for i in range(0, len(blue_s)):
    plt.axvspan(date[blue_s[i]], date[blue_e[i]], alpha=0.3, color='blue')
    plt.hlines(min(df.loc[blue_s[i]:blue_e[i], 'Price']), date[blue_s[i]], date[blue_e[i]], color='yellow')
    plt.text(date[blue_s[i]], min(df.loc[blue_s[i]:blue_e[i], 'Price'])-2.5, min(df.loc[blue_s[i]:blue_e[i], 'Price']), ha='center', alpha=0.5)

plt.title(f'USD/BTC, SMA +/-365ATR,  for {last_idx}days', fontsize=20)
plt.grid(axis='x')
plt.legend()

plt.savefig(file + ', graph.png', dpi=150)