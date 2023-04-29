import cv2
import matplotlib.pyplot as plt
import numpy as np
import math

height = 100
width = 120

# 楕円の長軸と短軸の設定
minors = [20, 20]
majors = [20, 20]
angles = [0, 0]
thickness = [5, -1]

# 0度から180度までの楕円を描く
for angle in range(0,181,10):
    minors.append(20)
    majors.append(50)
    angles.append(angle)
    thickness.append(-1)

# 画像のモーメントから丸っぽさと、伸びている方の角度を求める
def moments_round_angle(mom):
    X=mom["mu20"] + mom["mu02"]
    Y=((mom["mu20"] - mom["mu02"])**2 + 4.0 * mom["mu11"] **2)**0.5
    roundness = (1.0 - Y / X)**0.5
    if mom["mu20"] - mom["mu02"] == 0:
        angle = 0
    else:
        if mom["mu20"] - mom["mu02"]>0:
            angle = (math.atan(2.0*mom["mu11"]/(mom["mu20"] - mom["mu02"])) / 2.0)/math.pi*180
        else:
            angle = (math.atan(2.0*mom["mu11"]/(mom["mu20"] - mom["mu02"])) / 2.0)/math.pi*180+90
        if angle<0:
            angle += 180
    return roundness, angle

for mi, ma, an, th in zip(minors, majors, angles, thickness):
    img1 = np.zeros((height, width, 1))
    # OpenCVの角度の定義に変換するため -90
    img1 = cv2.ellipse(img1, ((width/2, height/2), (mi, ma), an-90), 255, thickness=th)
    plt.imshow(img1)
    plt.xlim(0, width)
    plt.ylim(0, height)
    plt.show()
    print("楕円の短軸長:",mi)
    print("楕円の長軸長:",ma)
    print("短軸長/長軸長:",mi/ma)
    print("楕円の角度:",an,"[deg]")
    print("楕円の厚み:",th)
    # 画像のモーメントを計算
    m1=cv2.moments(img1)
    print("丸っぽさ: {:.3f}".format(moments_round_angle(m1)[0]))
    print("角度: {:.1f} [deg]".format(moments_round_angle(m1)[1]))