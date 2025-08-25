import time
import json
import random

class DummySensor:
    """
    더미 센서 클래스: 화성 기지 환경 값을 무작위로 생성합니다.
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
    미션 컴퓨터 클래스: DummySensor로부터 데이터를 받아 5초마다 출력합니다.
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
        try:
            while True:
                self.ds.set_env()  # 센서 데이터 갱신
                sensor_data = self.ds.get_env()

                for key in self.env_values.keys():
                    self.env_values[key] = sensor_data[key]

                print(json.dumps(self.env_values, indent=4, ensure_ascii=False))
                time.sleep(5)

        except KeyboardInterrupt:
            print('System stoped....')


if __name__ == '__main__':
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()
