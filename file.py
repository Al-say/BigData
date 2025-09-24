import turtle
import math


def draw_nine_oclock():
    # 初始化设置
    screen = turtle.Screen()
    screen.bgcolor("white")
    screen.setup(500, 500)
    screen.title("9点整时钟")

    # 创建绘制对象
    pen = turtle.Turtle()
    pen.speed(0)  # 最快绘制速度
    pen.hideturtle()

    # 绘制钟表外圆
    def draw_outer_circle():
        pen.penup()
        pen.goto(0, -180)  # 外圆半径180
        pen.pendown()
        pen.color("black")
        pen.width(2)
        pen.circle(180)

    # 绘制固定时间的指针（9点整）
    def draw_fixed_hands():
        # 固定时间：9点整
        hours = 9
        minutes = 0

        # 计算指针角度
        minute_angle = math.radians(90)  # 分针指向12点（正上方）
        hour_angle = math.radians(180)  # 时针指向9点（正左方）

        # 绘制分针（红色）
        pen.penup()
        pen.goto(0, 0)
        pen.pendown()
        pen.color("red")  # 分针设置为红色
        pen.width(3)
        pen.goto(120 * math.cos(minute_angle), 120 * math.sin(minute_angle))

        # 绘制时针（黑色）
        pen.penup()
        pen.goto(0, 0)
        pen.pendown()
        pen.color("black")  # 时针保持黑色
        pen.width(5)
        pen.goto(80 * math.cos(hour_angle), 80 * math.sin(hour_angle))

        # 绘制中心点
        pen.penup()
        pen.goto(0, 0)
        pen.dot(8, "black")

    # 绘制时钟
    draw_outer_circle()
    draw_fixed_hands()

    # 保持窗口打开
    turtle.done()


if __name__ == "__main__":
    draw_nine_oclock()
