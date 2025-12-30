import pygetwindow as gw
import pyautogui
import random
import time
import keyboard

def in_parallelogram(x, y, A, B, C, D):
    def cross_product(ax, ay, bx, by, px, py):
        # 计算 (B-A) x (P-A) 的叉积
        return (bx - ax) * (py - ay) - (by - ay) * (px - ax)
    
    # 计算叉积
    cross1 = cross_product(A[0], A[1], B[0], B[1], x, y)
    cross2 = cross_product(B[0], B[1], C[0], C[1], x, y)
    cross3 = cross_product(C[0], C[1], D[0], D[1], x, y)
    cross4 = cross_product(D[0], D[1], A[0], A[1], x, y)
    
    # 检查叉积符号是否一致
    return (cross1 >= 0 and cross2 >= 0 and cross3 >= 0 and cross4 >= 0) or \
           (cross1 <= 0 and cross2 <= 0 and cross3 <= 0 and cross4 <= 0)

def on_space_pressed():
    global pause_flag
    pause_flag = not pause_flag
    if pause_flag:
        print("已暂停")
    else:
        print("继续运行")

def enter_mine(left, top):
    # 取相对窗口的坐标
    pyautogui.press('d') # 打开地图
    time.sleep(0.5)
    pyautogui.moveTo(left + 460, top + 153)  # 点击公共场景
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.moveTo(left + 410, top + 172)  # 点击矿洞
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.moveTo(left + 619, top + 318)  # 点击进入二星矿洞二区
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.moveTo(left + 563, top + 317)  # 点击直接进入
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.press('d') # 关闭地图
    time.sleep(5)

def mining_loop(left, top, A, B, C, D):
    global exit_flag, pause_flag

    # 手动确定第一次点击位置（矿场中心），使进入循环时两变量不为空
    random_x, random_y = 477, 352
    # 记录特殊位置的上次点击时间
    last_special_click_time = 0
    # 记录特殊像素点的上次检测时间
    last_special_colour_time = 0

    while not exit_flag:
        # 暂停检测
        while pause_flag:
            time.sleep(0.5)
            if exit_flag:
                return

        rx = random.randint(-70, 70)
        ry = random.randint(-70, 70)

        if not in_parallelogram(random_x + rx, random_y + ry, A, B, C, D):
            continue

        random_x += rx
        random_y += ry

        current_time = time.time()

        # 模拟鼠标移动到随机位置并点击
        pyautogui.click(left + random_x, top + random_y)
        time.sleep(0.5) 
        pyautogui.click(left + random_x, top + random_y)
        time.sleep(0.5) # 等小人走到该位置

        # 检查是否到达特殊位置点击的时间
        if current_time - last_special_click_time >= 6:
            pyautogui.click(left + 421, top + 355)
            last_special_click_time = current_time

        # 检查是否到达特殊像素点检测的时间
        if current_time - last_special_colour_time >= 40: # 每隔40秒检测一次特殊像素点颜色
            color = pyautogui.pixel(left + 613, top + 42)
            print("检测背景颜色：", color)

            if color != (0, 0, 0): # 如果不为全黑，证明已被炸出矿洞
                break

            # 更新最后检测的时间
            last_special_colour_time = current_time


# main
pyautogui.FAILSAFE = True

windows = gw.getWindowsWithTitle('皮卡堂')

if windows:
    target_window = windows[0]
    target_window.activate()
    time.sleep(1)

    # 获取窗口的坐标和大小
    left, top, width, height = target_window.left, target_window.top, target_window.width, target_window.height
    print("按空格暂停/继续，Esc键退出程序")

    # 取边界点，顺序：左上右下
    A = (245, 361)
    B = (480, 254)
    C = (740, 361)
    D = (489, 466)

    # 定义一个退出和暂停标志
    exit_flag = False
    pause_flag = False

    # 监听快捷键Esc
    def on_esc_pressed():
        global exit_flag
        exit_flag = True
        print("检测到 Esc 键，退出脚本...")

    # 注册快捷键
    keyboard.add_hotkey('Esc', on_esc_pressed)
    keyboard.add_hotkey('space', on_space_pressed)

    while not exit_flag:
        # 暂停检测
        while pause_flag:
            time.sleep(0.5)
            if exit_flag:
                break

        print("进入矿洞")
        enter_mine(left, top)

        print("开始挖矿")
        mining_loop(left, top, A, B, C, D)

        print("等待重新进入矿洞")
        time.sleep(3)

else:
    print("未找到 '皮卡堂' 窗口")
