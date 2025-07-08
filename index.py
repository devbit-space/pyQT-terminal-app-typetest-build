# typing_test.py

import time
import random
import os
import sys

# Try to import colorama for cross-platform colors
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Fallback for systems without colorama
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Back:
        BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print the game banner with ASCII art."""
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    ████████╗██╗   ██╗██████╗ ██╗███╗   ██╗ ██████╗     ████████╗███████╗███████╗████████╗║
║    ╚══██╔══╝╚██╗ ██╔╝██╔══██╗██║████╗  ██║██╔════╝     ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝║
║       ██║    ╚████╔╝ ██████╔╝██║██╔██╗ ██║██║  ███╗       ██║   █████╗  ███████╗   ██║   ║
║       ██║     ╚██╔╝  ██╔═══╝ ██║██║╚██╗██║██║   ██║       ██║   ██╔══╝  ╚════██║   ██║   ║
║       ██║      ██║   ██║     ██║██║ ╚████║╚██████╔╝       ██║   ███████╗███████║   ██║   ║
║       ╚═╝      ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝        ╚═╝   ╚══════╝╚══════╝   ╚═╝   ║
║                                                                              ║
║                          {Fore.YELLOW}🚀 Master Your Typing Skills! 🚀{Fore.CYAN}                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    print(banner)

def print_box(text, color=Fore.WHITE, width=80):
    """Print text in a decorative box."""
    lines = text.split('\n')
    max_line_length = max(len(line) for line in lines) if lines else 0
    box_width = max(width, max_line_length + 4)
    
    print(f"{color}╔{'═' * (box_width - 2)}╗{Style.RESET_ALL}")
    for line in lines:
        padding = box_width - len(line) - 4
        left_pad = padding // 2
        right_pad = padding - left_pad
        print(f"{color}║ {' ' * left_pad}{line}{' ' * right_pad} ║{Style.RESET_ALL}")
    print(f"{color}╚{'═' * (box_width - 2)}╝{Style.RESET_ALL}")

def print_instructions():
    """Print game instructions in a nice format."""
    instructions = f"""
{Fore.GREEN}{Style.BRIGHT}📖 HOW TO PLAY:{Style.RESET_ALL}

{Fore.YELLOW}1.{Style.RESET_ALL} Read the sentence displayed on screen
{Fore.YELLOW}2.{Style.RESET_ALL} Press Enter when ready to start
{Fore.YELLOW}3.{Style.RESET_ALL} Type the sentence as accurately and quickly as possible
{Fore.YELLOW}4.{Style.RESET_ALL} Press Enter when finished
{Fore.YELLOW}5.{Style.RESET_ALL} View your results and try to improve!

{Fore.MAGENTA}💡 Tips:{Style.RESET_ALL}
• Focus on accuracy first, speed will come naturally
• Try to type without looking at the keyboard
• Take breaks to avoid fatigue

{Fore.CYAN}Press Enter to begin your typing journey!{Style.RESET_ALL}
"""
    print(instructions)

def display_sentence(sentence):
    """Display the target sentence in a highlighted box."""
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}{'=' * 80}{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}{Style.BRIGHT} TARGET SENTENCE {Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}{'=' * 80}{Style.RESET_ALL}")
    print(f"\n{Fore.WHITE}{Style.BRIGHT}{sentence}{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}{'=' * 80}{Style.RESET_ALL}")

def get_wpm_color(wpm):
    """Return color based on WPM performance."""
    if wpm >= 60:
        return Fore.GREEN
    elif wpm >= 40:
        return Fore.YELLOW
    else:
        return Fore.RED

def get_accuracy_color(accuracy):
    """Return color based on accuracy performance."""
    if accuracy >= 95:
        return Fore.GREEN
    elif accuracy >= 85:
        return Fore.YELLOW
    else:
        return Fore.RED

def display_results(elapsed_time, wpm, accuracy, user_input, target_sentence):
    """Display results with colorful formatting."""
    wpm_color = get_wpm_color(wpm)
    accuracy_color = get_accuracy_color(accuracy)
    
    # Performance rating
    if wpm >= 60 and accuracy >= 95:
        rating = f"{Fore.GREEN}{Style.BRIGHT}🏆 EXCELLENT! 🏆{Style.RESET_ALL}"
    elif wpm >= 40 and accuracy >= 85:
        rating = f"{Fore.YELLOW}{Style.BRIGHT}⭐ GOOD JOB! ⭐{Style.RESET_ALL}"
    else:
        rating = f"{Fore.CYAN}{Style.BRIGHT}💪 KEEP PRACTICING! 💪{Style.RESET_ALL}"
    
    results = f"""
{Fore.CYAN}{Style.BRIGHT}📊 YOUR PERFORMANCE REPORT 📊{Style.RESET_ALL}

