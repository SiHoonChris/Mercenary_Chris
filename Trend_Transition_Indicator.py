import matplotlib.pyplot as plt
import pandas as pd
def trim(df):
    df.sort_index(ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.drop(columns=df.columns[2:], inplace=True)
    # df.rename(columns={'날짜': 'Date', '종가': 'Price'}, inplace=True)
    # (* kr.investing.com에서 자료 가져왔을 때 사용)

# 데이터 생성
df=pd.read_csv('AAPL Historical Data.csv')  # 19.8.27~22.8.26, 출처; investing.com
trim(df)

df['CL']=''
df['BL']=''
df['LS_A']=''
df['LS_B']=''
df['ML']=''
df['UL']=''
df['LL']=''
df['Cond.1']=''
df['Cond.2']=''
df['Cond.3']=''

last_idx=df.index[-1]
for i in range(1, 26):
    df.loc[last_idx+i] = ['', '', '', '', '', '', '', '', '', '', '', '']

# 일목균형표:전환선
for i in df.index:
    if i < 9:
        df.loc[i,'CL']=''
    elif 9 <= i <= last_idx:
        max_value=max(df.loc[i-9:i-1 , 'Price'])
        min_value=min(df.loc[i-9:i-1 , 'Price'])
        df.loc[i,'CL']=(max_value+min_value)/2
    else:
        df.loc[i,'CL']=''
# 일목균형표:기준선
for i in df.index:
    if i < 26:
        df.loc[i,'BL']=''
    elif 26 <= i <= last_idx:
        max_value=max(df.loc[i-26:i-1 , 'Price'])
        min_value=min(df.loc[i-26:i-1 , 'Price'])
        df.loc[i,'BL']=(max_value+min_value)/2
    else:
        df.loc[i,'BL']=''
# 일목균형표:선행스팬1
for i in df.index:
    if i < 26:
        df.loc[i,'LS_A']=''
        df.loc[i+25,'LS_A']=''
    elif 26 <= i <= last_idx:
        df.loc[i+25,'LS_A']=(df.loc[i,'CL']+df.loc[i,'BL'])/2
    else:
        pass
# 일목균형표:선행스팬2
for i in df.index:
    if i < 51:
        df.loc[i,'LS_B']=''
        df.loc[i+25,'LS_B']=''
    elif 51 <= i <= last_idx:
        max_value=max(df.loc[i-51:i , 'Price'])
        min_value=min(df.loc[i-51:i , 'Price'])
        df.loc[i+25, 'LS_B']=(max_value+min_value)/2
    else:
        pass
# 볼린저밴드(중심선, 상단선, 하단선)
for i in range(0, last_idx+1):
    if i > 18:
        df.loc[i,'ML']=df.loc[i-19:i,'Price'].mean()
        df.loc[i,'UL']=df.loc[i,'ML'] + df.loc[i-19:i,'Price'].std()*2
        df.loc[i,'LL']=df.loc[i,'ML'] - df.loc[i-19:i,'Price'].std()*2
    else:
        pass

df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['CL'] = pd.to_numeric(df['CL'], errors='coerce')
df['BL'] = pd.to_numeric(df['BL'], errors='coerce')
df['BL'] = pd.to_numeric(df['BL'], errors='coerce')
df['LS_A'] = pd.to_numeric(df['LS_A'], errors='coerce')
df['LS_B'] = pd.to_numeric(df['LS_B'], errors='coerce')
df['ML'] = pd.to_numeric(df['ML'], errors='coerce')
df['UL'] = pd.to_numeric(df['UL'], errors='coerce')
df['LL'] = pd.to_numeric(df['LL'], errors='coerce')

# Condition 1~3
for i in range(1, last_idx+1):
    if df.loc[i,'Price'] > df.loc[i,'LS_A'] and df.loc[i-1,'Price'] < df.loc[i, 'LS_B'] < df.loc[i,'Price']:
        df.loc[i,'Cond.1']='O'
    elif df.loc[i,'Price'] > df.loc[i,'LS_B'] and df.loc[i-1,'Price'] < df.loc[i, 'LS_A'] < df.loc[i,'Price']:
        df.loc[i,'Cond.1']='O'

for i in range(1, last_idx+1):
    if df.loc[i-1,'UL'] < df.loc[i,'UL'] and df.loc[i+1,'UL'] < df.loc[i,'UL'] and\
    df.loc[i,'LL'] < df.loc[i,'LS_A'] and df.loc[i,'LL'] < df.loc[i,'LS_B']:
        df.loc[i,'Cond.2']='O'


print(df)
df.to_excel('AAPL, 19.8.27~22.8.26, TTI-signal.xlsx')


# 데이터 시각화
plt.figure(figsize=(18, 12))

date=df['Date'][:last_idx+1]
LS_A=df['LS_A'][:last_idx+1]
LS_B=df['LS_B'][:last_idx+1]
plt.plot(date, df['Price'][:last_idx+1], label='Price', color='black')
plt.plot(date, LS_A, label='ICMK_LS_A', color='orange', alpha=0.5)
plt.plot(date, LS_B, label='ICMK_LS_B', color='skyblue', alpha=0.5)
plt.plot(date, df['ML'][:last_idx+1], label='BB_ML', color='green', ls="--", lw=0.75, alpha=0.6)
plt.plot(date, df['UL'][:last_idx+1], label='BB_UL', color='red', lw=0.75)
plt.plot(date, df['LL'][:last_idx+1], label='BB_LL', color='blue', lw=0.75)
plt.fill_between(date, LS_A, LS_B, where=(LS_A >= LS_B), color='orange', alpha=0.5, interpolate=True)
plt.fill_between(date, LS_A, LS_B, where=(LS_A < LS_B), color='skyblue', alpha=0.5, interpolate=True)

for i in range(1, last_idx+1):
    if df.loc[i,'Cond.1']=='O':
        plt.axvline(x=date[i], lw=0.5, color='purple')
for i in range(1, last_idx+1):
    if df.loc[i,'Cond.2']=='O':
        plt.axvline(x=date[i], lw=0.5, color='yellow')

plt.title('AAPL, 19.8.27~22.8.26, TTI-signal', fontsize=18)
plt.xticks([df.loc[0,'Date'], df.loc[last_idx,'Date']])
plt.legend(ncol=6, loc=(0.025, 0.925))

plt.savefig('AAPL, 19.8.27~22.8.26, TTI-signal.png')


# To-do
# Condition 1~3 구현하려면 고민 좀 해야할 듯
# Cond.1에 해당하는 값(선)이 생성되어야 Cond.2에 대한 값(선)이 생성되도록 설계
# Cond.1에 해당하는 값(선)이 생성된 후 새로운 Cond.1이 생성되면, 이전 값 삭제
# Cond.2는 무조건 Cond.1이 먼저 생성된 다음에 생성 가능
# 참고
# Condition.1 - 종가가 일목균형표 구름대 상향 돌파(이 때 볼린저밴드 하단선은 일목균형표 구름 아래 위치)
# Condition.2 - 1)이 발생한 시점 이후에, 볼린저밴드의 상단선의 n자 모양 형성(접선의 기울기=0)  
# Condition.3 - 2)가 발생한 시점 이후에, 1)과 2)가 발생한 시점 사이에 형성된 종가의 최고가 보다 높은 종가 형성