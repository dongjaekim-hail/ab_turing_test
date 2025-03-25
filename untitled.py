#visual: 시각적 자극(텍스트, 도형 등)을 표시,event: 키보드 입력 처리,data: 실험 조건을 CSV에서 가져오는 데 사용,core: 타이머와 종료 기능.
from psychopy import visual, event, data, core
import random
import csv
import os

# PsychoPy 창 생성 fullscr은 전체 화면 모드 off
win = visual.Window(size=[800, 600], fullscr=False, color='#DCDCDC')

# 시계 객체 생성 (반응 시간 측정용)
clock = core.Clock()

# 지침 텍스트 win은 위에서 정의한 표시할 창, height은 글씨 크기.
instruction1 = visual.TextStim(win, text="이 실험은 한 질문에 두 개의 답변을 보여 줍니다. 두 답변 중 하나는 사람이, 나머지 하나는 AI가 작성한 것입니다.", 
                              pos=[0, 0.4], height=0.07, color='#333333', alignText='center', font='Malgun Gothic')
instruction2 = visual.TextStim(win, text="더 사람처럼 느껴지는 답변을 '1'(A1) 또는 '2'(A2) 키로 선택해 주세요.", bold=True, 
                              pos=[0, 0.1], height=0.07, color='#333333', alignText='center', font='Malgun Gothic')
escape = visual.TextStim(win, text="실험을 시작하려면 s키를 누르고, 종료하려면 q키를 누르세요.", 
                        pos=[0, -0.1], height=0.05, color='black')

# 초기화면 지침 텍스트 출력
instruction1.draw()
instruction2.draw()
escape.draw()
# 창 갱신 (넘기기)
win.flip()
# 키 받기
event.waitKeys(keyList=['s'])

# CSV 파일에서 시행 조건 불러오기
csv_path = r"C:\Users\HyunJun\Desktop\Q&A DATA.csv"
# csv파일 불러오기
conditions = data.importConditions(csv_path)
trial_list = conditions[:]  # 리스트 복사
random.shuffle(trial_list)  # 랜덤 순서로 섞기

# Attention trial 추가 (fraud detection용 쉬운 문제)
attention_trial = {
    'question': '1+1은 무엇인가요?',
    'answer1': '2',  # 정답 (human-like)
    'answer2': '사과',  # 오답 (AI-like)
    'answer1_label': 'human',
    'answer2_label': 'AI'
}
# 랜덤 위치에 Attention trial 삽입
trial_list.insert(random.randint(0, len(trial_list)), attention_trial)

# 응답 저장 리스트와 현재 인덱스 초기화
responses = []
current_index = -1 # 현재 시행 번호 (-1로 시작)

