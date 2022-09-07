import matplotlib.pyplot as plt
import pandas as pd
def trim(df):
    df.sort_index(ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.drop(columns=df.columns[2:], inplace=True)
    # df.rename(columns={'날짜': 'Date', '종가': 'Price'}, inplace=True)
    # (* kr.investing.com에서 자료 가져왔을 때 사용)
def ICMK_CL(last_idx):  # 일목균형표:전환선
    for i in df.index:
        if i < 8:
            df.loc[i,'CL']=''
        elif 8 <= i <= last_idx:
            max_value=max(df.loc[i-8:i , 'Price'])
            min_value=min(df.loc[i-8:i , 'Price'])
            df.loc[i,'CL']=(max_value+min_value)/2
        else:
            df.loc[i,'CL']=''
def ICMK_BL(last_idx):  # 일목균형표:기준선
    for i in df.index:
        if i < 25:
            df.loc[i,'BL']=''
        elif 25 <= i <= last_idx:
            max_value=max(df.loc[i-25:i , 'Price'])
            min_value=min(df.loc[i-25:i , 'Price'])
            df.loc[i,'BL']=(max_value+min_value)/2
        else:
            df.loc[i,'BL']=''
def ICMK_LS_A(last_idx):  # 일목균형표:선행스팬1
    for i in df.index:
        if i < 25:
            df.loc[i,'LS_A']=''
            df.loc[i+26,'LS_A']=''
        elif 25 <= i <= last_idx:
            df.loc[i+26,'LS_A']=(df.loc[i,'CL']+df.loc[i,'BL'])/2
        else:
            pass
def ICMK_LS_B(last_idx):  # 일목균형표:선행스팬2
    for i in df.index:
        if i < 51:
            df.loc[i,'LS_B']=''
            df.loc[i+26,'LS_B']=''
        elif 51 <= i <= last_idx:
            max_value=max(df.loc[i-51:i , 'Price'])
            min_value=min(df.loc[i-51:i , 'Price'])
            df.loc[i+26, 'LS_B']=(max_value+min_value)/2
        else:
            pass
def BB_Band(last_idx):# 볼린저밴드(중심선, 상단선, 하단선)
    for i in range(0, last_idx+1):
        if i > 18:
            df.loc[i,'ML']=df.loc[i-19:i,'Price'].mean()
            df.loc[i,'UL']=df.loc[i,'ML'] + df.loc[i-19:i,'Price'].std()*2
            df.loc[i,'LL']=df.loc[i,'ML'] - df.loc[i-19:i,'Price'].std()*2
        else:
            pass



# 데이터 생성
df=pd.read_csv('GOOGL Historical Data.csv')  # 21.9.7~22.9.2, 출처; investing.com
file_name='GOOGL, 21.9.7~22.9.2, TTI-signal'
trim(df)

acols=['CL', 'BL', 'LS_A', 'LS_B', 'ML', 'UL', 'LL', 'Cond.']
for col in acols:
    df[col]=''

last_idx=df.index[-1]

for i in range(1, 26):
    df.loc[last_idx+i] = ['', '', '', '', '', '', '', '', '', '']

ICMK_CL(last_idx)
ICMK_BL(last_idx)
ICMK_LS_A(last_idx)
ICMK_LS_B(last_idx)
BB_Band(last_idx)

bcols=['Price', 'CL', 'BL', 'LS_A', 'LS_B', 'ML', 'UL', 'LL']
for col in bcols:
    df[col] = pd.to_numeric(df[col], errors='coerce')


# Condition for Red Area
red_start_list=[]
red_end_list=[]
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
for i in range(0, len(red_start)):
    n=0
    while red_start[i] >= red_end[n]:
        n+=1
        if red_start[i] < red_end[n]:
            red_end_list.append(red_end[n])

# Condition for Blue Area
blue_start_list=[]
blue_end_list=[]
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
for i in range(0, len(blue_start)):
    n=0
    while blue_start[i] >= blue_end[n]:
        n+=1
        if blue_start[i] < blue_end[n]:
            blue_end_list.append(blue_end[n])

print(df)
df.to_excel(file_name+'.xlsx')



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
    
plt.title(file_name, fontsize=18)
plt.xticks([df.loc[0,'Date'], df.loc[last_idx,'Date']])
plt.legend(ncol=6, loc=(0.025, 0.925))

plt.savefig(file_name+'.png', dpi=150)


# 4. 3년치 데이터에 대해 적용한 내용을 한정된 공간 안에서 모두 출력하자니 눈에 잘 안들어온다.
# 6. 그래프에서 각 선의 두께 때문에 잘못된 인지가 생긴다. 캔들차트 상에서 구현하면 한 눈에 알아볼 수 있을 텐데

# 7. 일목균형표 계산식 수정
#    (Investing.com은 주가를 소수점 둘째자리까지 반올림하여 기록, 실제 가격과 조금 차이남)
#    (그렇기에 어쩔 수 없이 Price에서 파생된 계산들이 실제값과 다를 수 밖에 없음)
# 8. 그래프, 이미지 파일, 엑셀 파일 의 타이틀 한 번에 적용
# 9. HTS의 OpenAPI를 활용하면, 일목균형표와 볼린저밴드는 기본으로 제공되는 내용이니까,
#    더 간편하게, 더 정확하게 값을 출력할 수 있지 않을까??