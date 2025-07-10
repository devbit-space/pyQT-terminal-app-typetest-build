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
                             QSpacerItem, QSizePolicy, QMessageBox)
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
        
        self.init_ui()
        self.setup_styles()
        self.new_round()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🎯 Desktop Typing Test - Master Your Skills!")
        # Increased window size to ensure all content is visible and comfortable
        self.setGeometry(100, 100, 1200, 900)  # Increased height from 800 to 900
        self.setMinimumSize(1000, 800)  # Increased minimum height from 700 to 800
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with optimized spacing
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(12)  # Reduced from 15
        main_layout.setContentsMargins(15, 15, 15, 15)  # Reduced from 20 all around
        
        # Title and header
        self.create_header(main_layout)
        
        # Game area
        self.create_game_area(main_layout)
        
        # Stats and controls
        self.create_controls_area(main_layout)

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
        
        # Round info
        self.round_label = QLabel(f"Round {self.round_number}")
        self.round_label.setObjectName("roundLabel")
        self.round_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.round_label)
        
        parent_layout.addWidget(header_frame)

    def create_game_area(self, parent_layout):
        """Create the main game area with sentence display and input"""
        game_frame = QFrame()
        game_frame.setObjectName("gameFrame")
        game_layout = QVBoxLayout(game_frame)
        game_layout.setSpacing(8)  # Reduced from 10
        
        # Instructions
        instructions_label = QLabel("📖 Read the sentence below and type it as accurately and quickly as possible!")
        instructions_label.setObjectName("instructionsLabel")
        instructions_label.setAlignment(Qt.AlignCenter)
        instructions_label.setWordWrap(True)
        game_layout.addWidget(instructions_label)
        
        # Target sentence display
        sentence_frame = QFrame()
        sentence_frame.setObjectName("sentenceFrame")
        sentence_layout = QVBoxLayout(sentence_frame)
        sentence_layout.setSpacing(4)  # Reduced from 5
        
        sentence_title = QLabel("🎯 TARGET SENTENCE")
        sentence_title.setObjectName("sentenceTitle")
        sentence_title.setAlignment(Qt.AlignCenter)
        sentence_layout.addWidget(sentence_title)
        
        self.sentence_label = QLabel()
        self.sentence_label.setObjectName("sentenceLabel")
        self.sentence_label.setAlignment(Qt.AlignCenter)
        self.sentence_label.setWordWrap(True)
        sentence_layout.addWidget(self.sentence_label)
        
        game_layout.addWidget(sentence_frame)
        
        # Typing input area
        input_frame = QFrame()
        input_frame.setObjectName("inputFrame")
        input_layout = QVBoxLayout(input_frame)
        input_layout.setSpacing(4)  # Reduced from 5
        
        input_title = QLabel("✏️ TYPE HERE")
        input_title.setObjectName("inputTitle")
        input_title.setAlignment(Qt.AlignCenter)
        input_layout.addWidget(input_title)
        
        self.typing_input = QTextEdit()
        self.typing_input.setObjectName("typingInput")
        self.typing_input.setMaximumHeight(70)  # Reduced from 80
        self.typing_input.setMinimumHeight(50)  # Reduced from 60
        self.typing_input.textChanged.connect(self.on_text_changed)
        input_layout.addWidget(self.typing_input)
        
        game_layout.addWidget(input_frame)
        
        # Timer and progress
        progress_layout = QHBoxLayout()
        progress_layout.setSpacing(12)  # Reduced from 15
        
        self.timer_label = QLabel("⏱️ Ready to start!")
        self.timer_label.setObjectName("timerLabel")
        progress_layout.addWidget(self.timer_label)
        
        progress_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setMinimumWidth(220)  # Reduced from 250
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
        self.current_sentence = random.choice(self.sentences)
        self.sentence_label.setText(self.current_sentence)
        self.typing_input.clear()
        self.typing_input.setEnabled(True)
        self.typing_input.setFocus()
        
        self.round_label.setText(f"Round {self.round_number}")
        self.start_time = None
        self.progress_bar.setValue(0)
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
        self.timer_label.setText("⏱️ Ready to start!")

    def on_text_changed(self):
        """Handle text change in the typing input"""
        if not self.start_time:
            self.start_time = time.time()
        
        user_text = self.typing_input.toPlainText()
        target_text = self.current_sentence
        
        # Check if the typed text matches the target text so far
        # If not, revert to the last correct position
        correct_length = 0
        for i in range(min(len(user_text), len(target_text))):
            if user_text[i] == target_text[i]:
                correct_length += 1
            else:
                # Found incorrect character, revert to correct portion
                correct_text = target_text[:correct_length]
                # Temporarily disconnect signal to avoid recursion
                self.typing_input.textChanged.disconnect()
                self.typing_input.setPlainText(correct_text)
                # Move cursor to end
                cursor = self.typing_input.textCursor()
                cursor.movePosition(cursor.End)
                self.typing_input.setTextCursor(cursor)
                # Reconnect signal
                self.typing_input.textChanged.connect(self.on_text_changed)
                # Update user_text to the corrected text
                user_text = correct_text
                break
        
        # If user typed more characters than target, limit to target length
        if len(user_text) > len(target_text):
            correct_text = target_text
            # Temporarily disconnect signal to avoid recursion
            self.typing_input.textChanged.disconnect()
            self.typing_input.setPlainText(correct_text)
            # Move cursor to end
            cursor = self.typing_input.textCursor()
            cursor.movePosition(cursor.End)
            self.typing_input.setTextCursor(cursor)
            # Reconnect signal
            self.typing_input.textChanged.connect(self.on_text_changed)
            user_text = correct_text
        
        # Calculate progress
        progress = min(100, (len(user_text) / len(target_text)) * 100)
        self.progress_bar.setValue(int(progress))
        
        # Calculate elapsed time
        elapsed_time = time.time() - self.start_time
        self.time_label.setText(f"{elapsed_time:.1f}s")
        
        # Calculate WPM and Characters per second
        if elapsed_time > 0:
            words_typed = len(user_text) / 5
            minutes = elapsed_time / 60
            wpm = words_typed / minutes
            self.wpm_label.setText(f"{wpm:.1f}")
            
            # Calculate characters per second
            chars_per_second = len(user_text) / elapsed_time
            self.cps_label.setText(f"{chars_per_second:.1f}")
        
        # Check if completed
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
