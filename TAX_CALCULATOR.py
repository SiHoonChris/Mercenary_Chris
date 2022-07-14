# 금융 활동(국내외 주식 매매, 가상자산 매매, 배당과 이자)에서 발생하는 소득에 대한 세액 계산

import datetime
today=datetime.date.today()
# td=datetime.timedelta(days=365*4)
# today=today+td
intro=datetime.date(2025,1,1)


# 1. 금융소득종합과세(2021년 기준 누진세율)
def Global_Income_Taxation():
    while True:
        try:
            Div_Int=int(input("a. 금융소득(배당+이자) : "))
            if Div_Int <= 20000000:
                print("1. 금융소득종합과세 대상자 아님")
                return Div_Int, int(0)
            elif Div_Int > 20000000:
                other_income=int(input("   종합소득(근로·사업·연금·퇴직 등에 따른 소득) : "))
                global_income=other_income+Div_Int
                if 20000000 < global_income <= 46000000 :
                    GIT_F=Div_Int*0.15-1080000*(Div_Int/global_income)
                    print("1. (종합소득세 중) 금융소득에 대한 과세 : {0:,}(원)".format(round(GIT_F)))
                    return Div_Int, round(GIT_F)
                elif 46000000 < global_income <= 88000000 : 
                    GIT_F=Div_Int*0.24-5220000*(Div_Int/global_income)
                    print("1. (종합소득세 중) 금융소득에 대한 과세 : {0:,}(원)".format(round(GIT_F)))
                    return Div_Int, round(GIT_F)
                elif 88000000 < global_income <= 150000000 : 
                    GIT_F=Div_Int*0.35-14900000*(Div_Int/global_income)
                    print("1. (종합소득세 중) 금융소득에 대한 과세 : {0:,}(원)".format(round(GIT_F)))
                    return Div_Int, round(GIT_F)
                elif 150000000 < global_income <= 300000000 :
                    GIT_F=Div_Int*0.38-19400000*(Div_Int/global_income)
                    print("1. (종합소득세 중) 금융소득에 대한 과세 : {0:,}(원)".format(round(GIT_F)))
                    return Div_Int, round(GIT_F)
                elif 300000000 < global_income <= 500000000 :
                    GIT_F=Div_Int*0.4-25400000*(Div_Int/global_income)
                    print("1. (종합소득세 중) 금융소득에 대한 과세 : {0:,}(원)".format(round(GIT_F)))
                    return Div_Int, round(GIT_F)
                elif 500000000 < global_income <= 1000000000 : 
                    GIT_F=Div_Int*0.42-35400000*(Div_Int/global_income)
                    print("1. (종합소득세 중) 금융소득에 대한 과세 : {0:,}(원)".format(round(GIT_F)))
                    return Div_Int, round(GIT_F)
                elif 1000000000 < global_income :
                    GIT_F=Div_Int*0.45-65400000*(Div_Int/global_income)
                    print("1. (종합소득세 중) 금융소득에 대한 과세 : {0:,}(원)".format(round(GIT_F)))
                    return Div_Int, round(GIT_F)
            else:
                raise ValueError
        except:
            print("   입력 오류 : 문자 X / 숫자 사이 쉼표, 띄어쓰기 X")


# 2. 금융투자소득세(양도소득세)
# 2-1. 현재   * 보유기간(전종목 1년 이상 보유한 것으로 판단) 및 기업 규모에 따른 과세 차이는 제외
def YOON_Transfer_Income_Taxation():
    while True:
        try:
            DS_Income = int(input("b. 국내주식 양도소득 : "))
            FS_Income = int(input("c. 국외주식 양도소득 : "))

            print("** 대주주 요건 **")
            print("    => 국내 주식시장 내 개별종목에 대해 100억원 이상 보유")
            print("    => 국외주식에 대해서는 대주주 요건 해당 없음")
            Check=input("   대주주 요건 충족하는지? (네: Y , 아니오: N) :  ")

            while Check != "Y" or Check != "y" or Check != "N" or Check != "n":
                if Check=="Y" or Check=="y":
                    TaxBase=DS_Income+FS_Income-2500000
                    if TaxBase <= 2500000:
                        TaxBase=0
                        print("2. 양도소득세 과세 대상자 아님   * 과세표준 : {0:,}(원)".format(TaxBase))
                        return DS_Income, FS_Income, int(0)
                    else:
                        if TaxBase <= 300000000:
                            YTIT=TaxBase*0.22
                            print("2. 양도소득세 : {0:,}(원)   * 과세표준 : {1:,}(원)".format(round(YTIT), TaxBase))
                            return DS_Income, FS_Income, int(YTIT)
                        else:
                            YTIT=TaxBase*0.275-300000000*0.055
                            print("2. 양도소득세 : {0:,}(원)   * 과세표준 : {1:,}(원)".format(round(YTIT), TaxBase))
                            return DS_Income, FS_Income, int(YTIT)

                elif Check=="N" or Check=="n":
                    if FS_Income <= 2500000:
                        TaxBase=0
                        print("2. 양도소득세 과세 대상자 아님   * 과세표준 : {0:,}(원)".format(TaxBase))
                        return DS_Income, FS_Income, int(0)
                    else:
                        TaxBase=FS_Income-2500000
                        YTIT=TaxBase*0.22
                        print("2. 양도소득세 : {0:,}(원)   * 과세표준 : {1:,}(원)".format(round(YTIT), TaxBase))
                        return DS_Income, FS_Income, int(YTIT)

                print("   입력 오류 : 입력내용 다시 확인 바랍니다(대/소문자 구분 확인)")
                Check=input("   대주주 요건 충족하는지? (네: Y , 아니오: N) :  ")
        
        except ValueError:
            print("   입력 오류 : 문자 X / 숫자 사이 쉼표, 띄어쓰기 X")

