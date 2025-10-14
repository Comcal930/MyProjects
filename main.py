import tkinter as tk
import requests
import sys
import os
from PIL import Image, ImageTk


# 资源路径处理函数 - 确保打包后也能找到资源文件
def resource_path(relative_path):
    """获取资源文件的绝对路径，适用于开发和PyInstaller打包后环境"""
    try:
        # PyInstaller创建临时文件夹，存储路径在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def on_entry_click(event):
    if entry.get() == placeholder_text:
        entry.delete(0, tk.END)
        entry.config(fg="black")


def on_entry_leave(event):
    if entry.get() == "":
        entry.insert(0, placeholder_text)
        entry.config(fg="grey")


def search_city():
    city = entry.get()
    APIKEY = "3c0e89185e1a2df177dfa9014b3aa85e"
    get_weather(city, APIKEY)


def get_weather(city, api_key):
    base_url = "http://apis.juhe.cn/simpleWeather/query"
    params = {
        "city": city,
        "key": api_key,
        "unit": "metric",
    }
    response = requests.get(base_url, params=params)

    # 先清除Canvas上所有文本
    canvas.delete("weather_text")

    if response.status_code == 200:
        responseResult = response.json()
        city_name = responseResult["result"]["city"]
        current_temp = responseResult["result"]["realtime"]["temperature"]
        current_humidity = responseResult["result"]["realtime"]["humidity"]
        current_weather = responseResult["result"]["realtime"]["info"]
        current_wind = responseResult["result"]["realtime"]["direct"]
        current_aqi = responseResult["result"]["realtime"]["aqi"]
        future_forecasts = responseResult["result"]["future"]

        # 在Canvas上绘制文本
        y_position = 20
        canvas.create_text(10, y_position, text=f"城市: {city_name}", anchor="nw",
                           font=('Arial', 12), tags="weather_text", fill="black")
        y_position += 25
        canvas.create_text(10, y_position, text=f"当前温度: {current_temp}°C", anchor="nw",
                           font=('Arial', 12), tags="weather_text", fill="black")
        y_position += 25
        canvas.create_text(10, y_position, text=f"湿度: {current_humidity}%", anchor="nw",
                           font=('Arial', 12), tags="weather_text", fill="black")
        y_position += 25
        canvas.create_text(10, y_position, text=f"天气状况: {current_weather}", anchor="nw",
                           font=('Arial', 12), tags="weather_text", fill="black")
        y_position += 25
        canvas.create_text(10, y_position, text=f"风向: {current_wind}", anchor="nw",
                           font=('Arial', 12), tags="weather_text", fill="black")
        y_position += 25
        canvas.create_text(10, y_position, text=f"空气质量指数: {current_aqi}", anchor="nw",
                           font=('Arial', 12), tags="weather_text", fill="black")
        y_position += 40
        canvas.create_text(10, y_position, text="未来天气预报:", anchor="nw",
                           font=('Arial', 12, 'bold'), tags="weather_text", fill="black")
        y_position += 25

        for forecast in future_forecasts:
            date = forecast["date"]
            temp = forecast["temperature"]
            weather = forecast["weather"]
            canvas.create_text(10, y_position, text=f"日期: {date}", anchor="nw",
                               font=('Arial', 12), tags="weather_text", fill="black")
            y_position += 25
            canvas.create_text(10, y_position, text=f"温度: {temp}", anchor="nw",
                               font=('Arial', 12), tags="weather_text", fill="black")
            y_position += 25
            canvas.create_text(10, y_position, text=f"天气: {weather}", anchor="nw",
                               font=('Arial', 12), tags="weather_text", fill="black")
            y_position += 25

        # 显式更新滚动区域，使用 "weather_text" 标签来确保只有文本内容可滚动
        canvas.configure(scrollregion=canvas.bbox("all"))
    else:
        canvas.create_text(10, 20, text=f"错误: {response.json().get('reason', '未知错误')}",
                           anchor="nw", font=('Arial', 12), tags="weather_text", fill="red")
        # 显式更新滚动区域
        canvas.configure(scrollregion=canvas.bbox("all"))


root = tk.Tk()
root.title("天气查询小程序")
root.geometry("1024x512")
placeholder_text = "请在此输入想要查询的城市"

# 加载窗口背景图片
window_bg_image = Image.open(r"images\60e9f424384fdc5dcd7f6966d526cdec.jpg")
window_bg_image = window_bg_image.resize((1024, 512), Image.LANCZOS)
window_tk_image = ImageTk.PhotoImage(window_bg_image)

window_bg_label = tk.Label(root, image=window_tk_image)
window_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# 创建Canvas作为文本框
canvas = tk.Canvas(root, width=512, height=255, highlightthickness=0, bd=0)
canvas.place(relx=0.5, rely=0.5, anchor="center")

# 加载文本框背景图片并设置透明度
text_bg_image = Image.open(r"images\e62a0605da1bd5cd75e1559e8717dfd7.jpg")
text_bg_image = text_bg_image.resize((512, 255), Image.LANCZOS)
text_bg_image = text_bg_image.convert("RGBA")

# 设置透明度
alpha = 50
data = text_bg_image.getdata()
new_data = [(item[0], item[1], item[2], alpha) for item in data]
text_bg_image.putdata(new_data)
text_tk_image = ImageTk.PhotoImage(text_bg_image)

# 将背景图片添加到Canvas上，并使用 tags="background" 标签标识
canvas.create_image(0, 0, image=text_tk_image, anchor="nw", tags="background")

# 创建一个框架Frame来用于适应canvas内容的显示
inner_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor="nw")

# 滚动条绑定Canvas文本框
scrollbar = tk.Scrollbar(root, command=canvas.yview)
scrollbar.place(relx=0.74, rely=0.5, anchor="center", height=255)
canvas.configure(yscrollcommand=scrollbar.set)

# 将滚轮事件绑定到canvas
canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

# 当inner_frame的大小发生变化时，更新canvas的滚动区域
inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# entry模块管理
entry_font = ('Arial', 16)
entry = tk.Entry(root, width=25, font=entry_font)
entry.pack(pady=10)
entry.insert(0, placeholder_text)
entry.config(fg="grey")
entry.bind('<FocusIn>', on_entry_click)
entry.bind('<FocusOut>', on_entry_leave)

# Button模块管理
Check_Button = tk.Button(root, text="点击我开始查询天气", command=search_city)
Check_Button.pack(pady=10)

root.mainloop()