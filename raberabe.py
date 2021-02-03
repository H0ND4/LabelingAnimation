import cv2
import numpy as np
import random
import datetime

#
# LookupTableよりラベルを更新
# lut, 対象のインデックス 
# #
def raberabe(lut, index):
    if(lut[index] == index):
        return lut[index]
    else:
        index = lut[index]
        return raberabe(lut, index)

#
# RGB3色ランダムで所得
# label：ラベルの配列， max：ラベルの最大数
# #
def Label_Paint(label, max):
    clr_table = np.zeros(1, dtype=int)
    # 3色登録
    for i in range(max):
        for j in range(3):
            rgb = int(random.uniform(0, 256))
            clr_table = np.append(clr_table, rgb)
    clr_table[0] = 0
    clr_table[1] = 0
    clr_table[2] = 0

    return clr_table

# 
# ラベリング処理
# #
def OnLabeling():
    img = cv2.imread("./1.png")
    rgb_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rgb_im2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    i = 0
    j = 0
    a = 1
    lut = np.zeros(20000, dtype=int)
    for i in range(20000):
        lut[i] = i
    label = np.zeros((img.shape[0], img.shape[1]), dtype=int)

    # ランダム色
    color = Label_Paint(label, 2002)

    # こっから
    for i in range(img.shape[1]):
        for j in range(img.shape[0]):
            if (img[i][j][0] == 0):  # 背景
                label[i][j] = 0
            else:
                if(i == 0 and j == 0):  # 左上端のとき
                    qqqq = 0
                elif(i == 0):  # 上端の時
                    if(label[i][j-1] != 0):
                        label[i][j] = label[i][j-1]
                    else:  # 背景ならば新しいラベル
                        label[i][j] = lut[a]
                        a = a+1
                # ここまで上端の処理

                elif(j == 0):  # 左端のとき（背景以外）
                    label[i][j] = lut[a]  # 一度新しいラベル入れる
                    if(label[i-1][j] != 0):  # 上のラベルが背景じゃない時
                        if(label[i-1][j] < label[i][j]):  # ラベルが最小じゃないなら
                            label[i][j] = label[i-1][j]  # ラベルを最小に
                    if(label[i][j] == lut[a]):  # 最終的に新しいラベルが加えられら
                        a = a+1
                # ここまで左端処理

                # 他の場所
                else:
                    label[i][j] = lut[a]  # 一度次のラベル入れる

                    if(label[i-1][j] != 0 and img[i-1][j][0] == img[i-1][j][0]):
                        if(label[i-1][j] < label[i][j]):  # 上の方が小さい時
                            label[i][j] = label[i-1][j]  # ラベル最小

                    if(label[i][j-1] != 0 and img[i][j-1][0] == img[i][j][0]):
                        if(label[i][j] > label[i][j-1]):  # 左が小さい
                            label[i][j] = label[i][j-1]

                    # 最終的に新しいラベルが与えられたら
                    if(label[i][j] == lut[a]):
                        a = a+1

                    if(label[i-1][j] != 0 and img[i-1][j][0] == img[i][j][0]):
                        if(label[i-1][j] > label[i][j]):
                            lut[raberabe(lut, label[i-1][j])
                                ] = raberabe(lut, label[i][j])

                    if(label[i][j-1] != 0 and img[i][j-1][0] == img[i][j-1][0]):
                        if(label[i][j-1] > label[i][j]):
                            lut[raberabe(lut, label[i][j-1])
                                ] = raberabe(lut, label[i][j])
                # ここまで他

        # 塗り替え
        for ii in range(rgb_im.shape[0]):
            for jj in range(rgb_im.shape[1]):
                if(rgb_im[ii][jj][0] != 0):
                    rgb_im2[ii][jj][0] = color[label[ii][jj]]
                    rgb_im2[ii][jj][1] = color[label[ii][jj]+1]
                    rgb_im2[ii][jj][2] = color[label[ii][jj]+2]
        # 処理過程描画
        dasu = cv2.cvtColor(rgb_im2, cv2.COLOR_RGB2BGR)
        now = datetime.datetime.now()
        filename = './anim/' + now.strftime('%Y%m%d_%H%M%S') + '.png'
        reslut = cv2.imwrite(filename, dasu)

    # ラベリング
    for i in range(a):
        lut[i] = raberabe(lut, i)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            label[i][j] = lut[label[i][j]]

        # 塗り替え
        for ii in range(rgb_im.shape[0]):
            for jj in range(rgb_im.shape[1]):
                if(rgb_im[ii][jj][0] != 0):
                    rgb_im2[ii][jj][0] = color[label[ii][jj]]
                    rgb_im2[ii][jj][1] = color[label[ii][jj]+1]
                    rgb_im2[ii][jj][2] = color[label[ii][jj]+2]
        # 処理過程描画
        dasu = cv2.cvtColor(rgb_im2, cv2.COLOR_RGB2BGR)
        now = datetime.datetime.now()
        filename = './anim/' + now.strftime('%Y%m%d_%H%M%S') + '.png'
        reslut = cv2.imwrite(filename, dasu)

    #color = Label_Paint(label,a)

    # 塗り替え
    for i in range(rgb_im.shape[0]):
        for j in range(rgb_im.shape[1]):
            if(rgb_im[i][j][0] != 0):
                rgb_im2[i][j][0] = color[label[i][j]]
                rgb_im2[i][j][1] = color[label[i][j]+1]
                rgb_im2[i][j][2] = color[label[i][j]+2]


    # 描画

    #cv2.imshow('image', rgb_im2)
    # cv2.waitKey(0)


OnLabeling()
