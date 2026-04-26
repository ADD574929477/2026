#!/usr/bin/env python3
import os
import sys
import csv
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class CSVMerger:
    def __init__(self, input_files, output_file, delimiter=',', encoding='utf-8'):
        self.input_files = input_files
        self.output_file = output_file
        self.delimiter = delimiter
        self.encoding = encoding
        self.results = {
            'files_processed': 0,
            'total_rows': 0,
            'errors': [],
            'warnings': []
        }
    
    def check_csv_file(self, file_path):
        """检查CSV文件的有效性"""
        try:
            with open(file_path, 'r', encoding=self.encoding, newline='') as f:
                reader = csv.reader(f, delimiter=self.delimiter, quotechar='"')
                header = next(reader, None)
                if not header:
                    self.results['warnings'].append(f"文件 {file_path} 没有标题行")
                    return False, None
                
                header = [h.strip() for h in header]
                row_count = 0
                for row in reader:
                    row_count += 1
                
                return True, header
        except Exception as e:
            self.results['errors'].append(f"文件 {file_path} 读取错误: {str(e)}")
            return False, None
    
    def merge_files(self):
        """合并多个CSV文件"""
        if not self.input_files:
            return False, "错误: 没有提供输入文件"
        
        headers = []
        valid_files = []
        
        for file_path in self.input_files:
            if not os.path.exists(file_path):
                self.results['errors'].append(f"文件 {file_path} 不存在")
                continue
            
            is_valid, header = self.check_csv_file(file_path)
            if is_valid:
                headers.append(header)
                valid_files.append(file_path)
        
        if not valid_files:
            return False, "错误: 没有有效的CSV文件可以处理"
        
        first_header = headers[0]
        header_length = len(first_header)
        
        for i, header in enumerate(headers[1:], 1):
            if header != first_header:
                self.results['warnings'].append(f"文件 {valid_files[i]} 的标题行与第一个文件不一致")
        
        try:
            with open(self.output_file, 'w', encoding=self.encoding, newline='') as outfile:
                writer = csv.writer(outfile, delimiter=self.delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(first_header)
                
                for file_path in valid_files:
                    with open(file_path, 'r', encoding=self.encoding, newline='') as infile:
                        lines = infile.readlines()
                        for line in lines[1:]:
                            line = line.strip()
                            if not line:
                                continue
                            
                            cells = []
                            current_cell = []
                            in_quote = False
                            
                            for char in line:
                                if char == '"':
                                    in_quote = not in_quote
                                elif char == self.delimiter and not in_quote:
                                    cell_content = ''.join(current_cell).strip()
                                    if cell_content.startswith('"') and cell_content.endswith('"'):
                                        cell_content = cell_content[1:-1]
                                    cells.append(cell_content)
                                    current_cell = []
                                else:
                                    current_cell.append(char)
                            
                            if current_cell:
                                cell_content = ''.join(current_cell).strip()
                                if cell_content.startswith('"') and cell_content.endswith('"'):
                                    cell_content = cell_content[1:-1]
                                cells.append(cell_content)
                            
                            if len(cells) < header_length:
                                cells.extend([''] * (header_length - len(cells)))
                            elif len(cells) > header_length:
                                cells = cells[:header_length]
                            
                            writer.writerow(cells)
                            self.results['total_rows'] += 1
                
                self.results['files_processed'] = len(valid_files)
                return True, ""
        except Exception as e:
            self.results['errors'].append(f"合并文件时出错: {str(e)}")
            return False, f"合并文件时出错: {str(e)}"
    
    def generate_report(self):
        """生成处理报告"""
        report = []
        report.append("===== CSV文件处理报告 =====")
        report.append(f"处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"处理文件数: {self.results['files_processed']}")
        report.append(f"总数据行数: {self.results['total_rows']}")
        report.append(f"输出文件: {self.output_file}")
        
        if self.results['warnings']:
            report.append("\n警告:")
            for warning in self.results['warnings']:
                report.append(f"- {warning}")
        
        if self.results['errors']:
            report.append("\n错误:")
            for error in self.results['errors']:
                report.append(f"- {error}")
        
        report.append("=====================")
        return '\n'.join(report)

class CSVMergerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV文件合并工具")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        self.input_files = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 输入文件部分
        input_frame = ttk.LabelFrame(main_frame, text="输入文件", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        self.input_listbox = tk.Listbox(input_frame, height=10, width=80)
        self.input_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        input_buttons_frame = ttk.Frame(input_frame)
        input_buttons_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Button(input_buttons_frame, text="添加文件", command=self.add_files).pack(fill=tk.X, pady=5)
        ttk.Button(input_buttons_frame, text="移除文件", command=self.remove_file).pack(fill=tk.X, pady=5)
        ttk.Button(input_buttons_frame, text="清空列表", command=self.clear_files).pack(fill=tk.X, pady=5)
        
        # 输出文件部分
        output_frame = ttk.LabelFrame(main_frame, text="输出文件", padding="10")
        output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(output_frame, text="输出路径:").pack(side=tk.LEFT, padx=5)
        
        self.output_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_var, width=60).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ttk.Button(output_frame, text="选择", command=self.select_output).pack(side=tk.RIGHT, padx=5)
        
        # 参数设置部分
        params_frame = ttk.LabelFrame(main_frame, text="参数设置", padding="10")
        params_frame.pack(fill=tk.X, pady=5)
        
        # 分隔符设置
        delimiter_frame = ttk.Frame(params_frame)
        delimiter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(delimiter_frame, text="分隔符:").pack(side=tk.LEFT, padx=5)
        
        self.delimiter_var = tk.StringVar(value=",")
        delimiter_options = [(", 逗号", ","), ("; 分号", ";"), ("\t 制表符", "\t"), ("| 竖线", "|")]
        
        for text, value in delimiter_options:
            ttk.Radiobutton(delimiter_frame, text=text, variable=self.delimiter_var, value=value).pack(side=tk.LEFT, padx=10)
        
        # 编码设置
        encoding_frame = ttk.Frame(params_frame)
        encoding_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(encoding_frame, text="编码:").pack(side=tk.LEFT, padx=5)
        
        self.encoding_var = tk.StringVar(value="utf-8")
        encoding_options = ["utf-8", "gbk", "gb2312", "utf-16"]
        
        encoding_combo = ttk.Combobox(encoding_frame, textvariable=self.encoding_var, values=encoding_options, width=10)
        encoding_combo.pack(side=tk.LEFT, padx=5)
        
        # 操作按钮部分
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(buttons_frame, text="合并文件", command=self.merge_files, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="退出", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        
        # 结果显示部分
        result_frame = ttk.LabelFrame(main_frame, text="处理结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.result_text = tk.Text(result_frame, height=10, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.result_text, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        # 配置样式
        style = ttk.Style()
        style.configure("Accent.TButton", foreground="white", background="#0078d7")
    
    def add_files(self):
        files = filedialog.askopenfilenames(title="选择CSV文件", filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")])
        if files:
            for file in files:
                if file not in self.input_files:
                    self.input_files.append(file)
                    self.input_listbox.insert(tk.END, file)
    
    def remove_file(self):
        selected_indices = self.input_listbox.curselection()
        if selected_indices:
            for index in reversed(selected_indices):
                self.input_files.pop(index)
                self.input_listbox.delete(index)
    
    def clear_files(self):
        self.input_files.clear()
        self.input_listbox.delete(0, tk.END)
    
    def select_output(self):
        file = filedialog.asksaveasfilename(title="保存输出文件", defaultextension=".csv", filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")])
        if file:
            self.output_var.set(file)
    
    def merge_files(self):
        if not self.input_files:
            messagebox.showerror("错误", "请添加至少一个输入文件")
            return
        
        output_file = self.output_var.get()
        if not output_file:
            messagebox.showerror("错误", "请选择输出文件路径")
            return
        
        delimiter = self.delimiter_var.get()
        encoding = self.encoding_var.get()
        
        # 显示处理中
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "正在处理...\n")
        self.root.update()
        
        # 执行合并
        merger = CSVMerger(
            input_files=self.input_files,
            output_file=output_file,
            delimiter=delimiter,
            encoding=encoding
        )
        
        success, error_msg = merger.merge_files()
        report = merger.generate_report()
        
        # 显示结果
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, report)
        
        if success:
            messagebox.showinfo("成功", "文件合并成功！")
        else:
            messagebox.showerror("错误", error_msg)

if __name__ == '__main__':
    root = tk.Tk()
    app = CSVMergerGUI(root)
    root.mainloop()