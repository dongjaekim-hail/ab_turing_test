from psychopy import visual, event, data, core
import random
import csv
import os

# PsychoPy 창 생성 (정사각형으로 설정)
win = visual.Window(size=[800, 600], fullscr=False, color='#DCDCDC')

# 마우스 객체 생성
mouse = event.Mouse(win=win)

# 지침 텍스트
instruction1 = visual.TextStim(win, text="이 실험은 한 질문에 두 개의 답변을 보여 줍니다. 두 답변 중 하나는 사람이, 나머지 하나는 AI가 작성한 것입니다.", 
                              pos=[0, 0.4], height=0.07, color='#333333', alignText='center', font='Malgun Gothic')
instruction2 = visual.TextStim(win, text="어떤 답변이 더 사람처럼 느껴지나요? A1이나 A2 버튼으로 선택해 주세요.", bold=True, 
                              pos=[0, 0.1], height=0.07, color='#333333', alignText='center', font='Malgun Gothic')

escape = visual.TextStim(win, text="실험을 시작하려면 s키를 눌러주세요. \n(중간에 종료하려면 q키)", 
                         pos=[0, -0.1], height=0.05, color='black')

instruction1.draw()
instruction2.draw()
escape.draw()
win.flip()
event.waitKeys(keyList=['s'])

# CSV 파일에서 시행 조건 불러오기
csv_path = r"C:\Users\HyunJun\Desktop\Q&A DATA.csv"
conditions = data.importConditions(csv_path)
trial_list = conditions[:]  # 리스트 복사
random.shuffle(trial_list)  # 랜덤 순서로 섞기

# 응답 저장 리스트와 현재 인덱스 초기화
responses = []
current_index = -1

while current_index < len(trial_list) - 1:
    current_index += 1
    if current_index >= len(trial_list):
        break
    trial = trial_list[current_index]

    # 지침 텍스트
    instruction_text = visual.TextStim(win, text="더 인간같은 답변을 클릭해 주세요", 
                                       pos=[0.9, 0.9], height=0.05, wrapWidth=1.2, 
                                       color='#333333', alignText='left', font='Malgun Gothic')

    # 질문과 답변 텍스트
    q_text = visual.TextStim(win, text=f"Q. {trial['question']}", 
                             pos=[-0.3, 0.7], height=0.08, wrapWidth=1.2, 
                             color='#333333', bold=True, alignText='left', font='JetBrains Mono')
    a1_text = visual.TextStim(win, text=f"A1. {trial['answer1']}", 
                              pos=[0, 0.3], height=0.05, wrapWidth=1, 
                              color='#333333', alignText='left', font='Malgun Gothic')
    a2_text = visual.TextStim(win, text=f"A2. {trial['answer2']}", 
                              pos=[0, 0.0], height=0.05, wrapWidth=1, 
                              color='#333333', alignText='left', font='Malgun Gothic')

    # 응답 버튼 (기본 색상 설정)
    button1 = visual.Circle(win, radius=0.12, pos=[-0.3, -0.4], fillColor="#FF0000", 
                            lineColor='black', lineWidth=5, opacity=0.9)
    button2 = visual.Circle(win, radius=0.12, pos=[0.3, -0.4], fillColor="#FF0000", 
                            lineColor='black', lineWidth=5, opacity=0.9)
    button1_label = visual.TextStim(win, text="A1", pos=[-0.3, -0.6], height=0.05, color='black')
    button2_label = visual.TextStim(win, text="A2", pos=[0.3, -0.6], height=0.05, color='black')

    # "NEXT"와 "Go Back" 버튼
    proceed_button = visual.Rect(win, width=0.2, height=0.1, pos=[0.8, -0.8], fillColor='black')
    go_back_button = visual.Rect(win, width=0.2, height=0.1, pos=[0.6, -0.8], 
                                 fillColor='black' if current_index > 0 else '#DCDCDC')
    proceed_label = visual.TextStim(win, text="NEXT", pos=[0.8, -0.8], height=0.05, color='white')
    go_back_label = visual.TextStim(win, text="BACK", pos=[0.6, -0.8], height=0.05, color='white' if current_index > 0 else "#DCDCDC")
    line = visual.TextStim(win, text="ㅣ", pos=[0.7, -0.8], height=0.08, color='gray' if current_index > 0 else '#DCDCDC')

    # 화면 표시
    instruction_text.draw()
    q_text.draw()
    a1_text.draw()
    a2_text.draw()
    button1.draw()
    button2.draw()
    button1_label.draw()
    button2_label.draw()
    proceed_button.draw()
    go_back_button.draw()
    proceed_label.draw()
    go_back_label.draw()
    line.draw()
    win.flip()

    # 사용자 응답 수집 및 선택 변경 가능
    mouse.setVisible(True)
    response = None  # 응답 초기화
    while True:
        # 버튼 클릭 체크
        if button1.contains(mouse) and mouse.getPressed()[0]:
            response = '1'
            button1.fillColor = '#228B22'  # 초록색으로 변경
            button2.fillColor = '#FF0000'  # 다른 버튼 원래 색상으로 복귀
        elif button2.contains(mouse) and mouse.getPressed()[0]:
            response = '2'
            button2.fillColor = '#228B22'  # 초록색으로 변경
            button1.fillColor = '#FF0000'  # 다른 버튼 원래 색상으로 복귀

        # "NEXT" 또는 "BACK" 클릭 체크
        if proceed_button.contains(mouse) and mouse.getPressed()[0] and response is not None:
            responses.append((trial, response))
            break  # 다음 시행으로 이동
        elif go_back_button.contains(mouse) and mouse.getPressed()[0] and current_index > 0:
            if responses:
                responses.pop()  # 잘못된 응답 삭제
            current_index -= 2  # 이전 시행으로 돌아가기
            break

        # 종료 키 체크
        keys = event.getKeys(keyList=['q'])
        if 'q' in keys:
            # 종료 전 응답 저장
            file_exists = os.path.isfile('results.csv')
            with open('results.csv', 'a', newline='') as csvfile:
                fieldnames = list(trial_list[0].keys()) + ['response', 'is_correct']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                for (trial, resp) in responses:
                    row = trial.copy()
                    row['response'] = resp
                    selected_source = trial['answer1_label'] if resp == '1' else trial['answer2_label']
                    row['is_correct'] = (selected_source == 'human')
                    writer.writerow(row)
            win.close()
            core.quit()

        # 화면 업데이트
        instruction_text.draw()
        q_text.draw()
        a1_text.draw()
        a2_text.draw()
        button1.draw()
        button2.draw()
        button1_label.draw()
        button2_label.draw()
        proceed_button.draw()
        go_back_button.draw()
        proceed_label.draw()
        go_back_label.draw()
        line.draw()
        win.flip()
        core.wait(0.15)

# 데이터 저장 (모든 질문에 전부 대답한 경우)
file_exists = os.path.isfile('results.csv')
with open('results.csv', 'a', newline='') as csvfile:
    fieldnames = list(trial_list[0].keys()) + ['response', 'is_correct']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if not file_exists:
        writer.writeheader()
    for (trial, resp) in responses:
        row = trial.copy()
        row['response'] = resp
        selected_source = trial['answer1_label'] if resp == '1' else trial['answer2_label']
        row['is_correct'] = (selected_source == 'human')
        writer.writerow(row)

win.close()