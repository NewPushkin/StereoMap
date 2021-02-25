import cv2
import math
import numpy
import subprocess
from subprocess import call

# Camera Angle [Degrees] --> [Radians]
CamAngle = 120
CamAngle = CamAngle / 360 * math.pi
# CameraDistanse [millimeters] --> [meters]
CamDist = 20
CamDist = CamDist / 1000
# FocusDistance [millimeters] --> [meters]
FocusDist = 70
FocusDist = FocusDist / 1000
# Pixel Horizontal Resolution [pixels]
PxHor = 768
# Scale [meters --> pixel]
ScaleLen = 200
# Accuracy of detecting
Accuracy = 40
# PreCalculate
LenTmp = CamDist * PxHor / math.tan(CamAngle)

MyDirectory = "C:/Project/"
DirtRoom = MyDirectory + "Stereopair/" 

WhiteRect = cv2.imread(DirtRoom + "Data/WhiteRectangle.jpg")
DoublePict = cv2.imread(DirtRoom + "Stereopair.jpg")

ResultPict = MyDirectory + "Results.jpg"
Cam1Pict = DirtRoom + "Data/Cam1.jpg"
Cam2Pict = DirtRoom + "Data/Cam2.jpg"
Cam1Res = DirtRoom + "Data/Cam1.txt"
Cam2Res = DirtRoom + "Data/Cam2.txt"
windowName = 'Result'
# Rofl = MyDirectory + "Dungeon.jpg"
# ResultPict, windowName = Rofl, Rofl[Rofl.rfind('/') + 1:Rofl.rfind('.')]

