#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/2 002 20:13
# @Author  : willis
# @Site    :
# @File    : Mp4.py
# @Software: PyCharm

# 用于将视频转换为字符画，并在unix终端播放

import numpy as np
import os


class Mp42Chars:

    def video2imgs(self, video, size):

        from cv2 import VideoCapture
        from cv2 import cvtColor, resize
        from cv2 import COLOR_BGR2GRAY
        from cv2 import INTER_AREA

        img_list = []

        # 从指定文件创建一个VideoCapture对象
        cap = VideoCapture(video)

        # 如果cap对象已经初始化完成了，就返回true，换句话说这是一个 while true 循环
        while cap.isOpened():
            # cap.read() 返回值介绍：
            #   ret 表示是否读取到图像
            #   frame 为图像矩阵，类型为 numpy.ndarry.
            ret, frame = cap.read()
            if ret:
                # 转换成灰度图，也可不做这一步，转换成彩色字符视频。
                gray = cvtColor(frame, COLOR_BGR2GRAY)

                # resize 图片，保证图片转换成字符画后，能完整地在命令行中显示。
                img = resize(gray, size, interpolation=INTER_AREA)

                # 分帧保存转换结果
                img_list.append(img)
            else:
                break

        # 结束后释放空间
        cap.release()

        return img_list

    # 图片转字符画
    def img2chars(self, img):
        """
        :param img: numpy.ndarray, 图像矩阵
        :return: 字符串的列表：图像对应的字符画，其每一行对应图像的一行像素

        """
        # 目前5 3的效果较好
        chars = {
            '1': " .,-'`:!1+*abcdefghijklmnopqrstuvwxyz<>()\/{}[]?234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ%&@#$"[::-1],
            '1-1': r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
            '1-2': r"$kB%8&WM#*oa&**@qwmZO0QLCJUYXzcvun<rjft/\|()1{}[]?-_+~<>i!lI;:,\ ^`'. ",
            '2': "@MBHAXG89S5h1ri;:,. ",
            '3': '@w#$kdtji. ',
            '4': "@BAG951i:. ",
            '5': ".`_-'\"^;=L~!cxIr*ZCg{9FE[R/Ydnpq#V$OMHBU"[::-1]
        }

        pixels = chars['3']

        res = []
        # 要注意这里的顺序和 之前的 size 刚好相反
        height, width = img.shape
        for row in range(height):
            line = ""
            for col in range(width):
                # 灰度是用8位表示的，最大值为255。
                # 这里将灰度转换到0-1之间
                percent = img[row][col] / 255

                # 将灰度值进一步转换到 0 到 (len(pixels) - 1) 之间，这样就和 pixels 里的字符对应对应起来了
                index = int(percent * (len(pixels) - 1))

                # 添加字符像素（最后面加一个空格，是因为命令行有行距却没几乎有字符间距，用空格当间距）
                # 后来发现画面太淡，又去掉了空格
                line += pixels[index]   # + " "
            res.append(line)

        return res

    def imgs2chars(self, imgs):
        video_chars = []
        for img in imgs:
            video_chars.append(self.img2chars(img))

        return video_chars

    def play_video(self, video_chars):
        """
        curses 只支持 类 unix 系统 不能再win中运行
        :param video_chars:字符画的列表，每个元素为一帧
        :return:
        """
        if os.name == 'nt':
            print('curses 只支持 类 unix 系统 不能再win中运行')
            return
        import time
        import curses

        width, height = len(video_chars[0][0]), len(video_chars[0])

        stdscr = curses.initscr()
        curses.start_color()
        try:
            # 调整窗口大小，宽度最好略大于字符画宽度。另外注意curses的height和width的顺序
            stdscr.resize(height, width * 2)

            for pic_i in range(len(video_chars)):
                # 显示 pic_i，即第i帧字符画
                for line_i in range(height):
                    # 将pic_i的第i行写入第i列。(line_i, 0)表示从第i行的开头开始写入。最后一个参数设置字符为白色
                    stdscr.addstr(line_i, 0, video_chars[pic_i][line_i], curses.COLOR_WHITE)
                stdscr.refresh()  # 写入后需要refresh才会立即更新界面

                time.sleep(1 / 24)  # 粗略地控制播放速度。更精确的方式是使用游戏编程里，精灵的概念
        finally:
            # curses 使用前要初始化，用完后无论有没有异常，都要关闭
            curses.endwin()
        return


if __name__ == '__main__':
    mp4 = Mp42Chars()
    # (150, 120)
    imgs = mp4.video2imgs('dglk.mp4', (50, 40))
    # assert len(imgs) > 10
    video_chars = mp4.imgs2chars(imgs)
    # assert len(video_chars) > 10
    mp4.play_video(video_chars)
