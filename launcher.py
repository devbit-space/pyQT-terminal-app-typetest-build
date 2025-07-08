#!/usr/bin/env python3
"""
Typing Test Launcher
Choose between CLI (CUI) and Desktop GUI versions
"""

import sys
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    missing_deps = []
    
    try:
        import colorama
    except ImportError:
        missing_deps.append("colorama")
    
    try:
        import PyQt5
    except ImportError:
        missing_deps.append("PyQt5")
    
    return missing_deps

def show_banner():
    """Display the launcher banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                    🎯 TYPING TEST LAUNCHER 🎯                    ║
║                                                                  ║
║                     Choose Your Experience!                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

🚀 Available Versions:

1️⃣  CUI Version (Command Line Interface)
    • Colorful terminal-based interface
    • Works in any terminal/command prompt
    • Lightweight and fast

2️⃣  GUI Version (Desktop Application)
    • Modern graphical interface
    • Beautiful visual design
    • Mouse and keyboard interaction
    • Real-time statistics display

3️⃣  Exit

"""
    print(banner)

def run_cui_version():
    """Run the CUI (terminal) version"""
    print("🚀 Starting CUI Version...\n")
    try:
        import index
        # The index.py file will run automatically when imported
    except ImportError:
        print("❌ Error: Could not find index.py file!")
        input("Press Enter to return to main menu...")

def run_gui_version():
    """Run the GUI (desktop) version"""
    print("🚀 Starting Desktop GUI Version...\n")
    try:
        import typing_test_gui
        typing_test_gui.main()
    except ImportError as e:
        print(f"❌ Error: Could not start GUI version!")
        print(f"Details: {e}")
        print("\nMake sure PyQt5 is installed:")
        print("pip install PyQt5")
        input("Press Enter to return to main menu...")
    except Exception as e:
        print(f"❌ Error running GUI version: {e}")
        input("Press Enter to return to main menu...")

def main():
    """Main launcher function"""
    # Check dependencies
    missing_deps = check_dependencies()
    
    while True:
        # Clear screen (cross-platform)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        show_banner()
        
        # Show dependency warnings if any
        if missing_deps:
            print("⚠️  WARNING: Some dependencies are missing:")
            for dep in missing_deps:
                print(f"   • {dep}")
            print("\nInstall missing dependencies with:")
            print("pip install -r requirements.txt\n")
        
        try:
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == '1':
                if 'colorama' in missing_deps:
                    print("❌ CUI version requires 'colorama'. Please install it first.")
                    input("Press Enter to continue...")
                    continue
                run_cui_version()
            
            elif choice == '2':
                if 'PyQt5' in missing_deps:
                    print("❌ GUI version requires 'PyQt5'. Please install it first.")
                    input("Press Enter to continue...")
                    continue
                run_gui_version()
            
            elif choice == '3':
                print("\n👋 Thanks for using Typing Test! Goodbye!")
                break
            
            else:
                print("❌ Invalid choice! Please enter 1, 2, or 3.")
                input("Press Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main() 