while current_index < len(trial_list) - 1:
    current_index += 1
    if current_index >= len(trial_list):
        break
    trial = trial_list[current_index]

    # 기본 UI 요소 정의 (항상 표시)
    instruction_text = visual.TextStim(win, text="더 인간다운 답변을 골라주세요. (A1은 1키 A2는 2키)", 
                                       pos=[0.5, 0.9], height=0.05, wrapWidth=1.2, 
                                       color='#333333', alignText='center', font='Malgun Gothic')
    q_text = visual.TextStim(win, text=f"Q. {trial['question']}", 
                             pos=[-0.3, 0.7], height=0.08, wrapWidth=1.2, 
                             color='#333333', bold=True, alignText='left', font='JetBrains Mono')
    a1_text = visual.TextStim(win, text=f"A1. {trial['answer1']}", 
                              pos=[0, 0.3], height=0.05, wrapWidth=1, 
                              color='#333333', alignText='left', font='Malgun Gothic')
    a2_text = visual.TextStim(win, text=f"A2. {trial['answer2']}", 
                              pos=[0, 0.0], height=0.05, wrapWidth=1, 
                              color='#333333', alignText='left', font='Malgun Gothic')
    button1 = visual.Circle(win, radius=0.12, pos=[-0.3, -0.4], fillColor="#FF0000", 
                            lineColor='black', lineWidth=5, opacity=0.9)
    button2 = visual.Circle(win, radius=0.12, pos=[0.3, -0.4], fillColor="#FF0000", 
                            lineColor='black', lineWidth=5, opacity=0.9)
    button1_label = visual.TextStim(win, text="A1", pos=[-0.3, -0.6], height=0.05, color='black')
    button2_label = visual.TextStim(win, text="A2", pos=[0.3, -0.6], height=0.05, color='black')

    # tokens가 multiple일 때 추가 텍스트 정의
    option_texts = []
    if trial['tokens'] == 'multiple':
        options = [trial.get('a', ''), trial.get('b', ''), trial.get('c', '')]
        option_texts = [
            visual.TextStim(win, text=f"a. {options[0]}", pos=[-0.3, -0.1], height=0.05, wrapWidth=1, 
                            color='#555555', alignText='left', font='Malgun Gothic'),
            visual.TextStim(win, text=f"b. {options[1]}", pos=[-0.3, -0.2], height=0.05, wrapWidth=1, 
                            color='#555555', alignText='left', font='Malgun Gothic'),
            visual.TextStim(win, text=f"c. {options[2]}", pos=[-0.3, -0.3], height=0.05, wrapWidth=1, 
                            color='#555555', alignText='left', font='Malgun Gothic')
        ]

    # 화면 표시
    instruction_text.draw()
    q_text.draw()
    a1_text.draw()
    a2_text.draw()
    button1.draw()
    button2.draw()
    button1_label.draw()
    button2_label.draw()
    for opt_text in option_texts:  # multiple일 때만 추가 텍스트 표시
        opt_text.draw()
    win.flip()

    # 반응 시간 측정 시작
    clock.reset()
    keys = event.waitKeys(keyList=['1', '2', 'q'])
    rt = clock.getTime()

    if 'q' in keys:
        file_exists = os.path.isfile('results.csv')
        with open('results.csv', 'a', newline='') as csvfile:
            fieldnames = list(trial_list[0].keys()) + ['response', 'rt', 'is_correct']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for (trial, resp, rt_val) in responses:
                row = trial.copy()
                row['response'] = resp
                row['rt'] = rt_val
                selected_source = trial['answer1_label'] if resp == '1' else trial['answer2_label']
                row['is_correct'] = (selected_source == 'human')
                writer.writerow(row)
        win.close()
        core.quit()

    # 응답 처리
    response = '1' if '1' in keys else '2' if '2' in keys else None

    # Attention trial 체크
    if trial == attention_trial and response == '2':
        visual.TextStim(win, text="주의: 너무 부정확한 응답입니다. 실험이 종료됩니다.", 
                        height=0.07, color='red').draw()
        win.flip()
        core.wait(2)
        win.close()
        core.quit()

    # 응답과 RT 저장
    responses.append((trial, response, rt))

    # 선택 시 버튼 색 변경
    if response == '1':
        button1.fillColor = '#228B22'
    elif response == '2':
        button2.fillColor = '#228B22'

    # 화면 갱신
    instruction_text.draw()
    q_text.draw()
    a1_text.draw()
    a2_text.draw()
    button1.draw()
    button2.draw()
    button1_label.draw()
    button2_label.draw()
    for opt_text in option_texts:
        opt_text.draw()
    win.flip()
    core.wait(0.5)

# 데이터 저장
file_exists = os.path.isfile('results.csv')
with open('results.csv', 'a', newline='') as csvfile:
    fieldnames = list(trial_list[0].keys()) + ['response', 'rt', 'is_correct']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if not file_exists:
        writer.writeheader()
    for (trial, resp, rt_val) in responses:
        row = trial.copy()
        row['response'] = resp
        row['rt'] = rt_val
        selected_source = trial['answer1_label'] if resp == '1' else trial['answer2_label']
        row['is_correct'] = (selected_source == 'human')
        writer.writerow(row)

win.close()