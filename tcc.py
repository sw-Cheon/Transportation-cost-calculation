import re
import ssl
import urllib.request
from urllib import parse
from bs4 import BeautifulSoup

class transportation_Cost_Calculation():

    def __init__(self):
        self.highway = '고속도로'
        self.highways = []
        self.general_Road = []
        self.highway_Fuel_Efficiency = 0
        self.general_Road_Fuel_Efficiency = 0
        self.context = ssl._create_unverified_context()
        self.oil_Cost = 0
        self.road_Fare = ''
        self.result = ""
        self.oil_GSL = 'https://finance.naver.com/marketindex/oilDetail.nhn?marketindexCd=OIL_GSL' # 휘발유
        self.oil_LO = 'https://finance.naver.com/marketindex/oilDetail.nhn?marketindexCd=OIL_LO' # 경유

    def help(self):
        print("\n 1. 아래에 있는 url을 복사하고 인터넷 url창에\n    입력하여 Kakao map을 실행해 주세요.\n    (혹은 url에 Ctrl + 마우스 좌측클릭)")
        print("    =========================================")
        print("    https://m.map.kakao.com/actions/routeView")
        print("    =========================================")
        print(" \n 완료 시 아무키나 입력해주세요.")
        k = input(" > ")
        if k == 'q':
            return
        print("\n 2. 출발지와 도착지를 입력하고\n    자동차 아이콘을 눌러 자동차경로 찾기를 합니다.")
        print(" 3. 화면이 바뀌면 해당 화면의 url을 복사합니다.")
        print(" \n 완료 시 아무키나 입력해주세요.")
        input(" > ")
        if k == 'q':
            return
        print("\n 이용할 준비가 끝났습니다.\n 바로 이용메뉴로 넘어갑니다.\n")

    def get_Oil_Information(self):
        print("┌───────────────────────────────────────┐")
        print("│ 현재 유가를 가져올 유종을 선택하세요. │")
        print("└───────────────────────────────────────┘")
        print(" 1. 휘발유")
        print(" 2. 경유")
        print(" 3. 직접 입력")
        choice = input(" > ")
        if (choice == '3'):
            print(" ")
            print(" 주유할 주유소의 유가를 입력해주세요.")
            oil_Cost = input(" > ")
            self.oil_Cost = float(oil_Cost)
            print(" 입력된 유가입니다 :", str(self.oil_Cost) + '원')
        else:
            if (choice == '1'):
                oil = self.oil_GSL
            else:
                oil = self.oil_LO
            html = urllib.request.urlopen(oil, context=self.context).read()
            soup = BeautifulSoup(html, 'html.parser')
            oil_Cost = soup.find_all('em', class_='no_up')
            oil_Cost_ = oil_Cost[0].get_text()[1] + oil_Cost[0].get_text()[3:9]
            self.oil_Cost = float(oil_Cost_)
            print(" 조회된 유가입니다 : " + str(self.oil_Cost) + '원')

    def input_Fuel_Efficiency(self):
        print("┌────────────────────────────────────┐")
        print("│ 차량의 도로별 연비를 입력해주세요. │")
        print("└────────────────────────────────────┘")
        print(" 일반도로")
        self.general_Road_Fuel_Efficiency = float(input(" > "))
        print(" 고속도로")
        self.highway_Fuel_Efficiency = float(input(" > "))

    def get_Road_Fare(self):
        html = urllib.request.urlopen(self.url, context=self.context).read()
        soup = BeautifulSoup(html, 'html.parser')
        extracted_Data = soup.find_all('span', class_='txt_fare')
        _road_Fare = extracted_Data[1].get_text()
        road_Fare = re.findall('\d', _road_Fare)
        for ele in road_Fare:
            self.road_Fare += ele
        return self.road_Fare

    def run(self):
        try:
            print("┌────────────────────────────┐")
            print("│ 복사한 url을 입력해주세요. │")
            print("└────────────────────────────┘")
            self.url = input(" > ")
            print("\n > Now calculating...\n")
            html = urllib.request.urlopen(self.url, context=self.context).read()
            soup = BeautifulSoup(html,'html.parser')
            roads = soup.find_all('span', class_='txt_section')
            for tag in roads:
                road = tag.get_text()
                if (self.highway in road):
                    extracted_Value = road.find('km') - 2
                    if (extracted_Value == -3):
                        extracted_Value = road.find('m') - 1
                    for cnt in range(extracted_Value, 0, -1):
                        try:
                            if (road[cnt] == '.'):
                                pass
                            else:
                                int(road[cnt])
                        except:
                            if (len(road[cnt + 1:extracted_Value + 2]) != 0):
                                if ('.' in road[cnt + 1:extracted_Value + 2]):
                                    self.highways.append(str(int(float(road[cnt + 1:extracted_Value + 2]) * 1000)))
                                elif ('m' in road[cnt + 1:extracted_Value + 2]):
                                    self.highways.append(road[cnt + 1:extracted_Value + 1])
                                else:
                                    self.highways.append(str(int(float(road[cnt + 1:extracted_Value + 2]) * 1000)))
                            break
                else:
                    extracted_Value = road.find('km') - 2
                    if (extracted_Value == -3):
                        extracted_Value = road.find('m') - 1
                    for cnt in range(extracted_Value, 0, -1):
                        try:
                            if (road[cnt] == '.'):
                                pass
                            else:
                                int(road[cnt])
                        except:
                            if (len(road[cnt+1:extracted_Value+2]) != 0):
                                if ('.' in road[cnt+1:extracted_Value+2]):
                                    self.general_Road.append(str(int(float(road[cnt+1:extracted_Value+2]) * 1000)))
                                elif ('m' in road[cnt+1:extracted_Value+2]):
                                    self.general_Road.append(road[cnt + 1:extracted_Value + 1])
                                else:
                                    self.general_Road.append(str(int(float(road[cnt + 1:extracted_Value + 2]) * 1000)))
                            break

            highways = 0
            general_Roads = 0
            for ele in self.highways:
                highways += int(ele)
            for ele in self.general_Road:
                general_Roads += int(ele)
            self.road_Fare = self.get_Road_Fare()
            print(" 산출된 예상 이동거리입니다.")
            str_Highways = list(str(highways))
            str_General_Roads = list(str(general_Roads))
            hlength = len(str_Highways)
            glength = len(str_General_Roads)
            if (hlength == 6):
                str_Highways.insert(3, ',')
            elif (hlength == 5):
                str_Highways.insert(2, ',')
            elif (hlength == 4):
                str_Highways.insert(1, ',')
            highways_ = ''
            for ele in str_Highways:
                highways_ += ele

            if (glength == 6):
                str_General_Roads.insert(3, ',')
            elif (glength == 5):
                str_General_Roads.insert(2, ',')
            elif (glength == 4):
                str_General_Roads.insert(1, ',')
            general_Roads_ = ''
            for ele in str_General_Roads:
                general_Roads_ += ele

            road_Fare = list(self.road_Fare)
            rflength = len(self.road_Fare)
            if (rflength == 6):
                road_Fare.insert(3, ',')
            elif (rflength == 5):
                road_Fare.insert(2, ',')
            elif (rflength == 4):
                road_Fare.insert(1, ',')
            road_Fare_ = ''
            for ele in road_Fare:
                road_Fare_ += ele

            print(" > 고속도로 :", highways_ + 'm', "(고속도로 이용료 :", road_Fare_ + '원)')
            print(" > 일반도로 :", general_Roads_ + 'm')

            result1 = ((highways / self.highway_Fuel_Efficiency) * self.oil_Cost) / 1000
            result2 = ((general_Roads / self.general_Road_Fuel_Efficiency) * self.oil_Cost) / 1000
            self.result = round(result1 + result2, 0)

            scost = list(str(int(self.result) + int(self.road_Fare)))
            rcost = list(str((int(self.result) + int(self.road_Fare)) * 2))
            slength = len(scost)
            rlength = len(rcost)
            if (slength == 6):
                scost.insert(3, ',')
            elif (slength == 5):
                scost.insert(2, ',')
            elif (slength == 4):
                scost.insert(1, ',')
            scost_ = ''
            for ele in scost:
                scost_ += ele

            if (rlength == 6):
                rcost.insert(3, ',')
            elif (rlength == 5):
                rcost.insert(2, ',')
            elif (rlength == 4):
                rcost.insert(1, ',')
            rcost_ = ''
            for ele in rcost:
                rcost_ += ele
            print(" \n 산출된 예상 교통비입니다.")
            print(" > 편도 :", scost_ + '원')
            print(" > 왕복 :", rcost_ + '원')
            print("\n 종료하려면 아무키나 누르세요.")
            end = input(" > ")

        except:
            print("잘못된 데이터가 입력되었습니다.")
            self.run()

def main():
    tcc = transportation_Cost_Calculation()
    print("┌─────────────────────────────────────────┐")
    print("│ Deerworld의 교통비 산출 프로그램입니다. │")
    print("└─────────────────────────────────────────┘")
    print(" 이용을 원하는 메뉴번호를 입력해주세요.")
    print(" 1. 설명보기")
    print(" 2. 바로이용")
    choice = input(" > ")
    if (choice == '1'):
        tcc.help()
    else:
        pass
    tcc.get_Oil_Information()
    tcc.input_Fuel_Efficiency()
    tcc.run()

if __name__ == '__main__':
    main()