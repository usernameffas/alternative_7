# ----------------------------- 모듈 임포트 -----------------------------

import time   # time 모듈: 프로그램을 일정 시간 동안 멈추는 기능(sleep)을 제공 -> 5초 간격 실행에 활용됨
import json   # json 모듈: Python dict 데이터를 JSON 문자열로 변환하여 사람이 읽기 좋은 출력 포맷 제공
import random # random 모듈: 난수(무작위 수)를 생성하는 기능 제공 -> 센서 데이터 시뮬레이션에 사용


# ----------------------------- DummySensor 클래스 -----------------------------

class DummySensor:
    """
    DummySensor 클래스
    -----------------
    - 실제 센서 대신 무작위 값을 생성하여 화성 기지의 환경 데이터를 모의실험(simulation)하기 위한 클래스.
    - MissionComputer 클래스는 이 DummySensor로부터 데이터를 읽어서 기지 환경 상태를 확인한다고 가정한다.
    """

    def __init__(self):
        """
        초기화 메소드(__init__):
        - 센서로부터 수집한 데이터를 저장할 딕셔너리(env_values)를 생성.
        - 처음에는 전부 0.0으로 초기화, 즉 "아직 측정되지 않은 값" 상태를 표현한다.
        - 각 키(key)는 측정 항목 이름을 의미한다.
        """
        self.env_values = {
            'mars_base_internal_temperature': 0.0,   # 내부 온도 (단위: °C)
            'mars_base_external_temperature': 0.0,   # 외부 온도 (단위: °C)
            'mars_base_internal_humidity': 0.0,      # 내부 습도 (단위: %)
            'mars_base_external_illuminance': 0.0,   # 외부 조도, 즉 밝기 (단위: lux)
            'mars_base_internal_co2': 0.0,           # 내부 공기 중 이산화탄소 농도 (단위: %)
            'mars_base_internal_oxygen': 0.0         # 내부 공기 중 산소 농도 (단위: %)
        }

    def set_env(self):
        """
        set_env 메소드:
        - 각 센서 값 키에 해당하는 값들을 무작위로 갱신한다.
        - random.uniform(a, b): a와 b 사이의 난수를 생성 (부동소수점 실수 값).
        - round(value, n): 생성된 값을 소수점 n자리에서 반올림 -> 더 깔끔한 숫자를 출력하기 위함.
        - 이렇게 생성된 값은 현실적인 환경 수치를 "가정하여" 설정한 것이다.
        """
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18.0, 30.0), 2) # 내부 온도 범위 18~30°C
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0.0, 21.0), 2)  # 외부 온도 범위 0~21°C
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50.0, 60.0), 2)    # 내부 습도 범위 50~60%
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500.0, 715.0), 2) # 외부 조도 범위 500~715 lux
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)          # 내부 이산화탄소 농도 범위 0.02~0.1%
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4.0, 7.0), 2)        # 내부 산소 농도 범위 4~7%

    def get_env(self):
        """
        get_env 메소드:
        - 현재 env_values 딕셔너리에 들어 있는 값을 반환한다.
        - MissionComputer 클래스에서 이 값을 읽어와 env_values를 업데이트하고 출력한다.
        """
        return self.env_values


# ----------------------------- MissionComputer 클래스 -----------------------------

