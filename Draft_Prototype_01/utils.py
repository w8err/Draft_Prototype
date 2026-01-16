"""
[utils.py] 공용 도구 모음(입력/출력/편의 기능)

- 여러 파일에서 계속 쓰는 기능을 모아둔다.
  예: 숫자 입력 안전하게 받기, 한 줄씩 천천히 출력(slow_print) 등.
- 이유:
  - 같은 코드를 여기저기 복붙하면 나중에 고칠 때 힘드니까
    공용 기능은 한 곳에서 관리하려고.
"""

# utils.py
import time
import random

TEXT_DELAY = 1  # 여기 숫자만 바꾸면 전체 속도 조절 가능 [web:428]

def draw_options(deck, count=3):
    return random.sample(deck, k=count)

def read_int(prompt, lo, hi):
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if lo <= val <= hi:
                return val
        except ValueError:
            pass
        print(f"{lo}~{hi} 숫자를 입력하세요.")

def say(line, delay=TEXT_DELAY):
    print(line, flush=True)
    time.sleep(delay)

def say_block(lines, delay=TEXT_DELAY):
    for line in lines:
        print(line, flush=True)
        time.sleep(delay)