# 2-2. 예정   * 2025년까지 연기 / 이월결손금, 반기 원천징수 등에 대한 관련 내용 제외
def Transfer_Income_Taxation():
    while True:
        try:
            DS_Income=int(input("b. 국내주식 양도소득 : "))
            if DS_Income <= 50000000:
                TaxBase_DS=0
            else:
                TaxBase_DS=DS_Income-50000000

            FS_Income=int(input("c. 국외주식 양도소득 : "))
            if FS_Income <= 2500000:
                TaxBase_FS=0
            else:
                TaxBase_FS=FS_Income-2500000

            TaxBase=TaxBase_DS+TaxBase_FS

            if TaxBase <= 300000000:
                TIT=TaxBase*0.22
                if TIT == 0:
                    print("2. 금융투자소득세(양도소득세) 과세 대상자 아님   * 과세표준 : {0:,}".format(TaxBase))
                    return DS_Income, FS_Income, int(TIT)
                else:
                    print("2. 금융투자소득세(양도소득세) : {0:,}(원)   * 과세표준 : {1:,}".format(round(TIT), TaxBase))
                    return DS_Income, FS_Income, int(TIT)
            else:
                TIT=TaxBase*0.275-300000000*0.055
                print("2. 금융투자소득세(양도소득세) : {0:,}(원)   * 과세표준 : {1:,}".format(round(TIT), TaxBase))
                return DS_Income, FS_Income, int(TIT)

        except ValueError:
            print("   입력 오류 : 문자 X / 숫자 사이 쉼표, 띄어쓰기 X")


# 3. 기타소득세(가상자산과 현물자산 간의 거래에 대한)   * (2025년까지 연기) / 교환거래(가상자산 간의 거래)로 인한 소득 금액은 다루지 않았음
def CryptoCurrency_Taxation():
    while True:
        try:
            C_Income=int(input("d. 가상자산 소득 : "))
            if C_Income > 2500000:
                C_Income_Tax=(C_Income-2500000)*0.20
                print("3. 가상자산소득세(기타소득세) : {0:,}(원)".format(round(C_Income_Tax)))
                return C_Income, round(C_Income_Tax)
            else:
                print("3. 가상자산소득세(기타소득세) 대상자 아님")
                return C_Income, int(0)
        except ValueError:
            print("   입력 오류 : 문자 X / 숫자 사이 쉼표, 띄어쓰기 X")


# 4. 세액 총합
def Tax_Sum():
    print("* 안내 : 금융 활동에서 발생한 소득의 세금에 대한 계산기임.")
    print("         (근로 소득 등의 다른 소득원에 대해서는 다루지 않음)\n")

    if today < intro: # 도입 전(2025년 이전)
        Div_Int, Div_Int_Tax = Global_Income_Taxation()
        DS_Income, FS_Income, DFS_Income_Tax = YOON_Transfer_Income_Taxation()
        C_Income, C_Income_Tax = CryptoCurrency_Taxation()
        C_Income_Tax=0
    else: #도입 후(2025년부터, 이후)
        Div_Int, Div_Int_Tax = Global_Income_Taxation()
        DS_Income, FS_Income, DFS_Income_Tax = Transfer_Income_Taxation()
        C_Income, C_Income_Tax = CryptoCurrency_Taxation()

    print("-"*50)
    print("4. 세액 계산 결과 ({0})".format(today))
    print("   a. 금융소득(배당+이자) : {0:,}원".format(Div_Int))
    print("   b. 국내주식 양도소득   : {0:,}원".format(DS_Income))
    print("   c. 국외주식 양도소득   : {0:,}원".format(FS_Income))
    print("   d. 가상자산 소득       : {0:,}원".format(C_Income))
    Earning_Before_Tax = Div_Int+DS_Income+FS_Income+C_Income
    print("   세전 수익: {0:,}원   * (a + b + c + d)\n".format(Earning_Before_Tax))

    print("   1. 종합소득세(배당, 이자) : {0:,}원".format(Div_Int_Tax))
    print("   2. 양도소득세(국내외주식) : {0:,}원".format(DFS_Income_Tax))
    print("   3. 기타소득세(가상자산)   : {0:,}원".format(C_Income_Tax))
    Sum_Tax = Div_Int_Tax+DFS_Income_Tax+C_Income_Tax

    print("   세금 지출: {0:,}원   * (1 + 2 + 3)\n".format(Sum_Tax))
    Earning_After_Tax = Earning_Before_Tax-(Div_Int_Tax+DFS_Income_Tax+C_Income_Tax)

    print("   세후 수익: {0:,}원   * (a + b + c + d) - (1 + 2 + 3)".format(Earning_After_Tax))
    print("-"*50)

    quit=str(input("프로그램 종료('Q' 누르기) : "))
    if quit == "q" or "Q":
        print("=> 이용해주셔서 감사합니다.")


if __name__=="__main__":
    Tax_Sum()