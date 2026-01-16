# main.py
"""

- 이 파일은 "게임을 실행하는 버튼" 역할만 한다.
- 여기에는 규칙/이벤트/밸런스 로직을 넣지 않는다.
- 이유: 나중에 실행 옵션(시드, 디버그 모드 등)을 바꿀 때
  다른 파일 건드리지 않고 여기만 수정하려고.

예시:
- 시작 스텝을 20으로 바꾸고 싶다 → main.py에서 DraftGame(start_steps=20)만 수정
- 나중에 'seed=1234' 같은 실행 옵션을 붙일 때도 main.py만 건드리면 됨

"""

from rooms import ROOM_DECK
from game import DraftGame

def main():
    game = DraftGame(ROOM_DECK, start_steps=50, risk_limit=25)
    game.run()

if __name__ == "__main__":
    main()
