# game.py
"""
[game.py] 게임 진행(턴) 담당

- 게임의 규칙을 정의한다.
  (현재 상태 저장 + 한 턴 진행 + 게임 끝날 때까지 반복)
- 방을 뽑는 방식은 balance.py에 맡기고,
  추격/랜덤 이벤트는 events.py에 맡기고,
  출력/입력 같은 잡일은 utils.py에 맡긴다.
- 이유: 게임 규칙을 한 곳에서 조립/관리하려고.
예시:
- '위험도 10이면 즉시 게임오버'를 '위험도 15'로 바꾸고 싶다
  → DraftGame(risk_limit=15)만 바꾸면 됨

"""


from utils import say, say_block, read_int
from balance import weighted_room_options, DEFAULT_CATEGORY_WEIGHTS
from events import EventSystem

class DraftGame:
    def __init__(self, room_deck, start_steps=10, risk_limit=10, category_weights=None):
        self.room_deck = room_deck
        self.steps = start_steps
        self.risk = 0
        self.depth = 0
        self.current_room = "입구"
        self.risk_limit = risk_limit

        self.category_weights = category_weights or DEFAULT_CATEGORY_WEIGHTS
        self.events = EventSystem()

    def print_status(self):
        say("\n----------------------------------------")
        say(f"현재 층: {self.depth}")
        say(f"현재 방: {self.current_room}")
        say(f"남은 스텝: {self.steps}")
        say(f"위험도: {self.risk}")
        say(f"추격 상태: {'ON' if self.events.is_chasing() else 'OFF'}")
        say("----------------------------------------")

    def print_options(self, options):
        for i, r in enumerate(options, start=1):
            print(f"{i}) {r['name']} [{r['category']}]  스텝 {r['step_delta']:+d} / 위험 {r['risk_delta']:+d}")
        print("0) 여기서 그만두기")

    def apply_room_base_effects(self, room):
        self.steps += room["step_delta"]
        self.risk  += room["risk_delta"]

        cat = room["category"]
        if cat == "System":
            say("  └ 시스템 사용: 스텝 +1")
            self.steps += 1
        elif cat == "Normal":
            say("  └ 휴식: 위험도 -1 (최소 0)")
            self.risk = max(0, self.risk - 1)

    def step_once(self):
        self.depth += 1
        self.print_status()

        options = weighted_room_options(self.room_deck, k=3, category_weights=self.category_weights)
        say("다음 방 선택지:")
        self.print_options(options)

        choice = read_int("어느 방으로 갈까? (0-3): ", 0, 3)
        if choice == 0:
            return False

        selected = options[choice - 1]
        say(f"\n>> {selected['name']} 방을 선택했다!")

        # 1) 기본(방 카드 자체) 효과
        self.apply_room_base_effects(selected)
        self.current_room = selected["name"]

        # 2) 이벤트 시스템(크리처/추격/랜덤)
        self.steps, self.risk, msgs = self.events.on_enter_room(selected, self.steps, self.risk)
        if msgs:
            say_block([f"  [EVENT] {m}" for m in msgs])

        # 종료 조건
        if self.risk >= self.risk_limit:
            say("\n위험도가 한계를 넘어섰다. 더 이상 버틸 수 없다…")
            return False
        if self.steps <= 0:
            return False

        return True

    def run(self):
        say("=== 텍스트 드래프트 프로토타입 ===")
        say("가중치 드래프트 + 추격 이벤트가 포함된 버전입니다.\n")

        while self.steps > 0:
            if not self.step_once():
                break

        say("\n=== 게임 종료 ===")
        say(f"도달한 층: {self.depth}")
        say(f"최종 위험도: {self.risk}")
        say(f"남은 스텝: {self.steps}")
