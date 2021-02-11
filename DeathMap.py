import cv2
import math
import numpy
import subprocess
from subprocess import call

# cv2.putText(img, str(a[i]), (int(a[i + 2]), int(a[i + 1])), cv2.FONT_HERSHEY_SIMPLEX, 0.1, (255, 0, 255), 2)
# cv2.line(img, (0, 0), (200, 200), (255, 255, 255), 10)
# cv2.rectangle(img, (0, 0), (50, 50), (255, 0, 0), -1)
MyDirectory = "C:/Project/"
DirtRoom = MyDirectory + "Stereopair/Data/"

WhiteRect = cv2.imread(DirtRoom + "WhiteRectangle.jpg")
DoublePict = cv2.imread(MyDirectory + "Stereopair/Stereopair.jpg")

ResultPict = MyDirectory + "Results.jpg"
Cam1Pict = DirtRoom + "Cam1.jpg"
Cam2Pict = DirtRoom + "Cam2.jpg"
Cam1Res = DirtRoom + "Cam1.txt"
Cam2Res = DirtRoom + "Cam2.txt"
windowName = 'Result'
# Rofl = MyDirectory + "Dungeon.jpg"
# ResultPict, windowName = Rofl, Rofl[Rofl.rfind('/') + 1:Rofl.rfind('.')]

