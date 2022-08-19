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
df['구름대']='미정'
df['추세']='미정'

last_idx=df.index[-1]
for i in range(1, 26):
    df.loc[last_idx+i] = ['', '', '', '', '', '', '미정', '미정']

print(df)
df.to_csv('일목균형표 중간점검.csv', encoding='utf-8-sig')