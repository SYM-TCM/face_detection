# 调用摄像头，进行人脸捕获，和68个特征点的追踪
# Real-time facial landmarks detect from camera

# Author:   coneypo
# Blog:     http://www.cnblogs.com/AdaminXie
# GitHub:   https://github.com/coneypo/Dlib_face_detection_from_camera

# Created at 2018-02-26
# Updated at 2019-04-01

import dlib         # 人脸识别的库 Dlib
import numpy as np  # 数据处理的库 numpy
import cv2          # 图像处理的库 OpenCv
import time
import os

# 储存截图的目录
path_screenshots = "img/"

# Dlib 正向人脸检测
detector = dlib.get_frontal_face_detector()
# Dlib 人脸特征点预测
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# 创建 cv2 摄像头对象
cap = cv2.VideoCapture(0)

# cap.set(propId, value)
# 设置视频参数，propId 设置的视频参数，value 设置的参数值
#具体参数见：https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html
#3，表示设置宽度，480表示设置为480宽
cap.set(3, 480)



# Delete all the screenshots
def del_ss():
    ss = os.listdir("img/")
    for image in ss:
        print("Remove: ", "img/"+image)
        os.remove("img/"+image)

#删除文件夹原始图像
#del_ss()


# 截图 screenshots 的计数器
ss_cnt = 0

# cap.isOpened() 返回 true/false 检查初始化是否成功
while cap.isOpened():

    # cap.read()
    # 返回两个值：
    #    一个布尔值 true/false，用来判断读取视频是否成功/是否到视频末尾
    #    图像对象，图像的三维矩阵
    flag, im_rd = cap.read()

    # 每帧数据延时 1ms，延时为 0 读取的是静态帧
    k = cv2.waitKey(1)

    # 取灰度
    img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)

    # 人脸数
    faces = detector(img_gray, 0)

    # 待会要写的字体
    font = cv2.FONT_HERSHEY_SIMPLEX

    # 检测到人脸
    if len(faces) != 0:
        for i in range(len(faces)):
            landmarks = np.matrix([[p.x, p.y] for p in predictor(im_rd, faces[i]).parts()])

            # 标68个点
            for idx, point in enumerate(landmarks):
                # 68点的坐标
                pos = (point[0, 0], point[0, 1])

                # 特征点画圈
                cv2.circle(im_rd, pos, 2, color=(255, 255, 255))
                # 写1-68
                cv2.putText(im_rd, str(idx + 1), pos, font, 0.2, (187, 255, 255), 1, cv2.LINE_AA)

        cv2.putText(im_rd, "Faces: " + str(len(faces)), (20, 50), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
    else:
        # 没有检测到人脸
        cv2.putText(im_rd, "No face detected", (20, 50), font, 1, (0, 0, 0), 1, cv2.LINE_AA)

    # 添加说明
    im_rd = cv2.putText(im_rd, "'S': screenshot", (20, 400), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
    im_rd = cv2.putText(im_rd, "'Q': quit", (20, 450), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)

    # 按下 's' 键保存
    if k == ord('s'):
        ss_cnt += 1
        print(path_screenshots + "ss_" + str(ss_cnt) + "_" +
              time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + ".jpg")
        cv2.imwrite(path_screenshots + "ss_" + str(ss_cnt) + "_" +
                    time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + ".jpg", im_rd)

    # 按下 'q' 键退出
    if k == ord('q'):
        break

    # 窗口显示
    # 参数取 0 可以拖动缩放窗口，为 1 不可以
    # cv2.namedWindow("camera", 0)
    cv2.namedWindow("camera", 1)

    cv2.imshow("camera", im_rd)

# 释放摄像头
cap.release()

# 删除建立的窗口
cv2.destroyAllWindows()