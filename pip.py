import cv2
import tkinter as tk
from PIL import Image, ImageTk
import time
import numpy as np
from tkinter import Tk, Text, Button, Frame, Scrollbar, Label, END, messagebox, filedialog,Canvas
import os
# Biến toàn cục
cap = None
red_count = 0
orange_count = 0
yellow_count = 0
green_count = 0
blue_count = 0
purple_count = 0
none_count = 0
last_count_time = 0  # Lưu thời điểm lần đếm cuối

# Hàm phân loại màu sắc
def classify_color(hue, saturation, value):  # màu sắc, độ bão hòa, độ sáng
    if saturation < 50 or value < 50:
        return None
    if hue < 10 or hue > 170:
        return "Red"
    elif hue < 30:
        return "Orange"
    elif hue < 85:
        return "Yellow"
    elif hue < 170:
        return "Green"
    elif hue < 250:
        return "Blue"
    elif hue < 320:
        return "Purple"
    else:
        return "Red"

# Hàm phát hiện chuyển động và màu
def detect_motion_and_colors():
    global cap, red_count, orange_count, yellow_count, green_count, blue_count, purple_count, none_count, last_count_time

    ret, frame = cap.read()
    if not ret:
        return

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Vẽ ô trung tâm
    height, width, _ = frame.shape
    center_x, center_y = width // 2, height // 2
    box_size = 100
    top_left = (center_x - box_size // 2, center_y - box_size // 2)
    bottom_right = (center_x + box_size // 2, center_y + box_size // 2)
    cv2.rectangle(frame, top_left, bottom_right, (0, 0, 0), 2)

    # Chỉ đếm màu sau mỗi 1 giây
    current_time = time.time()
    if current_time - last_count_time >= 1:  # Chỉ đếm mỗi giây
        last_count_time = current_time

        # Tính toán màu trung bình trong vùng chọn
        roi = hsv_frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        avg_hue = roi[:, :, 0].mean()
        avg_saturation = roi[:, :, 1].mean()
        avg_value = roi[:, :, 2].mean()

        # Phân loại màu
        color = classify_color(avg_hue, avg_saturation, avg_value)
        if color == "Red":
            red_count += 1
        elif color == "Orange":
            orange_count += 1
        elif color == "Yellow":
            yellow_count += 1
        elif color == "Green":
            green_count += 1
        elif color == "Blue":
            blue_count += 1
        elif color == "Purple":
            purple_count += 1
        else:
            none_count += 1

        # Cập nhật giao diện
        label_red_count.config(text=f"{red_count}")
        label_orange_count.config(text=f"{orange_count}")
        label_yellow_count.config(text=f"{yellow_count}")
        label_green_count.config(text=f"{green_count}")
        label_blue_count.config(text=f"{blue_count}")
        label_purple_count.config(text=f"{purple_count}")
        label_none_count.config(text=f"{none_count}")

    # Hiển thị hình ảnh trên giao diện
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    # Giảm kích thước khung hình (giữ 80% kích thước gốc)
    resize_ratio = 0.8
    new_width = int(width * resize_ratio)
    new_height = int(height * resize_ratio)
    resized_frame = cv2.resize(cv2image, (new_width, new_height))


    # Chuyển đổi khung hình để hiển thị trong giao diện Tkinter
    img = Image.fromarray(resized_frame)
    imgtk = ImageTk.PhotoImage(image=img)
    panel.imgtk = imgtk
    panel.config(image=imgtk)


    # Lặp lại hàm sau 10ms để camera hiển thị liên tục
    if cap.isOpened():
        window.after(10, detect_motion_and_colors)


# Nút bắt đầu
def start_detection():
    global cap, red_count, green_count, orange_count, blue_count, purple_count, yellow_count, none_count
    red_count = 0
    green_count = 0
    orange_count = 0
    blue_count = 0
    purple_count = 0
    yellow_count = 0
    none_count = 0


    label_red_count.config(text="0")
    label_green_count.config(text="0")
    label_orange_count.config(text="0")
    label_blue_count.config(text="0")
    label_purple_count.config(text="0")
    label_yellow_count.config(text="0")
    label_none_count.config(text="0")


    cap = cv2.VideoCapture(0)
    start_button.pack_forget()
    label_results.pack_forget()
    panel.pack(padx=10, pady=10)
    end_button.pack(pady=10)
    detect_motion_and_colors()
# Nút kết thúc
def stop_detection():
    global cap
    if cap.isOpened():
        cap.release()
    panel.pack_forget()
    end_button.pack_forget()
    label_results.config(
        text=f"Final Results:\n\nRed: {red_count}\nGreen: {green_count}\nOrange: {orange_count}\nBlue: {blue_count}\nPurple: {purple_count}\nYellow: {yellow_count}\nNone: {none_count}"
    )
    label_results.pack(pady=20)
    start_button.pack(pady=30)
#Nút scan ảnh
def scan_image():
    # Chọn ảnh từ máy tính
    history_list = []
    file_path = filedialog.askopenfilename(
        title="Chọn hình ảnh",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    if not file_path:
        return
    # Đọc ảnh bằng OpenCV
    image = cv2.imread(file_path)
    if image is None:
        messagebox.showerror("Error", "Không thể đọc ảnh.")
        return

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


    # Làm mờ ảnh để phát hiện hình tròn tốt hơn
    blurred_image = cv2.GaussianBlur(hsv_image, (15, 15), 0)


    # Chuyển đổi ảnh HSV sang ảnh grayscale trước khi sử dụng HoughCircles
    gray_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2GRAY)


    # Phát hiện hình tròn mà không giới hạn kích thước
    circles = cv2.HoughCircles(
        gray_image,   # Sử dụng ảnh grayscale
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=50,
        param1=100,
        param2=30,
        minRadius=30,  # Kích thước tối thiểu của quả, có thể điều chỉnh hoặc bỏ qua
        maxRadius=0    # Không giới hạn kích thước quả
    )


    color_count = {}


    start_time = time.time()
    # Nếu phát hiện hình tròn
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")


        # Lặp qua tất cả các quả phát hiện
        for (x, y, r) in circles:
            # Tính toán vị trí và kích thước của hình vuông bao quanh quả
            side_length = r * 2  # Kích thước cạnh của hình vuông là gấp đôi bán kính
            x1, y1 = x - r, y - r
            x2, y2 = x + r, y + r


            # Đảm bảo hình vuông không nhỏ hơn kích thước quả
            side_length = max(side_length, r * 2)  # Đảm bảo cạnh hình vuông ít nhất là bằng kích thước quả


            # Tính lại toạ độ của hình vuông
            x1, y1 = max(x - r, 0), max(y - r, 0)  # Đảm bảo tọa độ không ra ngoài biên ảnh
            x2, y2 = min(x + r, image.shape[1]), min(y + r, image.shape[0])


            # Vẽ khung hình vuông (rectangle) bao quanh quả
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 4)

            # Lấy giá trị HSV tại tâm của quả
            center_x = x
            center_y = y

            # Lấy giá trị HSV tại điểm trung tâm
            center_hue, center_saturation, center_value = hsv_image[center_y, center_x]

            # Phân loại màu
            color = classify_color(center_hue, center_saturation, center_value)
            color_text = color if color else "Unknown"

            if color_text in color_count:
                color_count[color_text] += 1
            else:
                color_count[color_text] = 1

            # Xác định màu chữ (đảm bảo chữ nổi bật trên nền của quả)
            if color == "Green" or color == "Orange":  # Chữ sáng trên quả màu tối
                text_color = (0, 0, 0)  # Màu chữ đen
            else:
                text_color = (255, 255, 255)  # Màu chữ trắng

            # Vẽ chữ vào ô vuông trong quả
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_size = cv2.getTextSize(color_text, font, 0.6, 2)[0]
            text_x = x - text_size[0] // 2
            text_y = y + text_size[1] // 2
            cv2.putText(image, color_text, (text_x, text_y), font, 0.6, text_color, 2, cv2.LINE_AA)


        end_time = time.time()
        scan_duration = end_time - start_time


        history_entry = {
            "Image": file_path,
            "Colors": color_count,
            "Scan Duration": scan_duration
        }
        history_list.append(history_entry)


        # Hiển thị kết quả
        result_text = "Quả đã được phát hiện và ghi chữ!"
        messagebox.showinfo("Kết quả quét ảnh", result_text)


        # Hiển thị ảnh đã ghi chữ
        cv2.imshow("Result", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


        # Lưu ảnh kết quả ra file history.txt mà không có ký tự xuống dòng giữa các mục.
        with open("history.txt", "a") as file:
            for entry in history_list:
                file.write(f"Image: {entry['Image']}\n")  # Xuống dòng sau khi ghi thông tin hình ảnh
                for color, count in entry["Colors"].items():
                    file.write(f"{color}: {count}\n")  # Xuống dòng sau mỗi màu
                file.write(f"Scan Duration: {entry['Scan Duration']} seconds\n")  # Xuống dòng sau thời gian quét
                file.write("\n")  # Thêm dòng trống giữa các mục
                
                
#Nút lịch sử
def show_history():
    def delete_entry(frame, entry_index):
        """Xóa mục khỏi giao diện và file."""
        frame.destroy()  # Xóa mục khỏi giao diện
        history_data.pop(entry_index)  # Xóa mục khỏi danh sách lịch sử
        save_history_to_file(history_data)  # Cập nhật lại file lịch sử


    def save_history_to_file(data):
        """Ghi lại danh sách lịch sử vào file."""
        with open("history.txt", "w") as file:
            for entry in data:
                file.write(f"Image: {entry['Image']}\n")
                for color, count in entry["Colors"].items():
                    file.write(f"{color}: {count}\n")
                file.write(f"Scan Duration: {entry['Scan Duration']:.6f} seconds\n\n")
    try:
        # Đọc dữ liệu từ file history.txt
        with open("history.txt", "r") as file:
            raw_data = file.read()
        # Phân tích dữ liệu từ file
        history_entries = raw_data.strip().split("\n\n")
        history_data = []
        for entry in history_entries:
            if entry.strip():
                lines = entry.strip().split("\n")
                image_path = lines[0].split(": ")[1]
                colors = {}
                scan_duration = 0.0
                for line in lines[1:]:
                    if "Scan Duration" in line:
                        scan_duration = float(line.split(": ")[1].replace(" seconds", ""))
                    elif ":" in line:
                        color, count = line.split(": ")
                        colors[color] = int(count)
                history_data.append({
                    "Image": image_path,
                    "Colors": colors,
                    "Scan Duration": scan_duration
                })
        # Tạo cửa sổ hiển thị lịch sử
        history_window = Tk()
        history_window.title("Lịch sử quét ảnh")
        history_window.geometry("600x400")


        scrollbar = Scrollbar(history_window)
        scrollbar.pack(side="right", fill="y")


        canvas = Canvas(history_window, yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)


        scrollbar.config(command=canvas.yview)
        inner_frame = Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner_frame.bind("<Configure>", on_frame_configure)
        # Thêm từng mục lịch sử vào giao diện
        for idx, entry in enumerate(history_data):
            entry_frame = Frame(inner_frame, bd=2, relief="groove", padx=5, pady=5, bg="white")
            entry_frame.pack(fill="x", pady=5, padx=5)
            # Nút xóa
            delete_button = Button(entry_frame, text="X", fg="red", command=lambda idx=idx, frame=entry_frame: delete_entry(frame, idx))
            delete_button.pack(side="top", anchor="nw")
            # Thông tin chi tiết
            Label(entry_frame, text=f"Image: {entry['Image']}", bg="white", anchor="w").pack(fill="x")
            Label(entry_frame, text="Colors:", bg="white", anchor="w").pack(fill="x")
            for color, count in entry["Colors"].items():
                Label(entry_frame, text=f"- {color}: {count}", bg="white", anchor="w").pack(fill="x")
            Label(entry_frame, text=f"Scan Duration: {entry['Scan Duration']:.6f} seconds", bg="white", anchor="w").pack(fill="x")
        history_window.mainloop()
    except FileNotFoundError:
        messagebox.showerror("Error", "Không tìm thấy file lịch sử.")
# Tạo giao diện Tkinter
window = tk.Tk()
window.title("Color Detection System")
window.configure(bg="#2c3e50")
window.geometry("800x700")
# Header
header = tk.Label(
    window,
    text="Color Detection System",
    font=("Helvetica", 30, "bold"),
    bg="#1abc9c",
    fg="white",
    pady=10,
)
header.pack(fill=tk.X)
# Khu vực hiển thị đếm màu
counter_frame = tk.Frame(window, bg="#34495e", pady=20)
counter_frame.pack(fill=tk.X)
# Red
label_red = tk.Label(
    counter_frame, text="Red", font=("Helvetica", 18), fg="red", bg="#34495e"
)
label_red.grid(row=0, column=0, padx=20)
label_red_count = tk.Label(
    counter_frame, text="0", font=("Helvetica", 18, "bold"), fg="red", bg="#34495e"
)
label_red_count.grid(row=1, column=0)
# Orange
label_orange = tk.Label(
    counter_frame, text="Orange", font=("Helvetica", 18), fg="orange", bg="#34495e"
)
label_orange.grid(row=0, column=1, padx=20)
label_orange_count = tk.Label(
    counter_frame, text="0", font=("Helvetica", 18, "bold"), fg="orange", bg="#34495e"
)
label_orange_count.grid(row=1, column=1)


# Yellow
label_yellow = tk.Label(
    counter_frame, text="Yellow", font=("Helvetica", 18), fg="yellow", bg="#34495e"
)
label_yellow.grid(row=0, column=2, padx=20)
label_yellow_count = tk.Label(
    counter_frame, text="0", font=("Helvetica", 18, "bold"), fg="yellow", bg="#34495e"
)
label_yellow_count.grid(row=1, column=2)


# Green
label_green = tk.Label(
    counter_frame, text="Green", font=("Helvetica", 18), fg="green", bg="#34495e"
)
label_green.grid(row=0, column=3, padx=20)
label_green_count = tk.Label(
    counter_frame, text="0", font=("Helvetica", 18, "bold"), fg="green", bg="#34495e"
)
label_green_count.grid(row=1, column=3)


# Blue
label_blue = tk.Label(
    counter_frame, text="Blue", font=("Helvetica", 18), fg="blue", bg="#34495e"
)
label_blue.grid(row=0, column=4, padx=20)
label_blue_count = tk.Label(
    counter_frame, text="0", font=("Helvetica", 18, "bold"), fg="blue", bg="#34495e"
)
label_blue_count.grid(row=1, column=4)


# Purple
label_purple = tk.Label(
    counter_frame, text="Purple", font=("Helvetica", 18), fg="purple", bg="#34495e"
)
label_purple.grid(row=0, column=5, padx=20)
label_purple_count = tk.Label(
    counter_frame, text="0", font=("Helvetica", 18, "bold"), fg="purple", bg="#34495e"
)
label_purple_count.grid(row=1, column=5)


# None
label_none = tk.Label(
    counter_frame, text="None", font=("Helvetica", 18), fg="white", bg="#34495e"
)
label_none.grid(row=0, column=6, padx=20)
label_none_count = tk.Label(
    counter_frame, text="0", font=("Helvetica", 18, "bold"), fg="white", bg="#34495e"
)
label_none_count.grid(row=1, column=6)
# Nút bắt đầu
start_button = tk.Button(
    window,
    text="Start Detection",
    font=("Helvetica", 18, "bold"),
    bg="#2ecc71",
    fg="white",
    command=start_detection,
    pady=10,
    padx=20,
)
start_button.pack(pady=30)


# Nút kết thúc
end_button = tk.Button(
    window,
    text="Stop Detection",
    font=("Helvetica", 18, "bold"),
    bg="#e74c3c",
    fg="white",
    command=stop_detection,
    pady=10,
    padx=20,
)
end_button.pack(pady=30)
# Nút quét ảnh
scan_button = tk.Button(
    window,
    text="Scan Image",
    font=("Helvetica", 18, "bold"),
    bg="#f39c12",
    fg="white",
    command=scan_image,
    pady=10,
    padx=20,
)
scan_button.pack(pady=20)
#Nút lịch sử
history_button = tk.Button(
    window,
    text="History",
    font=("Helvetica", 18, "bold"),
    bg="#e74c3c",  # Màu đỏ
    fg="white",
    command=show_history,
    pady=10,
    padx=20,
)
history_button.pack(pady=30)

# Nhãn kết quả
label_results = tk.Label(window, font=("Helvetica", 18, "bold"), bg="#34495e", fg="white")


# Khung hình hiển thị webcam
panel = tk.Label(window)
panel.pack(padx=10, pady=10)


# Chạy giao diện Tkinter
window.mainloop()
