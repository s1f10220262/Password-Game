# -*- coding: utf-8 -*-

import pygame
import random as rd
from pygame.locals import *
import sys, os, json, re, time

sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')

SCR_RECT = Rect(0, 0, 640, 480)
ROW, COL = 15, 20
GS = 32

font_name = "data/font/NotoSansJP-VariableFont_wght.ttf"

def load_quiz_data(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data['quiz']

quiz = []

event_data = {}
already_positions = []

start_time = time.time()
time_limit = 150

for num in range(3):
    while True:
        x = rd.randint(1, COL - 2)
        y = rd.randint(1, ROW - 2)
        pos = (x, y)
        if pos not in already_positions:
            already_positions.append(pos)
            event_data[pos] = num
            break


solved_events = set()

map_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

def load_image(filename, colorkey=None):
    filename = os.path.join("data", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print("Cannot load image:", filename)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

def draw_map(screen, event_img):
    for r in range(ROW):
        for c in range(COL):
            if map_data[r][c] == 0:
                screen.blit(grassImg, (c * GS, r * GS), (0, 128, GS, GS))
            elif map_data[r][c] == 1:
                screen.blit(sabakuImg, (c * GS, r * GS), (0, 128, GS, GS))
    for pos, quiz_index in event_data.items():
        if quiz_index not in solved_events:
            x, y = pos
            screen.blit(event_img, (x * GS, y * GS), (0, 0, GS, GS))

def handle_events(player_pos, pending_quiz):
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            if event.key == K_DOWN and player_pos['y'] < ROW - 1:
                player_pos['y'] += 1
            elif event.key == K_UP and player_pos['y'] > 0:
                player_pos['y'] -= 1
            elif event.key == K_LEFT and player_pos['x'] > 0:
                player_pos['x'] -= 1
            elif event.key == K_RIGHT and player_pos['x'] < COL - 1:
                player_pos['x'] += 1
            elif event.key == K_SPACE and pending_quiz:
                return True
    return False

def show_quiz(screen, quiz):
    font = pygame.font.Font(font_name, 20)
    screen.fill((0, 0, 0))
    question_text = font.render(quiz["question"], True, (255, 255, 255))
    screen.blit(question_text, (20, 20))

    for i, option in enumerate(quiz["options"]):
        option_text = font.render(f"{i}: {option}", True, (255, 255, 255))
        screen.blit(option_text, (20, 60 + i * 40))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                if K_0 <= event.key <= K_9:
                    choice = event.key - K_0
                    return choice == quiz["answer"]

def show_result(screen, result):
    font = pygame.font.Font(font_name, 48)
    text = "正解" if result else "不正解"
    color = (0, 255, 0) if result else (255, 0, 0)
    result_text = font.render(text, True, color)

    screen.fill((0, 0, 0))
    screen.blit(result_text, (SCR_RECT.width // 2 - 50, SCR_RECT.height // 2))
    pygame.display.update()
    pygame.time.wait(2000)

import re

def show_quiz_with_regex(screen, quiz):
    font = pygame.font.Font(font_name, 20)
    screen.fill((0, 0, 0))
    question_text = font.render(quiz["question"], True, (255, 255, 255))
    screen.blit(question_text, (20, 20))
    pygame.display.update()

    user_input = ""
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == K_RETURN:
                    if re.fullmatch(quiz["pattern"], user_input):
                        return True
                    else:
                        return False
                elif event.key == K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        input_text = font.render(f"入力: {user_input}", True, (255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(question_text, (20, 20))
        screen.blit(input_text, (20, 60))
        pygame.display.update()

def handle_quiz(screen, quiz_item):
    if quiz_item["kind"] == "quiz":
        result = show_quiz(screen, quiz_item)
        show_result(screen, result)
        if result and "explain" in quiz_item:
            show_explanation(screen, quiz_item["explain"])
        return result
    elif quiz_item["kind"] == "regex":
        result = show_quiz_with_regex(screen, quiz_item)
        show_result(screen, result)
        return result
    else:
        raise ValueError(f"不明なクイズの種類: {quiz_item['kind']}")

def show_explanation(screen, explanation):
    font = pygame.font.Font(font_name, 20)
    screen.fill((0, 0, 0))
    explanation_text = font.render(explanation, True, (255, 255, 255))

    screen.blit(explanation_text, (20, SCR_RECT.height // 2))
    pygame.display.update()
    pygame.time.wait(3000)

def show_escape_success(screen):
    font = pygame.font.Font(font_name, 48)
    success_text = font.render("脱出成功！", True, (0, 255, 0))
    screen.fill((0, 0, 0))
    screen.blit(success_text, (SCR_RECT.width // 2 - 100, SCR_RECT.height // 2 - 24))
    pygame.display.update()
    pygame.time.wait(3000)

def show_failure(screen):
    font = pygame.font.Font(font_name, 48)
    failure_text = font.render("脱出失敗！", True, (255, 0, 0))
    screen.fill((0, 0, 0))
    screen.blit(failure_text, (SCR_RECT.width // 2 - 100, SCR_RECT.height // 2 - 24))
    pygame.display.update()
    pygame.time.wait(3000)


try:
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption("PyRPG クイズ対応版")
except Exception as e:
    print(f"初期化中にエラーが発生しました: {e}")
    pygame.quit()
    sys.exit(1)

playerImg = load_image("chara_tip/pipo-charachip005b.png", -1)
grassImg = load_image("pipo-map001/640x480/pipo-map001_at-tuti.png")
sabakuImg = load_image("pipo-map001/640x480/pipo-map001_at-sabaku.png")
event_Img = load_image("add_chara_tip/pipo-etcchara002c.png")
player_pos = {'x': 0, 'y': 0}
if len(sys.argv) < 2:
    print("JSONファイルのパスを指定してください。")
    sys.exit(1)

json_file_path = sys.argv[1]
quiz = load_quiz_data(json_file_path)

running = True
while running:
    draw_map(screen, event_Img)
    screen.blit(playerImg, (player_pos['x'] * GS, player_pos['y'] * GS), (0, 0, GS, GS))
    pygame.display.update()

    passed_time = time.time() - start_time
    if passed_time > time_limit:
        show_failure(screen)
        running = False
    
    pos = (player_pos['x'], player_pos['y'])
    pending_quiz = pos in event_data and event_data[pos] not in solved_events
    if handle_events(player_pos, pending_quiz) and pending_quiz:
        quiz_index = event_data[pos]
        quiz_item = quiz[quiz_index]
        result = handle_quiz(screen, quiz_item)
        if result:
            solved_events.add(quiz_index)

    if len(solved_events) == len(event_data):
        show_escape_success(screen)
        running = False

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

pygame.quit()
sys.exit()