class MissionComputer:
    """
    MissionComputer 클래스
    ----------------------
    - 화성 기지의 미션 컴퓨터 역할을 시뮬레이션하는 클래스.
    - DummySensor 인스턴스를 활용하여 주기적으로 데이터를 받아오고 관리한다.
    - 제공하는 주요 기능:
        1. 센서 데이터를 5초마다 출력 -> 실시간 환경 모니터링 기능.
        2. 센서 데이터를 누적하여 5분마다 평균값 출력 -> 장기적인 환경 변화 추이를 확인 가능.
        3. CTRL+C 입력 시 KeyboardInterrupt 예외를 처리하여 안전하게 종료할 수 있음.
    """

    def __init__(self):
        """
        __init__ 메소드 (생성자):
        - env_values: 현재 환경 데이터를 저장할 딕셔너리. 초깃값은 None (아직 읽지 않았음을 의미).
        - ds: DummySensor 인스턴스를 생성하여 연결.
        - acc_data: 보너스 과제 수행용 -> 최근 60번(=5분 동안) 측정된 데이터를 누적 저장할 딕셔너리.
        """
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None,
        }
        self.ds = DummySensor() # DummySensor와 연결

        # acc_data 딕셔너리는 각 항목별로 리스트를 만들어서 값을 담는다.
        # 예: acc_data['mars_base_internal_temperature'] = [23.1, 22.5, ...]
        self.acc_data = { key: [] for key in self.env_values.keys() }

    def get_sensor_data(self):
        """
        get_sensor_data 메소드:
        - 무한 루프를 실행하면서 주기적으로 데이터를 가져오고 출력한다.
        - 작동 절차:
            (1) DummySensor에서 set_env()를 실행시켜 새로운 데이터 생성.
            (2) get_env()를 호출해서 Dict 데이터를 가져온다.
            (3) 그 Dict를 env_values와 acc_data에 저장한다.
            (4) 즉시 현재값을 JSON 형식으로 출력한다.
            (5) 60번 = 5분이 지나면 acc_data 리스트들의 평균값을 계산하여 출력한다.
            (6) 출력 후에는 acc_data를 초기화하여 새로운 5분 평균 계산을 준비한다.
            (7) time.sleep(5)으로 정확히 5초 대기 -> 5초 주기 유지.
            (8) CTRL+C 발생 시 KeyboardInterrupt 예외로 감지하여 종료 메시지를 출력하고 루프 중단.
        """
        try:
            count = 0  # "지금까지 몇 번째 데이터 출력인지"를 세는 카운터. 60번에 도달하면 평균 출력.
            while True:
                # (1) 센서 무작위 값 갱신
                self.ds.set_env()

                # (2) 센서 데이터 읽기
                sensor_data = self.ds.get_env()

                # (3) MissionComputer의 env_values 업데이트 & acc_data에 누적
                for key in self.env_values.keys():
                    self.env_values[key] = sensor_data[key]
                    self.acc_data[key].append(sensor_data[key])

                # (4) 현재 값 바로 출력 (JSON 형식)
                # indent=4 → 보기 좋게 들여쓰기
                # ensure_ascii=False → 한글(예: "5분 평균값")이 깨지지 않고 출력됨
                print(json.dumps(self.env_values, indent=4, ensure_ascii=False))

                # (5) 카운트 증가
                count += 1

                # (6) 60번째 마다 평균값 계산 후 출력 (즉, 5분마다 평균 출력)
                if count % 60 == 0:
                    # 각 항목의 평균값을 새 dict로 생성
                    avg_result = {
                        k: round(sum(v)/len(v), 2) for k, v in self.acc_data.items()
                    }
                    print('[5분 평균값]')
                    print(json.dumps(avg_result, indent=4, ensure_ascii=False))

                    # (7) 평균을 출력했으면 acc_data 초기화 -> 새로운 5분 준비
                    self.acc_data = { key: [] for key in self.env_values.keys() }

                # (8) 5초 동안 대기 (주기 제어)
                time.sleep(5)

        except KeyboardInterrupt:
            # 사용자 입력 CTRL+C 신호가 들어오면 KeyboardInterrupt 발생
            # 이때 except 블록으로 진입 -> "System stoped...." 출력 후 프로그램 안전 종료
            print('System stoped....')


# ----------------------------- 실행부 -----------------------------

if __name__ == '__main__':
    """
    실행부:
    - Python 인터프리터에서 직접 실행할 때만 동작하는 코드.
    - MissionComputer 인스턴스를 생성하고,
      get_sensor_data() 메소드를 실행하여 무한 루프 데이터 출력을 시작한다.
    """
    RunComputer = MissionComputer()  # MissionComputer 객체 생성
    RunComputer.get_sensor_data()    # 5초마다 데이터 출력 + 5분 평균 출력 기능 수행 시작
      
