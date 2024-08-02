import tkinter as tk
from tkinter import ttk
from utils import process_multi_line, beautify_dict, add_up_dan, add_up_zu, collect_v_count_dict_to_count_v_list_dict


def on_button_click():
    input_text = text_input.get("1.0", tk.END)
    processed_dict_dan, processed_dict_zu = process_multi_line(input_text)
    processed_dict_dan = add_up_dan(processed_dict_dan)
    processed_dict_zu = add_up_zu(processed_dict_zu)
    # 转回数组，以便显示
    processed_dict_dan = collect_v_count_dict_to_count_v_list_dict(processed_dict_dan)
    processed_zu_dict = collect_v_count_dict_to_count_v_list_dict(processed_dict_zu)
    processed_text = beautify_dict(processed_dict_dan, '单') + "\n" + "-"*32 + "\n" + beautify_dict(processed_zu_dict, '组')

    text_output.config(state=tk.NORMAL)  # 允许更改文本
    text_output.delete("1.0", tk.END)  # 清除现有文本
    text_output.insert(tk.END, processed_text)  # 插入新文本
    text_output.config(state=tk.DISABLED)  # 禁止更改文本

# 创建主窗口
root = tk.Tk()
root.title("Text Processor")
root.geometry("1400x800")

# 创建框架
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# 定义行列权重
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_rowconfigure(1, weight=0)  # 按钮所在行权重为0

# 创建文本输入框
text_input = tk.Text(frame, wrap="word")
text_input.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5), pady=(0, 10))

# 创建文本显示框
text_output = tk.Text(frame, wrap="word", state=tk.DISABLED)
text_output.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0), pady=(0, 10))

# 创建按钮并绑定事件
button = ttk.Button(frame, text="确定", command=on_button_click)
button.grid(row=1, column=0, columnspan=2, pady=(5, 0))

# 设置窗口关闭时的行为
def on_closing():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# 开始主事件循环
root.mainloop()

# if __name__ == '__main__':
#     """ 基本要求：所有数字与X单Y组之间，使用中/英文[逗号，顿号，句号，空格]分隔，【X单Y组,X单,Y组】只能出现一种、一次"""
#     str_in = """
#     247  237  437  467  343 373  479  459  491  457 267 两单一组
#     837 9单1组
#     123 321 一组
#     128 10单
#     """
#     total_sum = process_multi_line(str_in)
#     print(total_sum)
