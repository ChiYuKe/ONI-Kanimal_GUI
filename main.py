import tkinter as tk

from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
import subprocess
import platform
import os
import argparse
from tkdnd import TkinterDnD, DND_FILES

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)


    def enter(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(self.tooltip, text=self.text, justify='left', background="#ffffe0", relief='solid', borderwidth=1)
        label.pack(ipadx=1)

    def leave(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()

class KanimalGUI:
    def __init__(self, master):
        self.master = master
        self.selected_files = []

        master.title("Kanimal GUI  V1.0")


        # 在 __init__ 方法中添加如下绑定
        self.master.drop_target_register(DND_FILES)
        self.master.dnd_bind('<<Drop>>', self.drop)

        main_frame = ttk.Frame(master)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        main_frame.pack_propagate(False)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        left_frame.pack_propagate(False)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        right_frame.pack_propagate(False)

        style = ttk.Style()
        style.configure("TLabel", padding=6, font=('Microsoft YaHei', 12))
        style.configure("TButton", padding=6, font=('Microsoft YaHei', 12))

        # 使用文本框来显示选择的文件 tk.WORD  tk.NONE
        self.file_text = scrolledtext.ScrolledText(left_frame, wrap=tk.NONE, width=30, height=5, font=('Microsoft YaHei', 10))
        self.file_text.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        self.file_button = ttk.Button(left_frame, text="选择文件", command=self.select_files)
        self.file_button.grid(row=1, column=0, pady=5)
        Tooltip(self.file_button, "选择要处理的文件")

        self.process_button = ttk.Button(left_frame, text="处理文件", command=self.process_files)
        self.process_button.grid(row=1, column=1, columnspan=1, pady=10)


        # # 修改按钮的位置
        # self.output_button = ttk.Button(left_frame, text="...", command=self.select_output_folder)
        # self.output_button.grid(row=4, column=2, pady=5, padx=5)  # 设置 column 为 1，使其位于文本框旁边
        # Tooltip(self.output_button, "若未选择，会使用默认路径")
        #
        # self.output_label = ttk.Label(left_frame, text="输出目录:", anchor="w", justify="left", wraplength=200)
        # self.output_label.grid(row=3, column=0, columnspan=2, pady=10, sticky="w")
        #
        # self.output_entry = ttk.Entry(left_frame)
        # self.output_entry.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

        self.master.drop_target_register(DND_FILES)
        self.master.dnd_bind('<<Drop>>', self.drop)

        self.log_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=40, height=15, font=('Microsoft YaHei', 10))
        self.log_text.pack(pady=10, padx=10)

        main_frame.grid_columnconfigure(1, weight=1)

        # 解析命令行参数
        self.parse_command_line_arguments()

    def parse_command_line_arguments(self):
        parser = argparse.ArgumentParser(description="Kanimal GUI")
        parser.add_argument("files", nargs="*", help="List of files to process")
        parser.add_argument("-o", "--output", help="Output directory")
        args = parser.parse_args()

        # 检查是否有文件作为参数
        if args.files:
            self.selected_files = args.files
            self.update_file_text()

    def update_file_text(self):
        files_text = '\n'.join(self.selected_files)
        self.file_text.delete(1.0, tk.END)
        self.file_text.insert(tk.END, files_text)

    def select_files(self):
        files = filedialog.askopenfilenames(title="选择文件", filetypes=[("All files", "*.*")])
        self.selected_files = list(files)
        self.update_file_text()

    def process_files(self):
        try:
            if not self.selected_files:
                messagebox.showerror("Error", "不放文件进去是想让我处理空气吗")
                return

            # 将.txt文件重命名为.bytes文件
            for file_path in self.selected_files:
                if file_path.lower().endswith(".txt"):
                    new_file_path = file_path[:-4] + ".bytes"
                    os.rename(file_path, new_file_path)

            # 初始化 command 为一个空列表
            command = []

            # 在 Windows 上
            if platform.system() == "Windows":
                scml_files = [file for file in self.selected_files if file.lower().endswith(".scml")]

                if scml_files:
                    command += ["kanimal-cli.exe", "kanim"]
                else:
                    command += ["kanimal-cli.exe", "scml"]

            # 在 Mac/Linux 上
            else:
                scml_files = [file for file in self.selected_files if file.lower().endswith(".scml")]

                if scml_files:
                    command += ["./kanimal-cli", "kanim"]
                else:
                    command += ["./kanimal-cli", "scml"]

            # 将.txt文件修改为.bytes文件
            command += [os.path.normpath(file.replace(".txt", ".bytes")) for file in self.selected_files]

            # 修改为使用 list2cmdline 来构建命令行参数
            command_line = subprocess.list2cmdline(command)

            # 在日志框中显示命令
            self.log_text.insert(tk.END, f"执行命令：{command_line}\n")

            if self.selected_files:
                first_file_name = os.path.basename(self.selected_files[0])
                first_file_name_filtered = first_file_name[:-4]
                command += ["-o", f"output/{first_file_name_filtered}"]

            # 此时 command 包含了所有的元素
            process = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.log_text.insert(tk.END, process.stdout)
            self.log_text.insert(tk.END, process.stderr)
            
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            self.log_text.insert(tk.END, formatted_time)

            self.log_text.insert(tk.END, "文件处理成功\n")
            messagebox.showinfo("Success", "文件处理成功")

            # 清空 selected_files 列表
            self.selected_files = []

            # 在执行完成后自动清除框内的东西
            self.file_text.delete(1.0, tk.END)
        except subprocess.CalledProcessError as e:
            self.log_text.insert(tk.END, f"命令执行时发生错误: {e}\n")
            messagebox.showerror("Error", f"命令执行时发生错误: {e}")
        except Exception as e:
            self.log_text.insert(tk.END, f"处理文件时发生错误: {e}\n")
            messagebox.showerror("Error", f"处理文件时发生错误: {e}")

    def drop(self, event):
        # 获取拖放的数据
        files = event.data

        if isinstance(files, str):
            paths = files.split()

            for path in paths:
                if os.path.isfile(path):
                    self.selected_files.append(path)

            self.update_file_text()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = KanimalGUI(root)
    root.geometry("700x400")
    root.mainloop()