if __name__ == "__main__":
    width = int(DoublePict.shape[1])
    height = int(DoublePict.shape[0])
    # width, height = 300, 300

    Cam1 = DoublePict[0:height, 0:(int)(width / 2)].copy()
    Cam2 = DoublePict[0:height, (int)(width / 2):width].copy()
    cv2.imwrite(Cam1Pict, Cam1)
    cv2.imwrite(Cam2Pict, Cam2)

    subprocess.call(DirtRoom + "darknet.sh", shell=True)
    ipt, ndel, nmap, v, t = [], [], [], [], 0
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
        if p > Accuracy:
            v.append([name, p, x, y, w, h])

    dl = len(v)
    for i in range(dl - 1):
        for j in range(dl - i - 1):
            if v[j] > v[j+1]:
                v[j], v[j+1] = v[j+1], v[j]
    while t < dl:
        tl = 0
        while (t + tl) < dl and v[t][0] == v[t + tl][0]:
            tl = tl + 1
        t = t + tl
        nmap.append(tl)

    i1, i2 = 0, 0
    for tmp in nmap:
        i2 = i2 + tmp
        for i in range(i1, i2):
            for j in range(i1, i2 - 1):
                if v[j][5] + v[j][4] < v[j + 1][5] + v[j + 1][4]:
                    v[j], v[j + 1] = v[j + 1], v[j]
        i1 = i2

    tmp1, tmp2, DiffComp = 0, 0, 15
    for i in range(0, len(v)):
        tf = 1
        if i < len(v) - 1:
            tmp1 = v[i][2] - v[i + 1][2]
            if tmp1 < DiffComp and tmp1 > -1 * DiffComp:
                tf = 0
        if i > 0:
            tmp2 = v[i][2] - v[i - 1][2]
            if tmp2 < DiffComp and tmp2 > -1 * DiffComp:
                tf = 0
        if tf == 1:
            ndel.append(i)

    for i in range(len(ndel)-1, -1, -1):
        tmp = (int)(ndel[i])
        v.pop(tmp)

    for i in range(0, len(v)):
        # print(v[i][0], " ", v[i][1], " ", v[i][2], " ", v[i][3], " ", v[i][4], " ", v[i][5])
        pass

    # Start building a space map

    Red = (89, 16, 222)
    Green = (0, 179, 44)
    Blue = (222, 131, 49)
    Yellow = (0, 211, 255)
    White = (255, 255, 255)
    Salmon = (140, 105, 255)
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
    # print("\nInput Picture\n  width: ", width, "height: ", height, '\n')

    polew, poleh = 36, 36
    axisColor = Black

    img = cv2.resize(img, (width + polew, height + poleh), interpolation=cv2.INTER_AREA)
    cv2.rectangle(img, (0, 0), (width + polew, height + poleh), White, -1)
    cv2.rectangle(img, (polew, 0), (polew + width - 2, height), Red, 4)

    cv2.line(img, (polew, 0), ((int)(polew / 2), (int)(polew / 2)), axisColor, 3)
    cv2.line(img, (polew, 0), ((int)(polew / 2 + polew), (int)(polew / 2)), axisColor, 3)
    cv2.line(img, (polew, 0), (polew, height), axisColor, 3)

    cv2.line(img, (polew + width, height), (width + (int)(polew / 2), height - (int)(poleh / 2)), axisColor, 3)
    cv2.line(img, (polew + width, height), (width + (int)(polew / 2), height + (int)(poleh / 2)), axisColor, 3)
    cv2.line(img, (polew, height), (polew + width, height), axisColor, 3)

    cv2.putText(img, '(0,0)', (7, height + (int)(poleh / 2 - 1)), font, fontScale, Black, 2)

    AxisDivision = 50
    ArrowOfDeath = 0
    for i in range(AxisDivision, height, AxisDivision):
        if i > height - 30:
            break
        cv2.line(img, (polew - 6, height - i), (polew + 6, height - i), Black, 2)
        cv2.putText(img, (str)(i / 100), (0, height - i - 5), font, fontScale, Black, 2)

    for i in range(AxisDivision, width, AxisDivision):
        if i > width - 30:
            break
        ArrowOfDeath = ArrowOfDeath + 0.25
        cv2.line(img, (polew + i, height + 6), (polew + i, height - 6), Black, 2)
        # cv2.putText(img, (str)(ArrowOfDeath), (i + polew - 15, (int)(height + poleh / 2)), font, fontScale, Black, 2)

    ObjWColor, i3, LineDown, ArrowHeight = Yellow, 0, 2, 4
    TxTQue1, TxTQue2, TxTQue3 = [], [], []
    for i in range(0, len(v), 2):
        x1 = v[i][2] + v[i][4] / 2
        x2 = v[i + 1][2] + v[i + 1][4] / 2
        x1x2 = abs(x2 - x1)
        if x1x2 == 0:
            x1x2 = 1
        DistObj = LenTmp / x1x2
        DistObj = (int)(DistObj * ScaleLen)

        first = (int)((v[i][2] + v[i + 1][2]) / 2) + polew
        second = (int)((v[i][2] + v[i + 1][2] + v[i][4] + v[i + 1][4]) / 2) + polew

        ObjWidth = (2 * abs(first - second)) / PxHor * math.tan(CamAngle / 2)
        ObjWidth = (int)(ObjWidth * 1000) / 100
        # print(v[i][0], ObjWidth, 'meters')

        Dheight = height - DistObj
        TopTrianglePos = ((first + second) // 2, Dheight - 100 + abs(first - second)//3)

        cv2.line(img, (first, Dheight), (second, Dheight), LineColor, LineType)
        cv2.line(img, (first, Dheight), TopTrianglePos, LineColor, LineType)
        cv2.line(img, (second, Dheight), TopTrianglePos, LineColor, LineType)

        cv2.line(img, (first, Dheight + LineDown), (first + ArrowHeight, Dheight + LineDown - ArrowHeight), ObjWColor,2)
        cv2.line(img, (first, Dheight + LineDown), (first + ArrowHeight, Dheight + LineDown + ArrowHeight),  ObjWColor,2)

        cv2.line(img, (second, Dheight + LineDown), (second - ArrowHeight, Dheight + LineDown + ArrowHeight), ObjWColor,2)
        cv2.line(img, (second, Dheight + LineDown), (second - ArrowHeight, Dheight + LineDown - ArrowHeight), ObjWColor,2)
        cv2.line(img, (first, Dheight + LineDown), (second, Dheight + LineDown), ObjWColor, 2)

        TxTQue1.append(str(name + " " + str(ObjWidth) + "m"))
        TxTQue2.append(first)
        TxTQue3.append(height - DistObj + 10)
        # cv2.putText(img, str(name + " " + str(ObjWidth) + "m"), (first, height - DistObj + 10), font, fontScale, fontColor, fontType)

    for i in range(0, len(TxTQue1)):
        cv2.putText(img, TxTQue1[i], ((int)(TxTQue2[i]), (int)(TxTQue3[i])), font, fontScale, fontColor, fontType)
        pass

    ColorOfArrow = Salmon
    cv2.putText(img, 'y(m)', (0, 22), 2, 1, ColorOfArrow, 2)
    cv2.putText(img, 'x(m)', (width - polew - 4, poleh + height-10), 2, 1, ColorOfArrow, 2)

    while (True):
        cv2.imshow(windowName, img)
        a = cv2.waitKey(0)
        if a == ord('a'):
            print("\nPressed A --> Saved --> Break")
            cv2.imwrite(ResultPict, img)
            cv2.destroyAllWindows()
            break

        if a == ord('q'):
            print("\nPressed Q --> Break")
            cv2.destroyAllWindows()
            break

        if a == ord('z'):
            print("\nPressed Z --> Clear")
            cv2.rectangle(img, (0, 0), (width + polew + 10, height + poleh + 10), White, -1)

    cv2.imwrite("Results.jpg", img)
