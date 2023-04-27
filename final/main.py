import cv2
import numpy as np

cap = cv2.VideoCapture('coin04.mp4')

coin_num = 0
coin_dict = {}  # 存储每个硬币
frames = []

while (cap.isOpened()):

    ret, frame = cap.read()

    if not ret:
        break

    # 灰度
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 模糊
    blur = cv2.GaussianBlur(gray, (11, 11), 0)

    # 边缘
    canny = cv2.Canny(blur, 30, 150)

    # 轮廓
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 过滤面积太小的轮廓
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]

    # 判断是否为圆形
    coin_contours = []
    for cnt in contours:
        # 面积和周长
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)

        # 面积/周长之比接近圆形
        if 0.7 < area / (np.pi * perimeter ** 2 / 4) < 1.3:
            coin_contours.append(cnt)

    # 绘制最小外接圆和圆心
    for cnt in contours:
        # 最小外接圆
        (x, y), radius = cv2.minEnclosingCircle(cnt)

        found = False
        for key, value in coin_dict.items():
            # 坐标相近视为同一硬币
            if abs(x - value[0]) < 50 and abs(y - value[1]) < 50:
                found = True
                break
        if found:
            # 硬币编号
            num = key
        else:
            num = coin_num
            coin_dict[num] = (x, y)
            coin_num += 1

        # 绘制最小外接圆
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)

        # 标注硬币序号
        cv2.putText(frame, '#' + str(num),
                    (int(x) - 10, int(y)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # 圆心坐标
        cv2.putText(frame, 'position: ' + '(' + str(int(x)) + ',' + str(int(y)) + ')',
                    (int(x) - 150, int(y) + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # 显示结果
    frame = cv2.resize(frame, (440, 750))  # 设置大小
    cv2.imshow('Output', frame)

    # 按q退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
