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
        self.disc_highway = 0
        self.oil_GSL = 'https://finance.naver.com/marketindex/oilDetail.nhn?marketindexCd=OIL_GSL' # 휘발유
        self.oil_LO = 'https://finance.naver.com/marketindex/oilDetail.nhn?marketindexCd=OIL_LO' # 경유

    def get_Oil_Information(self, choice):
        if (choice == '1'):
            oil = self.oil_GSL
        elif (choice == '2'):
            oil = self.oil_LO
        else:
            pass
        html = urllib.request.urlopen(oil, context=self.context).read()
        soup = BeautifulSoup(html, 'html.parser')
        oil_Cost = soup.find_all('em', class_='no_up')
        oil_Cost_ = oil_Cost[0].get_text()[1] + oil_Cost[0].get_text()[3:9]
        self.oil_Cost = float(oil_Cost_)
        return self.oil_Cost

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
        req = urllib.request.Request(self.url, headers = {'User-Agent' : 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, context=self.context).read()
        soup = BeautifulSoup(html,'html.parser')
        roads = soup.find_all('span', class_='txt_section')
        for tag in roads:
            road = tag.get_text()
            if (self.highway in road):
                self.disc_highway += 1
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

        str_ = []
        print("self.disc_highway : ", self.disc_highway)
        if (self.disc_highway != 0):
            self.road_Fare = self.get_Road_Fare()

        highways = 0
        for ele in self.highways:
            highways += int(ele)
        str_Highways = list(str(highways))
        hlength = len(str_Highways)
        if (hlength == 6):
            str_Highways.insert(3, ',')
        elif (hlength == 5):
            str_Highways.insert(2, ',')
        elif (hlength == 4):
            str_Highways.insert(1, ',')
        highways_ = ''
        for ele in str_Highways:
            highways_ += ele

        general_Roads = 0
        for ele in self.general_Road:
            general_Roads += int(ele)
        str_General_Roads = list(str(general_Roads))
        glength = len(str_General_Roads)
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

        if (self.disc_highway == 0):
            highways_ = '0'
            road_Fare_ = '0'
        m1 = " 산출된 예상 이동거리입니다."
        hw = " 고속도로 : " + highways_ + "m" + " (고속도로 이용료 : " + road_Fare_ + "원)"
        gr = " 일반도로 : " + general_Roads_ + "m"
        str_.append(m1)
        str_.append(hw)
        str_.append(gr)

        if (self.disc_highway != 0):
            result1 = ((highways / self.highway_Fuel_Efficiency) * self.oil_Cost) / 1000
            result2 = ((general_Roads / self.general_Road_Fuel_Efficiency) * self.oil_Cost) / 1000
            self.result = round(result1 + result2, 0)
        else:
            result2 = ((general_Roads / self.general_Road_Fuel_Efficiency) * self.oil_Cost) / 1000
            self.result = round(result2, 0)

        if (self.disc_highway == 0):
            scost = list(str(int(self.result)))
            rcost = list(str(int(self.result) * 2))
        else:
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
        m2 = " \n 산출된 예상 교통비입니다."
        ow = " 편도 : " + scost_ + "원"
        tw = " 왕복 : " + rcost_ + "원"
        str_.append(m2)
        str_.append(ow)
        str_.append(tw)

        return str_