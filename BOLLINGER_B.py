import matplotlib
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
import matplotlib.pyplot as plt
import pandas as pd
def file_trimmer(df): # kr.investing.com의'과거 데이터'에서 가져온 자료, 순서 정리 및 불필요한 내용 삭제
    df.sort_index(ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.drop(columns=['오픈', '고가', '저가', '거래량', '변동 %'], inplace=True)


# 데이터 생성
df = pd.read_csv('KO 역사적 데이터.csv') # Coca-Cola, 19.8.27~22.8.27, kr.investing.com
file_trimmer(df)

# 중심선 ; 20일 이동평균선(SMA)
# 상한선 ; 중심선 + (20일 동안의 표준편차 * 2)
# 하한선 ; 중심선 - (20일 동안의 표준편차 * 2)
for i in range(0, df.index[-1]+1):
    if i > 18:
        df.loc[i,'Mid-line']=df.loc[i-19:i,'종가'].mean()
        df.loc[i,'Upper-line']=df.loc[i,'Mid-line'] + df.loc[i-19:i,'종가'].std()*2
        df.loc[i,'Lower-line']=df.loc[i,'Mid-line'] - df.loc[i-19:i,'종가'].std()*2
    else:
        pass
print(df)
df.to_excel('BB-KO.xlsx')

# 데이터 시각화
plt.figure(figsize=(20, 12))

plt.plot(df['날짜'], df['종가'], color='black', alpha=0.5, label='Price')
plt.plot(df['날짜'], df['Mid-line'], color='g', label='Mid-line')
plt.plot(df['날짜'], df['Upper-line'], color='r', label='Upper-line')
plt.plot(df['날짜'], df['Lower-line'], color='b', label='Lower-line')

plt.xticks([df.loc[0,'날짜'], df.loc[df.index[-1],'날짜']])
plt.text(df['종가'].idxmax(), max(df['종가'])+0.3, max(df['종가']), ha='center')
plt.text(df['종가'].idxmin(), min(df['종가'])-0.5, min(df['종가']), ha='center')

plt.title("BB, KO: Coca-Cola, '19.8.27~'22.8.26", fontsize=20)
plt.legend(loc=(0.02,0.85))

plt.savefig('BOLLINGER-BAND, KO.png')