Dcam = 120
rcam = 0.02
focus = 100000
probability = 38
if __name__ == "__main__":
    width = int(DoublePict.shape[1])
    height = int(DoublePict.shape[0])
    # width, height = 300, 300

    Cam1 = DoublePict[0:height, 0:(int)(width / 2)].copy()
    Cam2 = DoublePict[0:height, (int)(width / 2):width].copy()
    cv2.imwrite(Cam1Pict, Cam1)
    cv2.imwrite(Cam2Pict, Cam2)

    subprocess.call("C:/Project/Stereopair/Darknet.sh", shell=True)

    ipt, ndel, nmap, v = [], [], [], []
    for op in [1, 2]:
        if op == 1:
            fin = open(Cam1Res, "r")
        if op == 2:
            fin = open(Cam2Res, "r")
        for i in range(0, 11):
            line = fin.readline()
            pass
        for line in fin:
            if line == "endstream\n" or line == ("endstream"):
                break
                pass
            else:
                ipt.append(line[0:len(line)-2])
        fin.close()

    for i in range(0, len(ipt)):
        line = ipt[i]
        line = line.replace("%	(left_x:", " ")
        line = line.replace("  top_y: ", " ")
        line = line.replace("  width:  ", " ")
        line = line.replace("  height:  ", " ")
        line = line.replace(": ", " ")
        line = line.replace("     ", " ")
        line = line.replace("    ", " ")
        line = line.replace("   ", " ")
        line = line.replace("  ", " ")
        line = line.replace(" ", " ")
        ipt[i] = line
    for lin in ipt:
        line = lin
        h = (int)(line[line.rfind(" "):])
        line = line[:line.rfind(" ")]
        w = (int)(line[line.rfind(" "):])
        line = line[:line.rfind(" ")]
        y = (int)(line[line.rfind(" "):])
        line = line[:line.rfind(" ")]
        x = (int)(line[line.rfind(" "):])
        line = line[:line.rfind(" ")]
        p = (int)(line[line.rfind(" "):])
        line = line[:line.rfind(" ")]
        name = line
        if p > probability:
            v.append([name, p, x, y, w, h])

    dl = len(v)
    for i in range(dl - 1):
        for j in range(dl - i - 1):
            if v[j] > v[j+1]:
                v[j], v[j+1] = v[j+1], v[j]
    t = 0
    while t < dl:
        tl = 0
        while (t + tl) < dl and v[t][0] == v[t + tl][0]:
            tl = tl + 1
        t = t + tl
        nmap.append(tl)

    i1 = 0
    i2 = 0
    for tmp in nmap:
        i2 = i2 + tmp
        for i in range(i1, i2):
            for j in range(i1, i2 - 1):
                if v[j][5] + v[j][4] < v[j + 1][5] + v[j + 1][4]:
                    v[j], v[j + 1] = v[j + 1], v[j]
        i1 = i2

    tmp1, tmp2, pazniza = 0, 0, 15
    for i in range(0, len(v)):
        tf = 1
        if i < len(v) - 1:
            tmp1 = v[i][2] - v[i + 1][2]
            if tmp1 < pazniza and tmp1 > -1 * pazniza:
                tf = 0
        if i > 0:
            tmp2 = v[i][2] - v[i - 1][2]
            if tmp2 < pazniza and tmp2 > -1 * pazniza:
                tf = 0
        if tf == 1:
            ndel.append(i)

    for i in range(len(ndel)-1, -1, -1):
        tmp = (int)(ndel[i])
        v.pop(tmp)

    for i in range(0, len(v)):
        print(v[i][0], " ", v[i][1], " ", v[i][2], " ", v[i][3], " ", v[i][4], " ", v[i][5])
        pass
    # Build depth map start
    Dcam = Dcam / 360 * math.pi

    Red = (89, 16, 222)
    Green = (0, 255, 0)
    Blue = (222, 131, 49)
    White = (255, 255, 255)
    Black = (0, 0, 0)

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    fontColor = Red
    LineColor = Blue
    fontType = 2
    LineType = 3
    cv2.namedWindow(windowName)
    img = WhiteRect
    width = int(Cam1.shape[1])
    height = int(Cam1.shape[0])
    print("Input Picture\n  width: ", width, "height: ", height, '\n')

    polew, poleh = 36, 36
    img = cv2.resize(img, (width + polew, height + poleh), interpolation=cv2.INTER_AREA)
    cv2.rectangle(img, (0, 0), (width + polew, height + poleh), White, -1)
    cv2.rectangle(img, (polew, 0), (polew + width - 2, height), Red, 4)

    cv2.line(img, (polew, 0), ((int)(polew / 2), (int)(polew / 2)), Black, 3)
    cv2.line(img, (polew, 0), ((int)(polew / 2 + polew), (int)(polew / 2)), Black, 3)
    cv2.line(img, (polew, 0), (polew, height), Black, 3)

    cv2.line(img, (polew + width, height), (width + (int)(polew / 2), height - (int)(poleh / 2)), Black, 3)
    cv2.line(img, (polew + width, height), (width + (int)(polew / 2), height + (int)(poleh / 2)), Black, 3)
    cv2.line(img, (polew, height), (polew + width, height), Black, 3)

    cv2.putText(img, '(0,0)', (7, height + (int)(poleh / 2 - 1)), font, fontScale, Black, 2)

    strt = 50
    for i in range(strt, height, strt):
        if i > height - 30:
            break
        cv2.line(img, (polew - 6, height - i), (polew + 6, height - i), Black, 2)
        cv2.putText(img, (str)(i / 100), (0, height - i - 5), font, fontScale, Black, 2)

    for i in range(strt, width, strt):
        if i > width - 30:
            break
        cv2.line(img, (polew + i, height + 6), (polew + i, height - 6), Black, 2)
        cv2.putText(img, (str)(i / 100), (i + polew, (int)(height + poleh / 2)), font, fontScale, Black, 2)

    for i in range(0, len(v), 2):
        # Line
        x1 = v[i][2] + v[i][4] / 2
        x2 = v[i + 1][2] + v[i + 1][4] / 2
       # print(x1, x2)
        m = (int)((focus * rcam) / abs(x1 - x2))

        first = (int)((v[i][2] + v[i + 1][2]) / 2)
        second =(int)((v[i][2] + v[i + 1][2] + v[i][4] + v[i + 1][4]) / 2)

        Dheight = height - int(m)
        LeftLineCorner = (int(first) + polew, Dheight)
        RightLineCorner = (int(second) + polew, Dheight)
        cv2.line(img, LeftLineCorner, RightLineCorner, LineColor, LineType)

    for i in range(0, len(v), 2):
        # Text
        name = v[i][0] + " " + (str)((v[i][1]+v[i+1][1])/2)+ "% "
        x1 = v[i][2] + v[i][4] / 2
        x2 = v[i + 1][2] + v[i + 1][4] / 2
        m = (int)((focus * rcam) / abs(x1 - x2))
        first = (int)((v[i][2] + v[i + 1][2]) / 2)

        Dheight = height - int(m)
        StartCornerOfText = (int(first) + polew, Dheight - 5)
        cv2.putText(img, str(name), StartCornerOfText, font, fontScale, fontColor, fontType)

    ColorOfArrow = Red
    cv2.putText(img, 'y(m)', (0, 20), 2, 1, ColorOfArrow, 2)
    cv2.putText(img, 'x(m)', (width - polew, poleh + height - 3), 2, 1, ColorOfArrow, 2)

    while (True):
        cv2.imshow(windowName, img)
        a = cv2.waitKey(0)
        if a == ord('a'):
            print("Pressed A --> Saved --> Break")
            cv2.imwrite(ResultPict, img)
            cv2.destroyAllWindows()
            break

        if a == ord('q'):
            print("Pressed Q --> Break")
            cv2.destroyAllWindows()
            break

        if a == ord('z'):
            print("Pressed Z --> Clear")
            cv2.rectangle(img, (0, 0), (width + polew + 10, height + poleh + 10), White, -1)

    cv2.imwrite("Results.jpg", img)
