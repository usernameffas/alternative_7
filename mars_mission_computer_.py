# ----------------------------- 모듈 임포트 -----------------------------

import time   # 시간 관련 기능 제공 (특히 sleep() 사용하여 주기적 반복을 구현할 때 필요)
import json   # 환경 데이터를 JSON 형식으로 예쁘게 출력하기 위해 사용
import random # 무작위 숫자를 생성해서 센서 값을 흉내내는 데 사용


# ----------------------------- DummySensor 클래스 -----------------------------

class DummySensor:
    """
    DummySensor 클래스
    -----------------
    목적:
        화성 기지 환경 데이터를 실제 센서 없이 무작위(random) 값으로 생성하여,
        마치 센서로 측정한 것처럼 시뮬레이션하는 역할을 한다.
    
    기능:
        - 센서 값 저장용 딕셔너리(env_values)를 초기화한다.
        - set_env 메서드를 통해 각 항목에 무작위 값을 채운다.
        - get_env 메서드는 현재 센서 값 딕셔너리를 반환한다.
    """

    def __init__(self):
        """
        초기화 메서드:
            env_values라는 사전(dict)을 생성하여 센서 값들을 저장하는 공간을 만들고,
            모든 값을 0.0으로 초기화한다.
        """
        self.env_values = {
            'mars_base_internal_temperature': 0.0,   # 화성 기지 내부 온도 (°C)
            'mars_base_external_temperature': 0.0,   # 화성 기지 외부 온도 (°C)
            'mars_base_internal_humidity': 0.0,      # 화성 기지 내부 습도 (%)
            'mars_base_external_illuminance': 0.0,   # 화성 기지 외부 광량 (lux)
            'mars_base_internal_co2': 0.0,           # 화성 기지 내부 이산화탄소 농도 (%)
            'mars_base_internal_oxygen': 0.0         # 화성 기지 내부 산소 농도 (%)
        }

    def set_env(self):
        """
        센서 데이터를 무작위 값으로 갱신하는 메서드.
        각 항목은 현실적인 범위 안에서 무작위 수를 생성한다.
        """
        # 내부 온도: 18~30°C
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18.0, 30.0), 2)

        # 외부 온도: 0~21°C
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0.0, 21.0), 2)

        # 내부 습도: 50~60%
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50.0, 60.0), 2)

        # 외부 조도: 500~715 lux
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500.0, 715.0), 2)

        # 내부 이산화탄소 농도: 0.02~0.1%
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)

        # 내부 산소 농도: 4~7%
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4.0, 7.0), 2)

    def get_env(self):
        """
        최신 환경 데이터를 담은 env_values 딕셔너리를 반환한다.
        """
        return self.env_values


# ----------------------------- MissionComputer 클래스 -----------------------------

class MissionComputer:
    """
    MissionComputer 클래스
    ----------------------
    목적:
        실제 화성 기지의 '미션 컴퓨터'와 같은 역할을 한다고 가정.
        더미 센서(DummySensor)로부터 데이터를 읽어와 주기적으로(5초마다) 출력한다.
    
    기능:
        - env_values라는 속성을 가지고 센서 데이터 저장.
        - DummySensor 인스턴스(ds)를 이용해 센서 데이터 받아오기.
        - get_sensor_data 메서드에서:
            1. 센서를 통해 새로운 데이터 생성
            2. env_values에 갱신
            3. JSON 형태로 화면에 예쁘게 출력
            4. 5초마다 반복 (무한 루프)
            5. 사용자가 CTRL+C 입력 시 종료
    """

    def __init__(self):
        """
        초기화 메서드:
            - env_values: 센서 데이터 저장용 딕셔너리, 시작 시 None 값으로 초기화.
            - ds: DummySensor 클래스 인스턴스를 생성하여 연결.
        """
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None,
        }
        # 더미 센서를 하나 사용 (ds 이름으로 인스턴스화)
        self.ds = DummySensor()

    def get_sensor_data(self):
        """
        센서 데이터 가져오기 메서드:
            - 무한 루프를 돌면서 데이터를 수집하고 출력한다.
            - 동작 순서:
                (1) 센서 값 갱신 (set_env 호출)
                (2) 센서로부터 현재 값 가져오기 (get_env 호출)
                (3) MissionComputer의 env_values에 저장
                (4) JSON 형식으로 화면에 출력
                (5) 5초 동안 대기 (time.sleep(5))
            - CTRL+C (KeyboardInterrupt)가 발생하면 루프를 빠져나와 종료 메시지를 출력한다.
        """
        try:
            while True:
                # (1) 센서 데이터 갱신
                self.ds.set_env()

                # (2) 센서 데이터를 가져오기
                sensor_data = self.ds.get_env()

                # (3) MissionComputer의 env_values에 복사
                for key in self.env_values.keys():
                    self.env_values[key] = sensor_data[key]

                # (4) JSON으로 출력 (ensure_ascii=False → 한글도 깨지지 않음)
                print(json.dumps(self.env_values, indent=4, ensure_ascii=False))

                # (5) 5초 동안 대기
                time.sleep(5)
        except KeyboardInterrupt:
            # CTRL+C 입력 시 여기로 와서 종료
            print('System stoped....')


# ----------------------------- 실행부분 -----------------------------

# Python에서 직접 실행될 경우(__name__ == '__main__')만 아래 코드 실행
if __name__ == '__main__':
    # MissionComputer 클래스 인스턴스를 RunComputer라는 이름으로 생성
    RunComputer = MissionComputer()

    # 환경 데이터 5초마다 출력하도록 메서드 호출
    RunComputer.get_sensor_data()
