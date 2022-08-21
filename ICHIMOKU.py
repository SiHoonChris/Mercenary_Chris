import pandas as pd

# 데이터 가공 : 기본 프레임
df = pd.read_csv('IVV, 21.01.01~21.12.31.csv')
df.sort_index(ascending=False, inplace=True)
df.reset_index(drop=True, inplace=True)

df.drop(columns=['오픈', '고가', '저가', '거래량', '변동 %'], inplace=True)
df['전환선']=0
df['기준선']=0
df['선행스팬A(1)']=0
df['선행스팬B(2)']=0
df['구름대']=''
df['추세']=''

last_idx=df.index[-1]
for i in range(1, 26):
    df.loc[last_idx+i] = ['', 0, '', '', 0, 0, '', '미정']

# 전환선
for i in df.index:
    if i < 9:
        df.loc[i, '전환선']=''
    elif 9 <= i <= last_idx:
        max_value=max(df.loc[i-9:i-1 , '종가'])
        min_value=min(df.loc[i-9:i-1 , '종가'])
        df.loc[i, '전환선']=(max_value+min_value)/2
    else:
        df.loc[i, '전환선']=''
        
# 기준선
for i in df.index:
    if i < 26:
        df.loc[i, '기준선']=''
    elif 26 <= i <= last_idx:
        max_value=max(df.loc[i-26:i-1 , '종가'])
        min_value=min(df.loc[i-26:i-1 , '종가'])
        df.loc[i, '기준선']=(max_value+min_value)/2
    else:
        df.loc[i, '기준선']=''

# 선행스팬A(1)
for i in df.index:
    if i < 26:
        df.loc[i, '선행스팬A(1)']=0
        df.loc[i+25, '선행스팬A(1)']=0
    elif 26 <= i <= last_idx:
        df.loc[i+25, '선행스팬A(1)']=(df.loc[i, '전환선']+df.loc[i, '기준선'])/2
    else:
        pass
    
# 선행스팬B(2)
for i in df.index:
    if i < 51:
        df.loc[i, '선행스팬B(2)']=0
        df.loc[i+25, '선행스팬B(2)']=0
    elif 51 <= i <= last_idx:
        max_value=max(df.loc[i-51:i , '종가'])
        min_value=min(df.loc[i-51:i , '종가'])
        df.loc[i+25, '선행스팬B(2)']=(max_value+min_value)/2
    else:
        pass
    
# 구름대
for i in df.index:
    if df.loc[i, '선행스팬B(2)']==0:
        pass
    else:
        if df.loc[i, '선행스팬A(1)'] > df.loc[i, '선행스팬B(2)']:
            df.loc[i, '구름대'] = '양운'
        elif df.loc[i, '선행스팬A(1)'] < df.loc[i, '선행스팬B(2)']:
            df.loc[i, '구름대'] = '음운'
        else:
            df.loc[i, '구름대'] = '구름선'
            
# 추세
for i in df.index:
    if df.loc[i, '선행스팬B(2)']==0 or df.loc[i, '종가']==0:
        pass
    else:
        if df.loc[i, '종가'] > df.loc[i, '선행스팬A(1)'] and df.loc[i, '종가'] > df.loc[i, '선행스팬B(2)']:
            df.loc[i, '추세'] = '상승'
        elif df.loc[i, '종가'] < df.loc[i, '선행스팬A(1)'] and df.loc[i, '종가'] < df.loc[i, '선행스팬B(2)']:
            df.loc[i, '추세'] = '하락'
        else:
            df.loc[i, '추세'] = '전환'
            
# 데이터 가공 : 정리
for i in range(1, 26):
    df.loc[last_idx+i, '종가'] = ''
for i in df.index:
    if df.loc[i, '선행스팬A(1)']==0:
        df.loc[i, '선행스팬A(1)']=''
    if df.loc[i, '선행스팬B(2)']==0:
        df.loc[i, '선행스팬B(2)']=''

print(df)
df.to_excel('일목균형표(IVV, 21.01.01~21.12.31).xlsx')