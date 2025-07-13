#!/usr/bin/env python3
"""
Desktop Typing Test Application using PyQt5
A modern, beautiful GUI version of the typing test game.
"""

import sys
import time
import random
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QTextEdit, QPushButton, 
                             QProgressBar, QFrame, QScrollArea, QGridLayout,
                             QSpacerItem, QSizePolicy, QMessageBox, QComboBox)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QThread, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap, QPainter, QLinearGradient

class TypingTestGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sentences = [
            "The quick brown fox jumps over the lazy dog.",
            "Pack my box with five dozen liquor jugs.",
            "How vexingly quick daft zebras jump.",
            "Programming is the art of telling a computer what to do.",
            "The journey of a thousand miles begins with a single step.",
            "Never underestimate the power of a good book.",
            "To be or not to be, that is the question.",
            "Success is not final, failure is not fatal: it is the courage to continue that counts.",
            "The only way to do great work is to love what you do.",
            "You can find this code on many websites, but this version is clean and simple.",
            "Practice makes perfect, but perfect practice makes champions.",
            "Code is poetry written for machines to understand and humans to maintain.",
            "Every expert was once a beginner, every professional was once an amateur.",
            "The best time to plant a tree was 20 years ago. The second best time is now."
        ]
        
        self.current_sentence = ""
        self.start_time = None
        self.round_number = 1
        self.stats_history = []
        self.timed_mode = False
        self.time_limit = 60  # Default 60 seconds
        self.remaining_time = 60
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timed_mode)
        
        self.init_ui()
        self.setup_styles()
        self.new_round()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🎯 Desktop Typing Test - Master Your Skills!")
        self.setGeometry(100, 100, 1200, 900)
        self.setMinimumSize(1000, 800)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(15, 15, 15, 15)
        self.create_header(main_layout)
        self.create_game_area(main_layout)
        self.create_controls_area(main_layout)
        # Ensure time limit combo is hidden on startup (sentence mode)
        self.time_limit_combo.setVisible(False)

    def create_header(self, parent_layout):
        """Create the header section with title and round info"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(6)  # Reduced from 8
        
        # Main title
        title_label = QLabel("🚀 Desktop Typing Test 🚀")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Master Your Typing Skills with Style!")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle_label)
        
        # Mode selection
        self.create_mode_selection(header_layout)
        
        # Round info
        self.round_label = QLabel(f"Round {self.round_number}")
        self.round_label.setObjectName("roundLabel")
        self.round_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.round_label)
        
        parent_layout.addWidget(header_frame)

    def create_mode_selection(self, parent_layout):
        """Create the mode selection frame"""
        mode_frame = QFrame()
        mode_frame.setObjectName("modeFrame")
        mode_layout = QHBoxLayout(mode_frame)
        mode_layout.setSpacing(10)
        
        self.sentence_mode_btn = QPushButton("📝 Sentence Mode")
        self.sentence_mode_btn.setObjectName("modeButton")
        self.sentence_mode_btn.setCheckable(True)
        self.sentence_mode_btn.setChecked(True)
        self.sentence_mode_btn.clicked.connect(lambda: self.switch_mode(False))
        mode_layout.addWidget(self.sentence_mode_btn)
        
        self.timed_mode_btn = QPushButton("⏱️ Timed Mode")
        self.timed_mode_btn.setObjectName("modeButton")
        self.timed_mode_btn.setCheckable(True)
        self.timed_mode_btn.clicked.connect(lambda: self.switch_mode(True))
        mode_layout.addWidget(self.timed_mode_btn)
        
        # Time limit selector for timed mode
        self.time_limit_combo = QComboBox()
        self.time_limit_combo.setObjectName("timeLimitCombo")
        self.time_limit_combo.addItems(["30 seconds", "60 seconds", "2 minutes", "5 minutes"])
        self.time_limit_combo.setCurrentText("60 seconds")
        self.time_limit_combo.currentTextChanged.connect(self.update_time_limit)
        mode_layout.addWidget(self.time_limit_combo)
        
        parent_layout.addWidget(mode_frame)

    def create_game_area(self, parent_layout):
        """Create the main game area with sentence display and input"""
        game_frame = QFrame()
        game_frame.setObjectName("gameFrame")
        game_layout = QVBoxLayout(game_frame)
        game_layout.setSpacing(8)
        
        self.instructions_label = QLabel("📖 Read the sentence below and type it as accurately and quickly as possible!")
        self.instructions_label.setObjectName("instructionsLabel")
        self.instructions_label.setAlignment(Qt.AlignCenter)
        self.instructions_label.setWordWrap(True)
        game_layout.addWidget(self.instructions_label)
        
        self.sentence_frame = QFrame()
        self.sentence_frame.setObjectName("sentenceFrame")
        sentence_layout = QVBoxLayout(self.sentence_frame)
        sentence_layout.setSpacing(4)
        self.sentence_title = QLabel("🎯 TARGET SENTENCE")
        self.sentence_title.setObjectName("sentenceTitle")
        self.sentence_title.setAlignment(Qt.AlignCenter)
        sentence_layout.addWidget(self.sentence_title)
        self.sentence_label = QLabel()
        self.sentence_label.setObjectName("sentenceLabel")
        self.sentence_label.setAlignment(Qt.AlignCenter)
        self.sentence_label.setWordWrap(True)
        sentence_layout.addWidget(self.sentence_label)
        game_layout.addWidget(self.sentence_frame)
        
        input_frame = QFrame()
        input_frame.setObjectName("inputFrame")
        input_layout = QVBoxLayout(input_frame)
        input_layout.setSpacing(4)
        input_title = QLabel("✏️ TYPE HERE")
        input_title.setObjectName("inputTitle")
        input_title.setAlignment(Qt.AlignCenter)
        input_layout.addWidget(input_title)
        
        self.typing_input = QTextEdit()
        self.typing_input.setObjectName("typingInput")
        self.typing_input.setMaximumHeight(70)
        self.typing_input.setMinimumHeight(50)
        self.typing_input.textChanged.connect(self.on_text_changed)
        input_layout.addWidget(self.typing_input)
        
        self.timed_start_button = QPushButton("▶️ Start Timed Test")
        self.timed_start_button.setObjectName("timedStartButton")
        self.timed_start_button.clicked.connect(self.start_timed_mode)
        self.timed_start_button.setVisible(False)
        input_layout.addWidget(self.timed_start_button)
        
        game_layout.addWidget(input_frame)
        
        self.input_frame = input_frame  # Save for show/hide
        self.input_title = input_title  # Save for show/hide
        self.input_layout = input_layout
        
        progress_layout = QHBoxLayout()
        progress_layout.setSpacing(12)
        self.timer_label = QLabel("⏱️ Ready to start!")
        self.timer_label.setObjectName("timerLabel")
        progress_layout.addWidget(self.timer_label)
        progress_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setMinimumWidth(220)
        progress_layout.addWidget(self.progress_bar)
        game_layout.addLayout(progress_layout)
        parent_layout.addWidget(game_frame)

    def create_controls_area(self, parent_layout):
        """Create controls and statistics area"""
        controls_frame = QFrame()
        controls_frame.setObjectName("controlsFrame")
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setSpacing(12)  # Reduced from 15
        
        # Statistics panel
        stats_frame = QFrame()
        stats_frame.setObjectName("statsFrame")
        stats_layout = QVBoxLayout(stats_frame)
        stats_layout.setSpacing(6)  # Reduced from 8
        
        stats_title = QLabel("📊 LIVE STATS")
        stats_title.setObjectName("statsTitle")
        stats_title.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(stats_title)
        
        stats_grid = QGridLayout()
        stats_grid.setSpacing(6)  # Reduced from 8
        
        # WPM
        stats_grid.addWidget(QLabel("🚀 WPM:"), 0, 0)
        self.wpm_label = QLabel("0")
        self.wpm_label.setObjectName("wpmLabel")
        stats_grid.addWidget(self.wpm_label, 0, 1)
        
        # Time
        stats_grid.addWidget(QLabel("⏱️ Time:"), 1, 0)
        self.time_label = QLabel("0.0s")
        self.time_label.setObjectName("timeLabel")
        stats_grid.addWidget(self.time_label, 1, 1)
        
        # Characters per second
        stats_grid.addWidget(QLabel("⚡ Chars/sec:"), 2, 0)
        self.cps_label = QLabel("0.0")
        self.cps_label.setObjectName("cpsLabel")
        stats_grid.addWidget(self.cps_label, 2, 1)
        
        stats_layout.addLayout(stats_grid)
        controls_layout.addWidget(stats_frame)
        
        # Control buttons
        buttons_frame = QFrame()
        buttons_layout = QVBoxLayout(buttons_frame)
        buttons_layout.setSpacing(6)  # Reduced from 8
        
        self.start_button = QPushButton("🎮 Start New Round")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.new_round)
        buttons_layout.addWidget(self.start_button)
        
        self.reset_button = QPushButton("🔄 Reset Input")
        self.reset_button.setObjectName("resetButton")
        self.reset_button.clicked.connect(self.reset_input)
        buttons_layout.addWidget(self.reset_button)
        
        self.results_button = QPushButton("📈 View Results")
        self.results_button.setObjectName("resultsButton")
        self.results_button.clicked.connect(self.show_results)
        buttons_layout.addWidget(self.results_button)
        
        self.quit_button = QPushButton("🚪 Exit")
        self.quit_button.setObjectName("quitButton")
        self.quit_button.clicked.connect(self.close)
        buttons_layout.addWidget(self.quit_button)
        
        controls_layout.addWidget(buttons_frame)
        
        parent_layout.addWidget(controls_frame)

    def setup_styles(self):
        """Setup the application styles and theme"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1e3c72, stop:1 #2a5298);
            }
            
            #headerFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border: 2px solid #4c63d2;
                border-radius: 12px;
                padding: 12px;
                margin: 3px;
            }
            
            #titleLabel {
                font-size: 24px;
                font-weight: bold;
                color: white;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
            
            #subtitleLabel {
                font-size: 14px;
                color: #e0e6ff;
                font-style: italic;
            }
            
            #roundLabel {
                font-size: 16px;
                font-weight: bold;
                color: #ffeb3b;
                background: rgba(255,255,255,0.1);
                border-radius: 8px;
                padding: 4px 12px;
                margin-top: 8px;
            }
            
            #modeFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border: 2px solid #4c63d2;
                border-radius: 10px;
                padding: 8px;
                margin: 6px 0;
            }
            
            #modeButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: 2px solid #4c63d2;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: bold;
                margin: 2px;
                min-height: 12px;
            }
            
            #modeButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00b894, stop:1 #00cec9);
                border: 2px solid #00a085;
            }
            
            #modeButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a67d8, stop:1 #667eea);
            }
            
            #timeLimitCombo {
                background: white;
                border: 2px solid #74b9ff;
                border-radius: 6px;
                padding: 6px 8px;
                font-size: 12px;
                color: #2d3436;
                min-width: 120px;
            }
            
            #timeLimitCombo:focus {
                border: 3px solid #0984e3;
            }
            
            #gameFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: 2px solid #dee2e6;
                border-radius: 12px;
                padding: 12px;
                margin: 3px;
            }
            
            #instructionsLabel {
                font-size: 13px;
                color: #495057;
                font-weight: bold;
                padding: 8px;
            }
            
            #sentenceFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ffeaa7, stop:1 #fab1a0);
                border: 2px solid #fdcb6e;
                border-radius: 10px;
                padding: 10px;
                margin: 6px 0;
            }
            
            #sentenceTitle {
                font-size: 13px;
                font-weight: bold;
                color: #2d3436;
                margin-bottom: 8px;
            }
            
            #sentenceLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2d3436;
                line-height: 1.3;
                padding: 8px;
                background: rgba(255,255,255,0.7);
                border-radius: 6px;
            }
            
            #inputFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #a8edea, stop:1 #fed6e3);
                border: 2px solid #00cec9;
                border-radius: 10px;
                padding: 10px;
                margin: 6px 0;
            }
            
            #inputTitle {
                font-size: 13px;
                font-weight: bold;
                color: #2d3436;
                margin-bottom: 8px;
            }
            
            #typingInput {
                font-size: 15px;
                font-family: 'Courier New', monospace;
                background: white;
                border: 2px solid #74b9ff;
                border-radius: 6px;
                padding: 8px;
                line-height: 1.4;
            }
            
            #typingInput:focus {
                border: 3px solid #0984e3;
                box-shadow: 0 0 10px rgba(9, 132, 227, 0.3);
            }
            
            #timerLabel, #timeLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2d3436;
            }
            
            #progressBar {
                height: 20px;
                border: 2px solid #00b894;
                border-radius: 10px;
                background: #ddd;
                text-align: center;
                color: white;
                font-weight: bold;
            }
            
            #progressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00b894, stop:1 #00cec9);
                border-radius: 8px;
            }
            
            #controlsFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: 2px solid #dee2e6;
                border-radius: 12px;
                padding: 12px;
                margin: 3px;
            }
            
            #statsFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #81ecec, stop:1 #74b9ff);
                border: 2px solid #0984e3;
                border-radius: 10px;
                padding: 10px;
                margin-right: 12px;
                min-width: 170px;
            }
            
            #statsTitle {
                font-size: 14px;
                font-weight: bold;
                color: #2d3436;
                margin-bottom: 12px;
            }
            
            #wpmLabel, #cpsLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2d3436;
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 14px;
                font-size: 13px;
                font-weight: bold;
                margin: 2px;
                min-height: 14px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a67d8, stop:1 #667eea);
                transform: translateY(-2px);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4c51bf, stop:1 #5a67d8);
            }
            
            #startButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00b894, stop:1 #00cec9);
            }
            
            #startButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00a085, stop:1 #00b894);
            }
            
            #quitButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e17055, stop:1 #d63031);
            }
            
            #quitButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d63031, stop:1 #74b9ff);
            }
        """)

    def new_round(self):
        """Start a new typing round"""
        if not self.timed_mode:
            self.current_sentence = random.choice(self.sentences)
            self.sentence_label.setText(self.current_sentence)
        
        self.typing_input.clear()
        self.typing_input.setEnabled(True)
        self.typing_input.setFocus()
        
        self.round_label.setText(f"Round {self.round_number}")
        self.start_time = None
        self.progress_bar.setValue(0)
        self.timer.stop()  # Stop any running timer
        
        if self.timed_mode:
            self.remaining_time = self.time_limit
            self.timer_label.setText(f"⏱️ {self.remaining_time}s remaining")
        else:
            self.timer_label.setText("⏱️ Ready to start!")
        
        # Reset stats
        self.wpm_label.setText("0")
        self.time_label.setText("0.0s")
        self.cps_label.setText("0.0")

    def reset_input(self):
        """Reset the typing input"""
        self.typing_input.clear()
        self.typing_input.setFocus()
        self.start_time = None
        self.progress_bar.setValue(0)
        self.timer.stop()  # Stop any running timer
        
        if self.timed_mode:
            self.remaining_time = self.time_limit
            self.timer_label.setText(f"⏱️ {self.remaining_time}s remaining")
        else:
            self.timer_label.setText("⏱️ Ready to start!")

    def on_text_changed(self):
        """Handle text change in the typing input"""
        if self.timed_mode:
            if not self.timer.isActive() or not self.typing_input.isEnabled():
                return
            user_text = self.typing_input.toPlainText()
            target_text = self.current_sentence
            correct_length = 0
            for i in range(min(len(user_text), len(target_text))):
                if user_text[i] == target_text[i]:
                    correct_length += 1
                else:
                    correct_text = target_text[:correct_length]
                    self.typing_input.textChanged.disconnect()
                    self.typing_input.setPlainText(correct_text)
                    cursor = self.typing_input.textCursor()
                    cursor.movePosition(cursor.End)
                    self.typing_input.setTextCursor(cursor)
                    self.typing_input.textChanged.connect(self.on_text_changed)
                    user_text = correct_text
                    break
            if len(user_text) > len(target_text):
                correct_text = target_text
                self.typing_input.textChanged.disconnect()
                self.typing_input.setPlainText(correct_text)
                cursor = self.typing_input.textCursor()
                cursor.movePosition(cursor.End)
                self.typing_input.setTextCursor(cursor)
                self.typing_input.textChanged.connect(self.on_text_changed)
                user_text = correct_text
            progress = min(100, (len(user_text) / len(target_text)) * 100)
            self.progress_bar.setValue(int(progress))
            if user_text.strip() == target_text.strip():
                self.timed_sentences_completed += 1
                self.timed_chars_typed += len(user_text)
                self.timed_words_typed += len(user_text) / 5
                self.load_new_sentence()
        else:
            if not self.start_time:
                self.start_time = time.time()
                self.timer_label.setText("⏱️ Typing...")
            user_text = self.typing_input.toPlainText()
            target_text = self.current_sentence
            correct_length = 0
            for i in range(min(len(user_text), len(target_text))):
                if user_text[i] == target_text[i]:
                    correct_length += 1
                else:
                    correct_text = target_text[:correct_length]
                    self.typing_input.textChanged.disconnect()
                    self.typing_input.setPlainText(correct_text)
                    cursor = self.typing_input.textCursor()
                    cursor.movePosition(cursor.End)
                    self.typing_input.setTextCursor(cursor)
                    self.typing_input.textChanged.connect(self.on_text_changed)
                    user_text = correct_text
                    break
            if len(user_text) > len(target_text):
                correct_text = target_text
                self.typing_input.textChanged.disconnect()
                self.typing_input.setPlainText(correct_text)
                cursor = self.typing_input.textCursor()
                cursor.movePosition(cursor.End)
                self.typing_input.setTextCursor(cursor)
                self.typing_input.textChanged.connect(self.on_text_changed)
                user_text = correct_text
            progress = min(100, (len(user_text) / len(target_text)) * 100)
            self.progress_bar.setValue(int(progress))
            elapsed_time = time.time() - self.start_time
            self.time_label.setText(f"{elapsed_time:.1f}s")
            if elapsed_time > 0:
                words_typed = len(user_text) / 5
                minutes = elapsed_time / 60
                wpm = words_typed / minutes
                self.wpm_label.setText(f"{wpm:.1f}")
                chars_per_second = len(user_text) / elapsed_time
                self.cps_label.setText(f"{chars_per_second:.1f}")
            if user_text.strip() == target_text.strip():
                self.complete_round(elapsed_time, float(self.wpm_label.text()))

    def complete_round(self, elapsed_time, wpm):
        """Complete the current round and show results"""
        self.typing_input.setEnabled(False)
        
        # Calculate characters per second for this round
        user_text = self.typing_input.toPlainText()
        chars_per_second = len(user_text) / elapsed_time if elapsed_time > 0 else 0
        
        # Store stats
        stats = {
            'round': self.round_number,
            'time': elapsed_time,
            'wpm': wpm,
            'cps': chars_per_second,
            'timestamp': datetime.now().isoformat()
        }
        self.stats_history.append(stats)
        
        # Show completion message
        if wpm >= 60:
            title = "🏆 EXCELLENT!"
            message = f"Outstanding performance!\n\nRound {self.round_number} Results:\n⏱️ Time: {elapsed_time:.2f} seconds\n🚀 WPM: {wpm:.1f}\n⚡ Chars/sec: {chars_per_second:.1f}"
        elif wpm >= 40:
            title = "⭐ GOOD JOB!"
            message = f"Great work!\n\nRound {self.round_number} Results:\n⏱️ Time: {elapsed_time:.2f} seconds\n🚀 WPM: {wpm:.1f}\n⚡ Chars/sec: {chars_per_second:.1f}"
        else:
            title = "💪 KEEP PRACTICING!"
            message = f"You're improving!\n\nRound {self.round_number} Results:\n⏱️ Time: {elapsed_time:.2f} seconds\n🚀 WPM: {wpm:.1f}\n⚡ Chars/sec: {chars_per_second:.1f}"
        
        QMessageBox.information(self, title, message)
        
        self.round_number += 1
        self.new_round()

    def show_results(self):
        """Show detailed results and statistics"""
        if not self.stats_history:
            QMessageBox.information(self, "📊 Statistics", "No rounds completed yet!\nStart typing to see your statistics.")
            return
        
        # Calculate averages
        avg_wpm = sum(s['wpm'] for s in self.stats_history) / len(self.stats_history)
        avg_cps = sum(s.get('cps', 0) for s in self.stats_history) / len(self.stats_history)
        total_rounds = len(self.stats_history)
        best_wpm = max(s['wpm'] for s in self.stats_history)
        best_cps = max(s.get('cps', 0) for s in self.stats_history)
        
        results_text = f"""📈 Your Typing Statistics 📈

