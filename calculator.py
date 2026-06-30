#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ماشین حساب پیشرفته - Advanced Calculator
ساخت: برای AnishtayiN
GitHub: https://github.com/AnishtayiN/mashinhesab
"""

import sys
import math
from decimal import Decimal, getcontext
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QLineEdit, QLabel, QComboBox,
    QStackedWidget, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QKeyEvent, QPalette, QColor

# تنظیم دقت محاسبات
getcontext().prec = 20

class CalculatorApp(QMainWindow):
    """کلاس اصلی ماشین حساب"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ماشین حساب پیشرفته")
        self.setWindowIcon(QIcon(":/icon.png"))
        self.setFixedSize(400, 600)
        
        # تنظیم فونت اصلی
        self.font_large = QFont("Segoe UI", 24, QFont.Weight.Bold)
        self.font_medium = QFont("Segoe UI", 18)
        self.font_small = QFont("Segoe UI", 14)
        self.font_history = QFont("Consolas", 12)
        
        # حالت‌ها
        self.modes = ["عادی", "علمی", "برنامه‌نویس", "ماتریس"]
        self.current_mode = "عادی"
        
        # متغیرها
        self.memory = 0
        self.last_result = 0
        self.history = []
        self.current_input = ""
        self.operation = None
        self.first_operand = None
        self.waiting_for_second = False
        self.shift_pressed = False
        self.hyper_pressed = False
        
        # ایجاد رابط کاربری
        self.init_ui()
        
        # تنظیم کیبورد
        self.installEventFilter(self)
    
    def init_ui(self):
        """ایجاد رابط کاربری"""
        # ویجت مرکزی
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # لایه اصلی
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # ایجاد تب‌ها
        self.tab_widget = QStackedWidget()
        
        # ایجاد صفحه‌ها
        self.basic_page = self.create_basic_page()
        self.scientific_page = self.create_scientific_page()
        self.programmer_page = self.create_programmer_page()
        self.matrix_page = self.create_matrix_page()
        
        self.tab_widget.addWidget(self.basic_page)
        self.tab_widget.addWidget(self.scientific_page)
        self.tab_widget.addWidget(self.programmer_page)
        self.tab_widget.addWidget(self.matrix_page)
        
        # نوار وضعیت
        self.status_bar = QLabel("حالت: عادی")
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_bar.setStyleSheet("color: #888;")
        
        # اضافه کردن به لایه اصلی
        main_layout.addWidget(self.create_display())  # نمایشگر
        main_layout.addWidget(self.create_mode_selector())  # انتخاب حالت
        main_layout.addWidget(self.tab_widget)
        main_layout.addWidget(self.status_bar)
        
        # اتصال سیگنال‌ها
        self.update_display()
    
    def create_display(self):
        """ایجاد نمایشگر"""
        display_frame = QFrame()
        display_frame.setFrameShape(QFrame.Shape.StyledPanel)
        display_frame.setStyleSheet("background: #1a1a2e; border-radius: 10px; padding: 15px;")
        
        layout = QVBoxLayout(display_frame)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # نمایشگر اصلی
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFont(self.font_large)
        self.display.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: #00ff88;
                padding: 5px;
            }
        """)
        self.display.setMinimumHeight(60)
        
        # نمایشگر ثانویه (عملیات)
        self.secondary_display = QLabel()
        self.secondary_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.secondary_display.setFont(self.font_small)
        self.secondary_display.setStyleSheet("color: #888;")
        self.secondary_display.setMinimumHeight(20)
        
        layout.addWidget(self.secondary_display)
        layout.addWidget(self.display)
        
        return display_frame
    
    def create_mode_selector(self):
        """ایجاد انتخاب‌کننده حالت"""
        mode_frame = QFrame()
        mode_layout = QHBoxLayout(mode_frame)
        mode_layout.setContentsMargins(5, 5, 5, 5)
        mode_layout.setSpacing(5)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(self.modes)
        self.mode_combo.setCurrentIndex(0)
        self.mode_combo.setFont(self.font_small)
        self.mode_combo.currentIndexChanged.connect(self.change_mode)
        
        # دکمه‌های حافظه
        self.mem_btn = QPushButton("MC")
        self.mem_btn.setFont(self.font_small)
        self.mem_btn.clicked.connect(self.memory_clear)
        
        self.mr_btn = QPushButton("MR")
        self.mr_btn.setFont(self.font_small)
        self.mr_btn.clicked.connect(self.memory_recall)
        
        self.m_plus_btn = QPushButton("M+")
        self.m_plus_btn.setFont(self.font_small)
        self.m_plus_btn.clicked.connect(self.memory_add)
        
        self.m_minus_btn = QPushButton("M-")
        self.m_minus_btn.setFont(self.font_small)
        self.m_minus_btn.clicked.connect(self.memory_subtract)
        
        self.ms_btn = QPushButton("MS")
        self.ms_btn.setFont(self.font_small)
        self.ms_btn.clicked.connect(self.memory_store)
        
        mode_layout.addWidget(QLabel("حالت:"))
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        mode_layout.addWidget(self.mem_btn)
        mode_layout.addWidget(self.mr_btn)
        mode_layout.addWidget(self.m_plus_btn)
        mode_layout.addWidget(self.m_minus_btn)
        mode_layout.addWidget(self.ms_btn)
        
        return mode_frame
    
    def create_basic_page(self):
        """ایجاد صفحه حالت عادی"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # شبکه دکمه‌ها
        grid = QGridLayout()
        grid.setSpacing(10)
        
        # دکمه‌ها
        buttons = [
            ('%', 'mod'), ('√', 'sqrt'), ('x²', 'square'), ('÷', '/'),
            ('CE', 'ce'), ('C', 'c'), ('⌫', 'backspace'), ('×', '*'),
            ('7', '7'), ('8', '8'), ('9', '9'), ('-', '-'),
            ('4', '4'), ('5', '5'), ('6', '6'), ('+', '+'),
            ('1', '1'), ('2', '2'), ('3', '3'),
            ('±', 'negate'), ('0', '0'), ('.', '.'), ('=', 'equal')
        ]
        
        for i, (text, action) in enumerate(buttons):
            row = i // 4
            col = i % 4
            btn = QPushButton(text)
            btn.setFont(self.font_medium)
            btn.setMinimumHeight(60)
            btn.clicked.connect(lambda _, a=action: self.on_button_click(a))
            
            # استایل دکمه‌ها
            if action in ['/', '*', '-', '+', '=']:
                btn.setStyleSheet("background: #ff9500; color: white;")
            elif action in ['ce', 'c', 'backspace']:
                btn.setStyleSheet("background: #ff3b30; color: white;")
            elif action in ['%', 'sqrt', 'square', 'negate']:
                btn.setStyleSheet("background: #a5a5a5; color: black;")
            else:
                btn.setStyleSheet("background: #4a4a4a; color: white;")
            
            # دکمه مساوی بزرگتر باشه
            if action == 'equal':
                btn.setStyleSheet("background: #ff9500; color: white;")
            
            grid.addWidget(btn, row, col)
        
        # دکمه 0 عرض بیشتری داشته باشه
        # اخرین سطر
        zero_btn = grid.itemAtPosition(4, 0).widget()
        zero_btn.setStyleSheet("background: #4a4a4a; color: white;")
        
        layout.addLayout(grid)
        return page
    
    def create_scientific_page(self):
        """ایجاد صفحه حالت علمی"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # شبکه دکمه‌ها
        grid = QGridLayout()
        grid.setSpacing(10)
        
        # دکمه‌ها
        buttons = [
            ('2nd', 'second'), ('x^y', 'power'), ('(', 'paren_open'), (')', 'paren_close'),
            ('sin', 'sin'), ('cos', 'cos'), ('tan', 'tan'), ('π', 'pi'),
            ('log', 'log10'), ('ln', 'ln'), ('e', 'e'), ('!', 'factorial'),
            ('7', '7'), ('8', '8'), ('9', '9'), ('÷', '/'),
            ('4', '4'), ('5', '5'), ('6', '6'), ('×', '*'),
            ('1', '1'), ('2', '2'), ('3', '3'), ('-', '-'),
            ('±', 'negate'), ('0', '0'), ('.', '.'), ('=', 'equal')
        ]
        
        for i, (text, action) in enumerate(buttons):
            row = i // 4
            col = i % 4
            btn = QPushButton(text)
            btn.setFont(self.font_medium)
            btn.setMinimumHeight(60)
            btn.clicked.connect(lambda _, a=action: self.on_button_click(a))
            
            # استایل
            if action in ['/', '*', '-', '+', '=']:
                btn.setStyleSheet("background: #ff9500; color: white;")
            elif action in ['second']:
                btn.setStyleSheet("background: #a5a5a5; color: black;")
            elif action in ['sin', 'cos', 'tan', 'log10', 'ln', 'factorial']:
                btn.setStyleSheet("background: #5c5c5c; color: white;")
            else:
                btn.setStyleSheet("background: #4a4a4a; color: white;")
            
            grid.addWidget(btn, row, col)
        
        layout.addLayout(grid)
        return page
    
    def create_programmer_page(self):
        """ایجاد صفحه حالت برنامه‌نویس"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # نمایشگر‌های باینری، هگز، دسیمال
        hex_frame = QFrame()
        hex_layout = QHBoxLayout(hex_frame)
        hex_layout.setContentsMargins(5, 5, 5, 5)
        hex_layout.setSpacing(5)
        
        self.hex_label = QLabel("HEX: 0")
        self.hex_label.setFont(self.font_small)
        self.hex_label.setStyleSheet("color: #00ff88;")
        
        self.bin_label = QLabel("BIN: 0")
        self.bin_label.setFont(self.font_small)
        self.bin_label.setStyleSheet("color: #00ff88;")
        
        self.dec_label = QLabel("DEC: 0")
        self.dec_label.setFont(self.font_small)
        self.dec_label.setStyleSheet("color: #00ff88;")
        
        hex_layout.addWidget(self.hex_label)
        hex_layout.addStretch()
        hex_layout.addWidget(self.bin_label)
        hex_layout.addStretch()
        hex_layout.addWidget(self.dec_label)
        
        layout.addWidget(hex_frame)
        
        # شبکه دکمه‌ها
        grid = QGridLayout()
        grid.setSpacing(10)
        
        # دکمه‌ها
        buttons = [
            ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),
            ('E', 'E'), ('F', 'F'), ('AND', 'and'), ('OR', 'or'),
            ('XOR', 'xor'), ('NOT', 'not'), ('<<', 'left_shift'), ('>>', 'right_shift'),
            ('7', '7'), ('8', '8'), ('9', '9'), ('÷', '/'),
            ('4', '4'), ('5', '5'), ('6', '6'), ('×', '*'),
            ('1', '1'), ('2', '2'), ('3', '3'), ('-', '-'),
            ('±', 'negate'), ('0', '0'), ('.', '.'), ('=', 'equal')
        ]
        
        for i, (text, action) in enumerate(buttons):
            row = i // 4
            col = i % 4
            btn = QPushButton(text)
            btn.setFont(self.font_medium)
            btn.setMinimumHeight(60)
            btn.clicked.connect(lambda _, a=action: self.on_button_click(a))
            
            # استایل
            if action in ['/', '*', '-', '+', '=']:
                btn.setStyleSheet("background: #ff9500; color: white;")
            elif action in ['A', 'B', 'C', 'D', 'E', 'F']:
                btn.setStyleSheet("background: #5c5c5c; color: white;")
            elif action in ['and', 'or', 'xor', 'not', 'left_shift', 'right_shift']:
                btn.setStyleSheet("background: #a5a5a5; color: black;")
            else:
                btn.setStyleSheet("background: #4a4a4a; color: white;")
            
            grid.addWidget(btn, row, col)
        
        layout.addLayout(grid)
        return page
    
    def create_matrix_page(self):
        """ایجاد صفحه حالت ماتریس"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # زمان ساخت این صفحه رو فعلا ساده می‌ذارم
        info_label = QLabel("حالت ماتریس به زودی اضافه خواهد شد")
        info_label.setFont(self.font_medium)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("color: #888;")
        
        layout.addWidget(info_label)
        
        # دکمه‌های اساسی برای ماتریس
        grid = QGridLayout()
        grid.setSpacing(10)
        
        buttons = [
            ('[', 'matrix_open'), (']', 'matrix_close'),
            ('+', 'matrix_add'), ('-', 'matrix_sub'),
            ('×', 'matrix_mul'), ('T', 'matrix_transpose'),
            ('det', 'matrix_det'), ('inv', 'matrix_inv')
        ]
        
        for i, (text, action) in enumerate(buttons):
            row = i // 2
            col = i % 2
            btn = QPushButton(text)
            btn.setFont(self.font_medium)
            btn.setMinimumHeight(60)
            btn.clicked.connect(lambda _, a=action: self.on_button_click(a))
            btn.setStyleSheet("background: #5c5c5c; color: white;")
            grid.addWidget(btn, row, col)
        
        layout.addLayout(grid)
        return page
    
    def change_mode(self, index):
        """تغییر حالت ماشین حساب"""
        self.current_mode = self.modes[index]
        self.tab_widget.setCurrentIndex(index)
        self.status_bar.setText(f"حالت: {self.current_mode}")
        self.clear_display()
    
    def on_button_click(self, action):
        """هنگام کلیک روی دکمه‌ها"""
        if action in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
            self.add_digit(action)
        elif action in ['+', '-', '*', '/', '=']:
            self.handle_operation(action)
        elif action == 'c':
            self.clear_display()
        elif action == 'ce':
            self.current_input = ""
            self.update_display()
        elif action == 'backspace':
            self.backspace()
        elif action == 'negate':
            self.negate()
        elif action in ['sqrt', 'square', 'sin', 'cos', 'tan', 'log10', 'ln']:
            self.handle_function(action)
        elif action == 'pi':
            self.current_input = str(math.pi)
            self.update_display()
        elif action == 'e':
            self.current_input = str(math.e)
            self.update_display()
        elif action == 'factorial':
            self.factorial()
        elif action == 'power':
            self.operation = '^'
            self.first_operand = self.current_input
            self.waiting_for_second = True
            self.secondary_display.setText(f"{self.first_operand} ^")
            self.current_input = ""
            self.update_display()
        elif action == 'paren_open':
            self.current_input += "("
            self.update_display()
        elif action == 'paren_close':
            self.current_input += ")"
            self.update_display()
        elif action in ['A', 'B', 'C', 'D', 'E', 'F']:
            self.current_input += action
            self.update_display()
        elif action in ['and', 'or', 'xor', 'not', 'left_shift', 'right_shift']:
            self.handle_bitwise(action)
    
    def add_digit(self, digit):
        """افزودن رقم"""
        if self.waiting_for_second:
            self.current_input = digit
            self.waiting_for_second = False
            self.secondary_display.setText(f"{self.first_operand} {self.operation}")
        else:
            self.current_input += digit
        self.update_display()
    
    def handle_operation(self, op):
        """مدیریت عملیات‌ها"""
        if op == '=':
            self.calculate()
        else:
            if self.operation and not self.waiting_for_second:
                self.calculate()
            self.first_operand = self.current_input
            self.operation = op
            self.waiting_for_second = True
            self.secondary_display.setText(f"{self.first_operand} {self.operation}")
            self.current_input = ""
            self.update_display()
    
    def calculate(self):
        """محاسبه نتیجه"""
        if not self.operation or self.first_operand is None:
            return
        
        try:
            num1 = Decimal(self.first_operand)
            num2 = Decimal(self.current_input)
            
            if self.operation == '+':
                result = num1 + num2
            elif self.operation == '-':
                result = num1 - num2
            elif self.operation == '*':
                result = num1 * num2
            elif self.operation == '/':
                if num2 == 0:
                    self.display.setText("خطا: تقسیم بر صفر")
                    return
                result = num1 / num2
            elif self.operation == '^':
                result = Decimal(math.pow(float(num1), float(num2)))
            
            self.current_input = str(result)
            self.last_result = float(result)
            self.add_to_history(f"{self.first_operand} {self.operation} {self.current_input} = {result}")
            self.operation = None
            self.first_operand = None
            self.waiting_for_second = False
            self.secondary_display.setText("")
            self.update_display()
            
            # به روز رسانی نمایشگر‌های برنامه‌نویس
            self.update_programmer_display()
            
        except Exception as e:
            self.display.setText(f"خطا: {str(e)}")
            self.secondary_display.setText("")
    
    def handle_function(self, func):
        """مدیریت توابع"""
        try:
            num = float(self.current_input)
            
            if func == 'sqrt':
                if num < 0:
                    self.display.setText("خطا: ریشه منفی")
                    return
                result = math.sqrt(num)
            elif func == 'square':
                result = num ** 2
            elif func == 'sin':
                result = math.sin(math.radians(num))
            elif func == 'cos':
                result = math.cos(math.radians(num))
            elif func == 'tan':
                result = math.tan(math.radians(num))
            elif func == 'log10':
                if num <= 0:
                    self.display.setText("خطا: لگاریتم غیرمثبت")
                    return
                result = math.log10(num)
            elif func == 'ln':
                if num <= 0:
                    self.display.setText("خطا: لن غیرمثبت")
                    return
                result = math.log(num)
            
            self.current_input = str(result)
            self.last_result = result
            self.add_to_history(f"{func}({num}) = {result}")
            self.update_display()
            self.update_programmer_display()
            
        except Exception as e:
            self.display.setText(f"خطا: {str(e)}")
    
    def factorial(self):
        """محاسبه فاکتوریل"""
        try:
            num = int(float(self.current_input))
            if num < 0:
                self.display.setText("خطا: فاکتوریل منفی")
                return
            if num > 20:
                self.display.setText("خطا: عدد زیاد")
                return
            result = math.factorial(num)
            self.current_input = str(result)
            self.last_result = result
            self.add_to_history(f"{num}! = {result}")
            self.update_display()
        except Exception as e:
            self.display.setText(f"خطا: {str(e)}")
    
    def handle_bitwise(self, op):
        """مدیریت عملیات بیت‌وار"""
        try:
            num1 = int(float(self.first_operand)) if self.first_operand else int(float(self.current_input))
            
            if op == 'and':
                if self.operation:
                    num2 = int(float(self.current_input))
                    result = num1 & num2
                    self.current_input = str(result)
                    self.operation = None
                    self.waiting_for_second = False
                    self.secondary_display.setText("")
                else:
                    self.operation = 'and'
                    self.first_operand = self.current_input
                    self.waiting_for_second = True
                    self.secondary_display.setText(f"{self.first_operand} AND")
                    self.current_input = ""
            
            elif op == 'or':
                if self.operation:
                    num2 = int(float(self.current_input))
                    result = num1 | num2
                    self.current_input = str(result)
                    self.operation = None
                    self.waiting_for_second = False
                    self.secondary_display.setText("")
                else:
                    self.operation = 'or'
                    self.first_operand = self.current_input
                    self.waiting_for_second = True
                    self.secondary_display.setText(f"{self.first_operand} OR")
                    self.current_input = ""
            
            elif op == 'xor':
                if self.operation:
                    num2 = int(float(self.current_input))
                    result = num1 ^ num2
                    self.current_input = str(result)
                    self.operation = None
                    self.waiting_for_second = False
                    self.secondary_display.setText("")
                else:
                    self.operation = 'xor'
                    self.first_operand = self.current_input
                    self.waiting_for_second = True
                    self.secondary_display.setText(f"{self.first_operand} XOR")
                    self.current_input = ""
            
            elif op == 'not':
                result = ~num1
                self.current_input = str(result)
                self.add_to_history(f"NOT({num1}) = {result}")
            
            elif op == 'left_shift':
                if self.operation:
                    num2 = int(float(self.current_input))
                    result = num1 << num2
                    self.current_input = str(result)
                    self.operation = None
                    self.waiting_for_second = False
                    self.secondary_display.setText("")
                else:
                    self.operation = 'left_shift'
                    self.first_operand = self.current_input
                    self.waiting_for_second = True
                    self.secondary_display.setText(f"{self.first_operand} <<")
                    self.current_input = ""
            
            elif op == 'right_shift':
                if self.operation:
                    num2 = int(float(self.current_input))
                    result = num1 >> num2
                    self.current_input = str(result)
                    self.operation = None
                    self.waiting_for_second = False
                    self.secondary_display.setText("")
                else:
                    self.operation = 'right_shift'
                    self.first_operand = self.current_input
                    self.waiting_for_second = True
                    self.secondary_display.setText(f"{self.first_operand} >>")
                    self.current_input = ""
            
            self.update_display()
            self.update_programmer_display()
            
        except Exception as e:
            self.display.setText(f"خطا: {str(e)}")
    
    def clear_display(self):
        """پاک کردن نمایشگر"""
        self.current_input = ""
        self.first_operand = None
        self.operation = None
        self.waiting_for_second = False
        self.secondary_display.setText("")
        self.update_display()
    
    def backspace(self):
        """پاک کردن آخرین کاراکتر"""
        self.current_input = self.current_input[:-1] if self.current_input else ""
        self.update_display()
    
    def negate(self):
        """عکس کردن علامت"""
        if self.current_input and self.current_input != "0":
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.update_display()
    
    def update_display(self):
        """به‌روز رسانی نمایشگر"""
        text = self.current_input if self.current_input else "0"
        self.display.setText(text)
        self.update_programmer_display()
    
    def update_programmer_display(self):
        """به‌روز رسانی نمایشگر‌های برنامه‌نویس"""
        try:
            if self.current_input and self.current_mode == "برنامه‌نویس":
                num = int(float(self.current_input))
                self.hex_label.setText(f"HEX: {hex(num)}")
                self.bin_label.setText(f"BIN: {bin(num)}")
                self.dec_label.setText(f"DEC: {num}")
        except:
            pass
    
    # توابع حافظه
    def memory_store(self):
        try:
            self.memory = float(self.current_input)
        except:
            pass
    
    def memory_recall(self):
        self.current_input = str(self.memory)
        self.update_display()
    
    def memory_add(self):
        try:
            self.memory += float(self.current_input)
        except:
            pass
    
    def memory_subtract(self):
        try:
            self.memory -= float(self.current_input)
        except:
            pass
    
    def memory_clear(self):
        self.memory = 0
    
    def add_to_history(self, expression):
        """افزودن به تاریخچه"""
        self.history.append(expression)
        if len(self.history) > 100:
            self.history.pop(0)
    
    # مدیریت رویداد کیبورد
    def eventFilter(self, source, event):
        if event.type() == QKeyEvent.Type.KeyPress:
            key = event.key()
            text = event.text()
            
            # اعداد و نقطه
            if text in '0123456789.':
                self.on_button_click(text)
                return True
            
            # عملیات
            elif key == Qt.Key.Key_Plus:
                self.on_button_click('+')
                return True
            elif key == Qt.Key.Key_Minus:
                self.on_button_click('-')
                return True
            elif key == Qt.Key.Key_Asterisk:
                self.on_button_click('*')
                return True
            elif key == Qt.Key.Key_Slash:
                self.on_button_click('/')
                return True
            elif key == Qt.Key.Key_Enter or key == Qt.Key.Key_Equal:
                self.on_button_click('=')
                return True
            
            # دکمه‌های خاص
            elif key == Qt.Key.Key_Escape:
                self.clear_display()
                return True
            elif key == Qt.Key.Key_Backspace:
                self.backspace()
                return True
            elif key == Qt.Key.Key_Delete:
                self.on_button_click('c')
                return True
            
            # توابع علمی
            elif text == 's':
                self.on_button_click('sin')
                return True
            elif text == 'c':
                self.on_button_click('cos')
                return True
            elif text == 't':
                self.on_button_click('tan')
                return True
            elif text == 'l':
                self.on_button_click('log10')
                return True
            elif text == 'n':
                self.on_button_click('ln')
                return True
            elif text == 'p':
                self.on_button_click('pi')
                return True
            elif text == 'e':
                self.on_button_click('e')
                return True
        
        return super().eventFilter(source, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # تنظیم استایل
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 40))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(200, 200, 200))
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 35))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 65))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Text, QColor(200, 200, 200))
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 65))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)
    
    calc = CalculatorApp()
    calc.show()
    sys.exit(app.exec())
