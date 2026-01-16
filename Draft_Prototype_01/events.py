"""
[events.py] 랜덤 이벤트 / 추격(크리처) 담당

- 방에 들어갈 때 일어나는 일(추격 시작, 추격 중 패널티, 이상현상 추가 피해 등)을 여기서 처리한다.
- game.py는 "이벤트 시스템을 호출하고 결과만 적용"한다.
- 이유:
  - 추격/이벤트는 규칙이 커지고 자주 바뀌는 부분이라,
    메인 게임 루프(game.py)와 분리해 유지보수하기 쉽게 하려고.
"""


# events.py
import random

class EventSystem:
    """
    아주 간단한 상태:
    - chase_meter: 0 이상이면 '추격 중'으로 간주
    - risk가 높을수록 추격 시작 확률이 증가
    """

    def __init__(self):
        self.chase_meter = 0   # 0이면 비추격, 1+이면 추격 중
        self.last_event = None

    def is_chasing(self):
        return self.chase_meter > 0

    def _chance_start_chase(self, risk):
        # risk 0이면 0%, risk 10이면 대략 40% 정도(원하면 조절)
        return min(0.40, 0.04 * max(0, risk))

    def _chance_end_chase(self):
        # 추격 중 자연 종료 확률
        return 0.20

    def on_enter_room(self, room, steps, risk):
        """
        방에 들어갈 때마다 호출.
        returns: (steps, risk, messages:list[str])
        """
        msgs = []

        # 1) 카테고리 기반 즉시 이벤트(가벼운 양념)
        cat = room["category"]
        if cat == "Ritual":
            msgs.append("이 방의 공기가 탁하다. 무언가 깨어나는 느낌이다. 위험도 +1")
            risk += 1
        elif cat == "Anomaly":
            # 이상현상은 가끔 추가 패널티
            if random.random() < 0.30:
                msgs.append("이상현상이 시야를 찢는다. 스텝 -1")
                steps -= 1
        elif cat == "System":
            # 시스템 방은 가끔 '경보'로 추격 트리거
            if random.random() < 0.15:
                msgs.append("기계음이 울린다. 경보가 울린 듯하다… (추격 게이지 +1)")
                self.chase_meter += 1

        # 2) 추격 시작 체크
        if not self.is_chasing():
            if random.random() < self._chance_start_chase(risk):
                self.chase_meter = max(self.chase_meter, 2)
                msgs.append("뒤에서 발소리가 빨라진다. 추격이 시작됐다!")

        # 3) 추격 중 처리(입장 시점)
        if self.is_chasing():
            # 추격 중이면 기본 압박: 스텝 추가 소모
            msgs.append("추격 중이다. 숨이 턱 막힌다. 스텝 -1")
            steps -= 1

            # 탈출/지속 판정
            if random.random() < self._chance_end_chase():
                self.chase_meter = 0
                msgs.append("숨을 곳을 찾았다. 추격이 끊겼다.")
            else:
                self.chase_meter += 1

        # 4) 사망(게임오버)성 이벤트는 프로토타입에선 risk/steps로만 처리
        return steps, risk, msgs
