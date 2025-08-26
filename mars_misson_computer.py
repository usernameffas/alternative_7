import time   # 주기적 대기(sleep)을 위해 사용
import json   # JSON 형식 출력
import random # 무작위 데이터 생성

class DummySensor:
    """
    DummySensor 클래스
    - 무작위 환경 데이터를 생성하여 반환하는 센서 시뮬레이터
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
    - DummySensor 데이터를 주기적으로 가져와 출력한다.
    - 5초마다 현재값 출력
    - 5분마다(=60회) 평균값 출력
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

        # --- 보너스 과제용 데이터 저장소 ---
        # 최근 60번(=5분) 동안의 데이터를 저장해 평균 계산
        self.acc_data = { key: [] for key in self.env_values.keys() }

    def get_sensor_data(self):
        """
        센서 데이터를 무한 루프로 반복 출력
        - 5초마다 현재 값 출력
        - 5분마다 평균값 출력
        - CTRL+C 시 종료
        """
        try:
            count = 0  # 몇 번(=몇 초 주기) 실행했는지 카운트
            while True:
                # 센서 데이터 갱신
                self.ds.set_env()
                sensor_data = self.ds.get_env()

                # MissionComputer의 env_values 갱신
                for key in self.env_values.keys():
                    self.env_values[key] = sensor_data[key]
                    # 보너스 평균 계산용으로 값 저장
                    self.acc_data[key].append(sensor_data[key])

                # 현재값 출력
                print(json.dumps(self.env_values, indent=4, ensure_ascii=False))

                # 카운트 증가
                count += 1

                # 60번(=5분)마다 평균값 출력
                if count % 60 == 0:
                    avg_result = {
                        k: round(sum(v)/len(v), 2) for k, v in self.acc_data.items()
                    }
                    print('[5분 평균값]')
                    print(json.dumps(avg_result, indent=4, ensure_ascii=False))
                    # 다 출력했으면 리스트 비워서 새로운 5분 간격 측정 준비
                    self.acc_data = { key: [] for key in self.env_values.keys() }

                # 5초 대기
                time.sleep(5)
        except KeyboardInterrupt:
            print('System stoped....')

if __name__ == '__main__':
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()
