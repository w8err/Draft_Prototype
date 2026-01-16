# rooms.py
"""
[rooms.py] 방 목록(데이터)만 모아둔 파일

- 여기에는 방 이름/카테고리/스텝 변화/위험도 변화 같은 "방 데이터"만 있다.
- 이유:
  1) 밸런스 조절할 때 코드를 안 보고 데이터만 고치게 하려고.
  2) 나중에 CSV/JSON로 바꿔도 게임 로직은 그대로 두려고.
"""


ROOM_DECK = [
    # Normal
    {"id": "N1", "name": "좁은 창고", "category": "Normal",   "step_delta": -1, "risk_delta": 0},
    {"id": "N2", "name": "휴게실",     "category": "Normal",   "step_delta":  0, "risk_delta": 0},

    # Corridor
    {"id": "C1", "name": "긴 복도",   "category": "Corridor", "step_delta": -1, "risk_delta": 0},
    {"id": "C2", "name": "L자 복도",  "category": "Corridor", "step_delta": -1, "risk_delta": 0},

    # Anomaly
    {"id": "A1", "name": "깜빡이는 방", "category": "Anomaly", "step_delta": -1, "risk_delta": 2},
    {"id": "A2", "name": "속삭임 방",   "category": "Anomaly", "step_delta": -2, "risk_delta": 3},

    # Ritual
    {"id": "R1", "name": "작은 제단",   "category": "Ritual",  "step_delta": -2, "risk_delta": 3},
    {"id": "R2", "name": "큰 제단",     "category": "Ritual",  "step_delta": -3, "risk_delta": 4},

    # System
    {"id": "S1", "name": "자판기 방",   "category": "System",  "step_delta": -1, "risk_delta": 0},
    {"id": "S2", "name": "장비 창구",   "category": "System",  "step_delta": -1, "risk_delta": 1},
]
