#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for Android build (using Kivy)
This is used by Buildozer for Android APK builds
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window

class CalculatorApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        self.title = "ماشین حساب پیشرفته"
        self.current_input = ""
        self.operation = None
        self.first_operand = None
        self.waiting_for_second = False
        
        # Main layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Display
        self.display = TextInput(
            multiline=False,
            readonly=True,
            font_size=32,
            halign='right',
            size_hint=(1, 0.2),
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(0, 1, 0, 1)
        )
        layout.add_widget(self.display)
        
        # Secondary display for operations
        self.secondary_display = Label(
            text="",
            font_size=16,
            halign='right',
            color=(0.8, 0.8, 0.8, 1),
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.secondary_display)
        
        # Buttons layout
        buttons_layout = BoxLayout(orientation='vertical', spacing=10)
        
        # Button rows
        button_texts = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['C', '0', '=', '+']
        ]
        
        for row in button_texts:
            button_row = BoxLayout(orientation='horizontal', spacing=10)
            for text in row:
                btn = Button(
                    text=text,
                    font_size=24,
                    background_normal='',
                    background_color=self.get_button_color(text),
                    color=(1, 1, 1, 1)
                )
                btn.bind(on_press=self.on_button_press)
                button_row.add_widget(btn)
            buttons_layout.add_widget(button_row)
        
        layout.add_widget(buttons_layout)
        
        return layout
    
    def get_button_color(self, text):
        if text in ['/', '*', '-', '+', '=']:
            return (1, 0.5, 0, 1)  # Orange
        elif text == 'C':
            return (1, 0.2, 0.2, 1)  # Red
        else:
            return (0.3, 0.3, 0.3, 1)  # Gray
    
    def on_button_press(self, instance):
        text = instance.text
        
        if text in '0123456789':
            self.add_digit(text)
        elif text in '+-*/':
            self.handle_operation(text)
        elif text == '=':
            self.calculate()
        elif text == 'C':
            self.clear_display()
    
    def add_digit(self, digit):
        if self.waiting_for_second:
            self.current_input = digit
            self.waiting_for_second = False
            self.secondary_display.text = f"{self.first_operand} {self.operation}"
        else:
            self.current_input += digit
        self.display.text = self.current_input
    
    def handle_operation(self, op):
        if self.operation and not self.waiting_for_second:
            self.calculate()
        self.first_operand = self.current_input
        self.operation = op
        self.waiting_for_second = True
        self.secondary_display.text = f"{self.first_operand} {self.operation}"
        self.current_input = ""
        self.display.text = ""
    
    def calculate(self):
        if not self.operation or self.first_operand is None:
            return
        
        try:
            num1 = float(self.first_operand)
            num2 = float(self.current_input)
            
            if self.operation == '+':
                result = num1 + num2
            elif self.operation == '-':
                result = num1 - num2
            elif self.operation == '*':
                result = num1 * num2
            elif self.operation == '/':
                if num2 == 0:
                    self.display.text = "Error"
                    return
                result = num1 / num2
            
            self.current_input = str(result)
            self.operation = None
            self.first_operand = None
            self.waiting_for_second = False
            self.secondary_display.text = ""
            self.display.text = self.current_input
            
        except Exception as e:
            self.display.text = "Error"
    
    def clear_display(self):
        self.current_input = ""
        self.first_operand = None
        self.operation = None
        self.waiting_for_second = False
        self.secondary_display.text = ""
        self.display.text = "0"

if __name__ == '__main__':
    CalculatorApp().run()
