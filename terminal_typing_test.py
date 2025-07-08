#!/usr/bin/env python3
"""
Simple and Robust Terminal Typing Test
A simplified version that works reliably across all systems
"""

import time
import random
import os
import sys

# Simple color codes that work everywhere
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'  
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print a simple header."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}")
    print("=" * 70)
    print("               TERMINAL TYPING TEST")
    print("            Master Your Typing Skills!")
    print("=" * 70)
    print(f"{Colors.RESET}\n")

def print_instructions():
    """Print simple instructions."""
    print(f"{Colors.GREEN}HOW TO PLAY:{Colors.RESET}")
    print("1. Read the sentence below")
    print("2. Press Enter when ready")
    print("3. Type the sentence exactly as shown")
    print("4. Press Enter when finished")
    print("5. View your results!")
    print(f"\n{Colors.YELLOW}Tips: Focus on accuracy first, speed comes with practice!{Colors.RESET}")

def display_sentence(sentence):
    """Display the target sentence."""
    print(f"\n{Colors.YELLOW}" + "=" * 70 + f"{Colors.RESET}")
    print(f"{Colors.BOLD}TARGET SENTENCE:{Colors.RESET}")
    print(f"{Colors.YELLOW}" + "=" * 70 + f"{Colors.RESET}")
    print(f"\n{Colors.WHITE}{Colors.BOLD}{sentence}{Colors.RESET}")
    print(f"\n{Colors.YELLOW}" + "=" * 70 + f"{Colors.RESET}")

def get_performance_rating(wpm, accuracy):
    """Get performance rating based on WPM and accuracy."""
    if wpm >= 60 and accuracy >= 95:
        return f"{Colors.GREEN}{Colors.BOLD}EXCELLENT!{Colors.RESET}", "You're a typing master!"
    elif wpm >= 40 and accuracy >= 85:
        return f"{Colors.YELLOW}{Colors.BOLD}GOOD JOB!{Colors.RESET}", "Great work, keep it up!"
    else:
        return f"{Colors.CYAN}{Colors.BOLD}KEEP PRACTICING!{Colors.RESET}", "You're improving!"

def display_results(elapsed_time, wpm, accuracy, user_input, target_sentence):
    """Display results in a simple format."""
    print(f"\n{Colors.CYAN}" + "=" * 50 + f"{Colors.RESET}")
    print(f"{Colors.BOLD}YOUR RESULTS:{Colors.RESET}")
    print(f"{Colors.CYAN}" + "=" * 50 + f"{Colors.RESET}")
    
    print(f"\nTime Taken: {Colors.BLUE}{elapsed_time:.2f} seconds{Colors.RESET}")
    print(f"Typing Speed: {Colors.GREEN}{wpm:.1f} WPM{Colors.RESET}")
    print(f"Accuracy: {Colors.YELLOW}{accuracy:.1f}%{Colors.RESET}")
    
    rating, message = get_performance_rating(wpm, accuracy)
    print(f"\nPerformance: {rating}")
    print(f"Message: {message}")
    
    # Show errors if any
    if accuracy < 100:
        print(f"\n{Colors.RED}ERROR ANALYSIS:{Colors.RESET}")
        print(f"Expected: {target_sentence}")
        print(f"You typed: {user_input}")
        
        # Show character-by-character comparison
        print(f"\nCharacter comparison:")
        for i, (expected, typed) in enumerate(zip(target_sentence, user_input)):
            if expected != typed:
                print(f"Position {i+1}: Expected '{expected}', Got '{typed}'")
    
    print(f"\n{Colors.CYAN}" + "=" * 50 + f"{Colors.RESET}")

def countdown(seconds=3):
    """Simple countdown."""
    print(f"\n{Colors.CYAN}Get ready to type...{Colors.RESET}")
    for i in range(seconds, 0, -1):
        print(f"\rStarting in: {Colors.RED}{Colors.BOLD}{i}{Colors.RESET}", end="", flush=True)
        time.sleep(1)
    print(f"\r{Colors.GREEN}{Colors.BOLD}START TYPING NOW!{Colors.RESET}" + " " * 20)

def terminal_typing_test():
    """
    Main typing test function - simplified and robust.
    """
    
    # Simple list of sentences
    sentences = [
        "The quick brown fox jumps over the lazy dog.",
        "Pack my box with five dozen liquor jugs.",
        "How quickly daft jumping zebras vex.",
        "Programming is the art of telling a computer what to do.",
        "Practice makes perfect in all endeavors.",
        "Never underestimate the power of determination.",
        "To be or not to be, that is the question.",
        "Success comes to those who keep trying.",
        "The only way to do great work is to love what you do.",
        "Keep practicing and you will improve your typing speed."
    ]

    clear_screen()
    print_header()
    print_instructions()
    
    input(f"\n{Colors.GREEN}Press Enter to begin your typing journey!{Colors.RESET}")
    
    round_number = 1
    
    # Main game loop
    while True:
        clear_screen()
        print(f"{Colors.MAGENTA}{Colors.BOLD}ROUND {round_number}{Colors.RESET}")
        print("-" * 30)
        
        # Select a random sentence
        target_sentence = random.choice(sentences)
        display_sentence(target_sentence)
        
        input(f"\n{Colors.CYAN}Press Enter when you're ready to start typing...{Colors.RESET}")
        countdown(3)

        # Start timing and get user input
        start_time = time.time()
        print(f"\n{Colors.GREEN}Type here: {Colors.RESET}", end="")
        
        try:
            user_input = input()
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Test interrupted. Goodbye!{Colors.RESET}")
            break
        except Exception as e:
            print(f"\n{Colors.RED}Input error: {e}{Colors.RESET}")
            continue
            
        end_time = time.time()

        # Calculate results
        elapsed_time = end_time - start_time
        
        # Calculate WPM (Words Per Minute)
        if elapsed_time > 0:
            words_typed = len(user_input) / 5  # Standard: 5 characters = 1 word
            minutes = elapsed_time / 60
            wpm = words_typed / minutes
        else:
            wpm = 0

        # Calculate accuracy
        correct_chars = 0
        min_length = min(len(user_input), len(target_sentence))
        
        for i in range(min_length):
            if i < len(user_input) and i < len(target_sentence):
                if user_input[i] == target_sentence[i]:
                    correct_chars += 1
        
        # Account for length differences
        total_chars = len(target_sentence)
        accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 0

        # Display results
        display_results(elapsed_time, wpm, accuracy, user_input, target_sentence)

        # Ask to continue
        print(f"\n{Colors.MAGENTA}Would you like to continue?{Colors.RESET}")
        try:
            play_again = input(f"{Colors.CYAN}Type 'y' for Yes or 'n' for No: {Colors.RESET}").lower().strip()
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Goodbye!{Colors.RESET}")
            break
            
        if play_again not in ['y', 'yes']:
            break
            
        round_number += 1

    # Goodbye message
    clear_screen()
    print(f"\n{Colors.GREEN}{Colors.BOLD}")
    print("=" * 50)
    print("       Thank you for playing!")
    print("    Practice regularly to improve!")
    print("         Happy typing!")
    print("=" * 50)
    print(f"{Colors.RESET}\n")

# Run the test if this file is executed directly
if __name__ == "__main__":
    try:
        terminal_typing_test()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Program interrupted. Goodbye!{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}An error occurred: {e}{Colors.RESET}")
        print(f"{Colors.YELLOW}Please try running the program again.{Colors.RESET}") 