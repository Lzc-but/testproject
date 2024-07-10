import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit


# 计算斜率
def calculate_slope(x, y):
    slopes = []
    for i in range(1, len(x)):
        dx = x[i] - x[i - 1]
        dy = y[i] - y[i - 1]
        slope = dy / dx if dx != 0 else float("inf")  # 处理斜率无穷大的情况
        slopes.append(slope)
    slopes.insert(0, 0)  # 初始点斜率为0
    return slopes


# 定义sigmoid函数
def sigmoid(x, L, x0, k):
    """
    Parameters
    ----------
    x : array-like
        Independent variable.
    L : float
        Maximum value of the sigmoid function.
    x0 : float
        Midpoint of the sigmoid function.
    k : float
        Steepness of the sigmoid function.

    Returns
    -------
    array-like
        Sigmoid function evaluated at `x`.
    """
    return L / (1 + np.exp(-k * (x - x0)))


def getperthreshold(filename1, filename2, filename3):
    # 读取第一个 CSV 文件的纵坐标
    df1 = pd.read_csv(filename1)
    x = df1.iloc[:, 0]
    y1 = df1.iloc[:, 1]  # 假设第二列是纵坐标
    slopes1 = calculate_slope(x, y1)
    max_index1 = slopes1.index(max(slopes1))

    # 读取第二个 CSV 文件的纵坐标
    df2 = pd.read_csv(filename2)
    y2 = df2.iloc[:, 1]
    slopes2 = calculate_slope(x, y2)
    max_index2 = slopes2.index(max(slopes2))
    # 读取第三个 CSV 文件的纵坐标
    df3 = pd.read_csv(filename3)
    y3 = df3.iloc[:, 1]
    slopes3 = calculate_slope(x, y3)
    max_index3 = slopes3.index(max(slopes3))
    # 设置中文字体为SimHei
    plt.rcParams["font.family"] = "SimHei"

    # plt.plot(x, y1, label="size5*5*5")
    plt.plot(x, slopes1, label="size8*8*8")
    plt.plot(x, slopes2, label="size16*16*16")
    plt.plot(x, slopes3, label="size32*32*32")
    # # 设置标签字体大小为14
    plt.legend(fontsize=16)

    plt.scatter(
        x[max_index1], slopes1[max_index1], color="red", s=50
    )  # 在最大值点上绘制一个红色的圆点
    plt.scatter(x[max_index2], slopes2[max_index2], color="red", s=50)
    plt.scatter(x[max_index3], slopes3[max_index3], color="red", s=50)
    # 添加标题和图例
    plt.title("不同位点浓度的斜率", fontsize=16)
    plt.xlabel("位点浓度", fontsize=14)
    plt.ylabel("斜率", fontsize=14)
    plt.legend()
    show_max1 = (
        "[" + str(x[max_index1]) + " " + str(round(slopes1[max_index1], 2)) + "]"
    )
    # 第一个参数为标记文本，第二个参数为标记对象的坐标，第三个参数为标记位置
    plt.annotate(
        show_max1,
        xy=(x[max_index1], slopes1[max_index1]),
        xytext=(x[max_index1], slopes1[max_index1]),
    )
    show_max2 = (
        "[" + str(x[max_index2]) + " " + str(round(slopes2[max_index2], 2)) + "]"
    )
    plt.annotate(
        show_max2,
        xy=(x[max_index2], slopes2[max_index2]),
        xytext=(x[max_index2], slopes2[max_index2]),
    )
    show_max3 = (
        "[" + str(x[max_index3]) + " " + str(round(slopes3[max_index3], 2)) + "]"
    )
    plt.annotate(
        show_max3,
        xy=(x[max_index3], slopes3[max_index3]),
        xytext=(x[max_index3], slopes3[max_index3]),
    )
    # 显示图形
    plt.show()
    return 0


def draw_percalotioncurve(filename1, filename2, filename3):
    # 读取第一个 CSV 文件的纵坐标
    df1 = pd.read_csv(filename1)
    x = df1.iloc[:, 0]
    y1 = df1.iloc[:, 1]  # 假设第二列是纵坐标

    # 读取第二个 CSV 文件的纵坐标
    df2 = pd.read_csv(filename2)
    y2 = df2.iloc[:, 1]

    # 读取第三个 CSV 文件的纵坐标
    df3 = pd.read_csv(filename3)
    y3 = df3.iloc[:, 1]

    # 设置中文字体为SimHei
    plt.rcParams["font.family"] = "SimHei"

    # plt.plot(x, y1, label="size5*5*5")
    plt.plot(x, y1, label="size8*8*8")
    plt.plot(x, y2, label="size16*16*16")
    plt.plot(x, y3, label="size32*32*32")
    # # 设置标签字体大小为14
    plt.legend(fontsize=18)

    # 添加标题和图例
    plt.title("在3Dcube格点的100次MC模拟结果", fontsize=16)
    plt.xlabel("位点浓度", fontsize=14)
    plt.ylabel("渗透次数", fontsize=14)
    plt.legend()

    # 显示图形
    plt.show()
    return 0


# draw_percalotioncurve(
#     r"C:\Users\33389\Desktop\materials_ccnb\percolation\cuberesult\cubetestsize888100percolation_result.csv",
#     r"C:\Users\33389\Desktop\materials_ccnb\percolation\cuberesult\cubetestsize161616100percolation_result.csv",
#     r"C:\Users\33389\Desktop\materials_ccnb\percolation\cuberesult\cubetestsize323232100percolation_result.csv",
# )
getperthreshold(
    r"C:\Users\33389\Desktop\materials_ccnb\percolation\cuberesult\cubetestsize888100percolation_result.csv",
    r"C:\Users\33389\Desktop\materials_ccnb\percolation\cuberesult\cubetestsize161616100percolation_result.csv",
    r"C:\Users\33389\Desktop\materials_ccnb\percolation\cuberesult\cubetestsize323232100percolation_result.csv",
)
with open("www.txt", "w") as f:
    f.write("Interstitial table:\tid\tlabel\tfraccoord\tradii\tenergy\n")
print("ss")