📊 Overall Performance:
• Total Rounds: {total_rounds}
• Average WPM: {avg_wpm:.1f}
• Average Chars/sec: {avg_cps:.1f}
• Best WPM: {best_wpm:.1f}
• Best Chars/sec: {best_cps:.1f}

🏆 Recent Rounds:
"""
        
        for i, stats in enumerate(self.stats_history[-5:], 1):
            cps_display = f", {stats.get('cps', 0):.1f} chars/sec" if 'cps' in stats else ""
            results_text += f"Round {stats['round']}: {stats['wpm']:.1f} WPM{cps_display}\n"
        
        QMessageBox.information(self, "📊 Your Statistics", results_text)

    def switch_mode(self, timed_mode):
        """Switch between sentence mode and timed mode"""
        self.timed_mode = timed_mode
        self.sentence_mode_btn.setChecked(not timed_mode)
        self.timed_mode_btn.setChecked(timed_mode)
        if timed_mode:
            self.instructions_label.setText("⏱️ Type as many sentences as you can for the selected time limit!")
            self.sentence_title.setText("🎯 TARGET SENTENCE")
            self.timed_start_button.setVisible(True)
            self.typing_input.setVisible(False)
            self.input_title.setVisible(False)
            self.sentence_label.setText("Click 'Start Timed Test' to begin!")
            self.time_limit_combo.setVisible(True)
            self.remaining_time = self.time_limit
            self.timer_label.setText(f"⏱️ {self.remaining_time}s remaining")
            self.progress_bar.setValue(0)
        else:
            self.instructions_label.setText("📖 Read the sentence below and type it as accurately and quickly as possible!")
            self.sentence_title.setText("🎯 TARGET SENTENCE")
            self.timed_start_button.setVisible(False)
            self.typing_input.setVisible(True)
            self.input_title.setVisible(True)
            self.time_limit_combo.setVisible(False)
            self.new_round()
        self.timer.stop()
        self.typing_input.clear()
        self.start_time = None
        if not timed_mode:
            self.typing_input.setEnabled(True)
            self.typing_input.setFocus()

    def start_timed_mode(self):
        """Start the timed typing session"""
        self.timed_start_button.setVisible(False)
        self.typing_input.setVisible(True)
        self.input_title.setVisible(True)
        self.typing_input.setEnabled(True)
        self.typing_input.clear()
        self.typing_input.setFocus()
        self.start_time = time.time()
        self.remaining_time = self.time_limit
        self.timer_label.setText(f"⏱️ {self.remaining_time}s remaining")
        self.progress_bar.setValue(0)
        self.timer.start(1000)
        self.timed_sentences_completed = 0
        self.timed_chars_typed = 0
        self.timed_words_typed = 0
        self.load_new_sentence()

    def load_new_sentence(self):
        """Load a new sentence for typing (used in both modes)"""
        self.current_sentence = random.choice(self.sentences)
        self.sentence_label.setText(self.current_sentence)
        self.typing_input.clear()
        self.typing_input.setFocus()

    def update_time_limit(self, text):
        """Update the time limit based on selection"""
        if "30 seconds" in text:
            self.time_limit = 30
        elif "60 seconds" in text:
            self.time_limit = 60
        elif "2 minutes" in text:
            self.time_limit = 120
        elif "5 minutes" in text:
            self.time_limit = 300
        
        self.remaining_time = self.time_limit
        if self.timed_mode:
            self.timer_label.setText(f"⏱️ {self.remaining_time}s remaining")

    def update_timed_mode(self):
        """Update the timer for timed mode"""
        if self.timed_mode and self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_label.setText(f"⏱️ {self.remaining_time}s remaining")
            progress = ((self.time_limit - self.remaining_time) / self.time_limit) * 100
            self.progress_bar.setValue(int(progress))
            if self.remaining_time <= 0:
                self.complete_timed_round()

    def complete_timed_round(self):
        """Complete the timed round and show results"""
        self.timer.stop()
        self.typing_input.setEnabled(False)
        self.timed_start_button.setEnabled(True)
        # Finalize stats
        elapsed_time = self.time_limit
        wpm = self.timed_words_typed / (elapsed_time / 60) if elapsed_time > 0 else 0
        chars_per_second = self.timed_chars_typed / elapsed_time if elapsed_time > 0 else 0
        stats = {
            'round': self.round_number,
            'time': elapsed_time,
            'wpm': wpm,
            'cps': chars_per_second,
            'characters': self.timed_chars_typed,
            'words': self.timed_words_typed,
            'sentences': self.timed_sentences_completed,
            'timestamp': datetime.now().isoformat()
        }
        self.stats_history.append(stats)
        if wpm >= 60:
            title = "🏆 EXCELLENT!"
            message = f"Outstanding performance!\n\nTimed Round {self.round_number} Results:\n⏱️ Time: {elapsed_time} seconds\n🚀 WPM: {wpm:.1f}\n⚡ Chars/sec: {chars_per_second:.1f}\n📝 Characters: {self.timed_chars_typed}\n📊 Words: {self.timed_words_typed:.1f}\n📚 Sentences: {self.timed_sentences_completed}"
        elif wpm >= 40:
            title = "⭐ GOOD JOB!"
            message = f"Great work!\n\nTimed Round {self.round_number} Results:\n⏱️ Time: {elapsed_time} seconds\n🚀 WPM: {wpm:.1f}\n⚡ Chars/sec: {chars_per_second:.1f}\n📝 Characters: {self.timed_chars_typed}\n📊 Words: {self.timed_words_typed:.1f}\n📚 Sentences: {self.timed_sentences_completed}"
        else:
            title = "💪 KEEP PRACTICING!"
            message = f"You're improving!\n\nTimed Round {self.round_number} Results:\n⏱️ Time: {elapsed_time} seconds\n🚀 WPM: {wpm:.1f}\n⚡ Chars/sec: {chars_per_second:.1f}\n📝 Characters: {self.timed_chars_typed}\n📊 Words: {self.timed_words_typed:.1f}\n📚 Sentences: {self.timed_sentences_completed}"
        QMessageBox.information(self, title, message)
        self.round_number += 1
        self.switch_mode(True)


def main():
    """Main function to run the application"""
    app = QApplication(sys.argv)
    app.setApplicationName("Desktop Typing Test")
    app.setApplicationVersion("1.0")
    
    # Set application icon and properties
    app.setStyle('Fusion')  # Modern look
    
    window = TypingTestGUI()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main() 