{Fore.BLUE}⏱️  Time Taken:{Style.RESET_ALL} {elapsed_time:.2f} seconds
{wpm_color}🚀 Typing Speed:{Style.RESET_ALL} {wpm:.1f} WPM
{accuracy_color}🎯 Accuracy:{Style.RESET_ALL} {accuracy:.1f}%

{rating}
"""
    
    print_box(results, Fore.CYAN)
    
    # Show typing errors if any
    if accuracy < 100:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}🔍 ERROR ANALYSIS:{Style.RESET_ALL}")
        print(f"{Fore.RED}Expected: {Fore.WHITE}{target_sentence}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}You typed: {Fore.WHITE}{user_input}{Style.RESET_ALL}")

def show_progress_bar(duration=3):
    """Show a countdown progress bar."""
    print(f"\n{Fore.CYAN}Get ready...")
    for i in range(duration, 0, -1):
        print(f"\r{Fore.YELLOW}Starting in: {Fore.RED}{Style.BRIGHT}{i}{Style.RESET_ALL}", end="", flush=True)
        time.sleep(1)
    print(f"\r{Fore.GREEN}{Style.BRIGHT}GO! Type now!{Style.RESET_ALL}" + " " * 20)

def typing_test():
    """
    Runs a CUI-style typing test game with enhanced visuals.
    """
    
    # A list of sentences for the test
    sentences = [
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
        "Code is poetry written for machines to understand and humans to maintain."
    ]

    clear_screen()
    print_banner()
    print_instructions()
    
    input()  # Wait for user to press Enter
    
    round_number = 1
    
    # Main game loop
    while True:
        clear_screen()
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'=' * 30} ROUND {round_number} {'=' * 30}{Style.RESET_ALL}")
        
        # Select a random sentence
        target_sentence = random.choice(sentences)
        display_sentence(target_sentence)
        
        input(f"\n{Fore.CYAN}Press Enter when you're ready to start typing...{Style.RESET_ALL}")
        show_progress_bar(3)

        # Get the start time and prompt for input
        start_time = time.time()
        print(f"\n{Fore.GREEN}📝 Type here: {Style.RESET_ALL}", end="")
        user_input = input()
        end_time = time.time()

        # Calculate Results
        elapsed_time = end_time - start_time
        
        # Calculate WPM
        if elapsed_time > 0:
            words_typed = len(user_input) / 5
            minutes = elapsed_time / 60
            wpm = words_typed / minutes
        else:
            wpm = 0

        # Calculate Accuracy
        correct_chars = 0
        for i in range(min(len(user_input), len(target_sentence))):
            if user_input[i] == target_sentence[i]:
                correct_chars += 1
        
        accuracy = (correct_chars / len(target_sentence)) * 100

        # Display Results
        display_results(elapsed_time, wpm, accuracy, user_input, target_sentence)

        # Ask to play again
        print(f"\n{Fore.MAGENTA}Would you like to continue?{Style.RESET_ALL}")
        play_again = input(f"{Fore.CYAN}[Y]es / [N]o: {Style.RESET_ALL}").lower()
        if play_again not in ['y', 'yes']:
            break
            
        round_number += 1

    # Goodbye message
    clear_screen()
    goodbye_msg = f"""
{Fore.CYAN}{Style.BRIGHT}Thank you for playing!{Style.RESET_ALL}

{Fore.YELLOW}🌟 Remember: Consistent practice is the key to improvement! 🌟{Style.RESET_ALL}

{Fore.GREEN}Happy typing! 👋{Style.RESET_ALL}
"""
    print_box(goodbye_msg, Fore.MAGENTA)


# This ensures the script runs the function when executed
if __name__ == "__main__":
    typing_test()