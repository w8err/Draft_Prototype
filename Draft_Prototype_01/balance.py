"""
[balance.py] 방 후보를 뽑는 규칙(확률) 담당

- 매 턴 3개 방 후보를 보여주는데, 어떤 카테고리가 더 자주 뜰지(가중치)를 여기서 정한다.
  예: Corridor 35%, Normal 30% ... 같은 룰.
- 이유:
  - 게임이 '재밌는 빈도'로 방이 나오게 만드는 핵심이 확률이라서,
    그 부분을 한 파일로 분리해 빨리 튜닝하려고.
"""

# balance.py
import random

DEFAULT_CATEGORY_WEIGHTS = {
    "Corridor": 35,
    "Normal":   30,
    "System":   20,
    "Anomaly":  10,
    "Ritual":    5,
}

def weighted_room_options(room_deck, k=3, category_weights=None):
    """
    room_deck에서 k개 방을 '중복 없이' 뽑되,
    카테고리 가중치에 의해 해당 카테고리의 방이 더 잘 나오게 한다.

    구현 방식:
    - 각 방에 "그 방의 카테고리 가중치"를 방 가중치로 부여
    - random.choices로 1개씩 뽑고, 이미 뽑은 건 제외(무작위 '비복원' 샘플링)
    """
    if category_weights is None:
        category_weights = DEFAULT_CATEGORY_WEIGHTS

    pool = list(room_deck)
    chosen = []

    for _ in range(min(k, len(pool))):
        weights = [max(0, category_weights.get(r["category"], 0)) for r in pool]
        # 가중치가 전부 0이면 균등 랜덤
        if sum(weights) == 0:
            pick = random.choice(pool)
        else:
            pick = random.choices(pool, weights=weights, k=1)[0]  # 표준 라이브러리 [web:422]
        chosen.append(pick)
        pool.remove(pick)

    return chosen
