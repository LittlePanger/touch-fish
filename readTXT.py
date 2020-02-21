# -*- coding: utf-8 -*-
import os
import re
import sys
from pynput import mouse, keyboard

filename = sys.argv[1]
size = 20 if len(sys.argv) < 3 else int(sys.argv[2])
total_size = os.path.getsize(filename)
total_page = round(total_size/size)
# print(total_page)


def read_chunks(start_page):
    cur_page = start_page
    with open(filename, encoding='utf-8')as f:
        if start_page != 0:
            f.seek((start_page-1) * 90)
            cur_page = start_page -1
        while 1:
            cur_page += 1
            data = f.read(size)
            print(f.tell())
            if not data:
                break
            yield data + f'     ({cur_page}/{total_page})'


def on_press(key):
    if key == keyboard.KeyCode.from_char('t'):
        input_page = input('跳到第几页')
        start_page = int(re.findall(r'\d+', input_page)[0])
        print('start_page',start_page)
        global f
        f = read_chunks(start_page)
        os.system('clear')
        print(f.__next__())
    if key == keyboard.KeyCode.from_char('q'):
        os.system('clear')
        print(f.__next__())
    if key == keyboard.KeyCode.from_char('h'):
        print('q键下一页,t键跳转,esc退出')


def on_release(key):
    if key == keyboard.Key.esc:
        os.system('clear')
        return False  # 返回False 就停止监听


f = read_chunks(0)

# 监听键盘按键
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
