import time   # 시간 지연(sleep)을 위해 사용
import json   # JSON 형식 출력 지원
import random # 무작위 데이터 생성

class DummySensor:
    """
    DummySensor 클래스
    - 임의의 센서 데이터를 생성해서 반환하는 시뮬레이션용 클래스
    """
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
    def set_env(self):
        """ 센서값 무작위 갱신 """
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18.0, 30.0), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0.0, 21.0), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50.0, 60.0), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500.0, 715.0), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4.0, 7.0), 2)
    def get_env(self):
        return self.env_values

class MissionComputer:
    """
    MissionComputer 클래스
    - DummySensor 데이터를 주기적으로 가져와 출력하는 역할
    """
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None,
        }
        self.ds = DummySensor()
    def get_sensor_data(self):
        """ 센서값을 5초마다 출력, CTRL+C 입력 시 종료 """
        try:
            while True:
                # 센서 갱신
                self.ds.set_env()
                # 센서 측정 데이터 가져오기
                sensor_data = self.ds.get_env()
                # MissionComputer의 값으로 복사
                for key in self.env_values.keys():
                    self.env_values[key] = sensor_data[key]
                # JSON 형식으로 예쁘게 출력
                print(json.dumps(self.env_values, indent=4, ensure_ascii=False))
                # 5초간 대기
                time.sleep(5)
        except KeyboardInterrupt:
            print('System stoped....')

if __name__ == '__main__':
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()
