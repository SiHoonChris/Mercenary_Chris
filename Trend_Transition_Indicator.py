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
df['Cond.']=''

last_idx=df.index[-1]
for i in range(1, 26):
    df.loc[last_idx+i] = ['', '', '', '', '', '', '', '', '', '']

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

# Condition for Red Area
red_start_list=[]
for idx in range(1, last_idx):
    if df.loc[idx,'Price'] > df.loc[idx,'LS_B'] > df.loc[idx-1,'Price'] > df.loc[idx,'LS_A'] > df.loc[idx, 'LL'] or\
    df.loc[idx,'Price'] > df.loc[idx,'LS_A'] > df.loc[idx-1,'Price'] > df.loc[idx,'LS_B'] > df.loc[idx, 'LL']:
        df.loc[idx,'Cond.']='red_start'
        red_start_list.append(idx)
    elif df.loc[idx,'UL'] > df.loc[idx-1,'UL'] and df.loc[idx,'UL'] > df.loc[idx+1,'UL']:
        df.loc[idx,'Cond.']='red_end'
    else:
        pass
red_start = df.loc[df['Cond.']=='red_start'].index
red_end = df.loc[df['Cond.']=='red_end'].index
red_end_list=[]
for i in range(0, len(red_start)):
    n=0
    while red_start[i] >= red_end[n]:
        n+=1
        if red_start[i] < red_end[n]:
            red_end_list.append(red_end[n])
print(red_start_list)
print(red_end_list)

# Condition for Blue Area
blue_start_list=[]
for idx in range(1, last_idx):
    if df.loc[idx, 'UL'] > df.loc[idx,'LS_A'] > df.loc[idx-1,'Price'] > df.loc[idx,'LS_B'] > df.loc[idx,'Price'] or\
    df.loc[idx, 'UL'] > df.loc[idx,'LS_B'] > df.loc[idx-1,'Price'] > df.loc[idx,'LS_A'] > df.loc[idx,'Price']:
        df.loc[idx,'Cond.']='blue_start'
        blue_start_list.append(idx)
    elif df.loc[idx,'LL'] < df.loc[idx-1,'LL'] and df.loc[idx,'LL'] < df.loc[idx+1,'LL']:
        df.loc[idx,'Cond.']='blue_end'
    else:
        pass
blue_start = df.loc[df['Cond.']=='blue_start'].index
blue_end = df.loc[df['Cond.']=='blue_end'].index
blue_end_list=[]
for i in range(0, len(blue_start)):
    n=0
    while blue_start[i] >= blue_end[n]:
        n+=1
        if blue_start[i] < blue_end[n]:
            blue_end_list.append(blue_end[n])
print(blue_start_list)
print(blue_end_list)

print(df)
df.to_excel('AAPL, 19.8.27~22.8.26, TTI-signal.xlsx')


# 데이터 시각화
plt.figure(figsize=(18, 12))

date=df['Date'][:last_idx+1]
LS_A=df['LS_A'][:last_idx+1]
LS_B=df['LS_B'][:last_idx+1]
plt.plot(date, df['Price'][:last_idx+1], label='Price', color='black', lw=0.8)
plt.plot(date, LS_A, label='ICMK_LS_A', color='orange', lw=0.6)
plt.plot(date, LS_B, label='ICMK_LS_B', color='skyblue', lw=0.6)
plt.plot(date, df['ML'][:last_idx+1], label='BB_ML', color='green', ls="--", lw=0.4, alpha=0.6)
plt.plot(date, df['UL'][:last_idx+1], label='BB_UL', color='red', lw=0.4)
plt.plot(date, df['LL'][:last_idx+1], label='BB_LL', color='blue', lw=0.4)
plt.fill_between(date, LS_A, LS_B, where=(LS_A >= LS_B), color='orange', alpha=0.3, interpolate=True)
plt.fill_between(date, LS_A, LS_B, where=(LS_A < LS_B), color='skyblue', alpha=0.3, interpolate=True)

for i in range(0, len(red_start_list)):
    plt.axvspan(date[red_start_list[i]], date[red_end_list[i]], alpha=0.3, color='red')
    plt.hlines(max(df.loc[red_start_list[i]:red_end_list[i], 'Price']), date[red_start_list[i]], date[red_end_list[i]], color='green')
    plt.text(date[red_start_list[i]], max(df.loc[red_start_list[i]:red_end_list[i], 'Price'])+1, max(df.loc[red_start_list[i]:red_end_list[i], 'Price']), ha='left', alpha=0.5)
for i in range(0, len(blue_start_list)):
    plt.axvspan(date[blue_start_list[i]], date[blue_end_list[i]], alpha=0.3, color='blue')
    plt.hlines(min(df.loc[blue_start_list[i]:blue_end_list[i], 'Price']), date[blue_start_list[i]], date[blue_end_list[i]], color='yellow')
    plt.text(date[blue_start_list[i]], min(df.loc[blue_start_list[i]:blue_end_list[i], 'Price'])-2.5, min(df.loc[blue_start_list[i]:blue_end_list[i], 'Price']), ha='center', alpha=0.5)
    
plt.title('AAPL, 19.8.27~22.8.26, TTI-signal', fontsize=18)
plt.xticks([df.loc[0,'Date'], df.loc[last_idx,'Date']])
plt.legend(ncol=6, loc=(0.025, 0.925))

plt.savefig('AAPL, 19.8.27~22.8.26, TTI-signal.png', dpi=150)


# 1.
# 1) 상향추세로의 전환 중 양운을 뚫고 올라가는 케이스
# 2) 하향추세로의 전환 중 음운을 뚫고 내려가는 케이스
# 1), 2)에 대한 내용 추가
# 2.
# Colored-Column 내에 horizontal line의 가격 표시
# 3.
# 이미지 저장시 dpi 조절

# 4. 3년치 데이터에 대해 적용한 내용을 한정된 공간 안에서 모두 출력하자니 눈에 잘 안들어온다.
# 5. 코드가 더럽게 쓰여졌다. 좀 깔끔하고, 처음보는 사람도 한 눈에 알아볼 수 있도록 명시적으로 정리할 필요가 있겠다.
# 6. 그래프에서 각 선의 두께 때문에 잘못된 인지가 생긴다. 캔들차트 상에서 구현하면 한 눈에 알아볼 수 있을 텐데