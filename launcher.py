#!/usr/bin/env python3
"""
Typing Test Launcher
Choose between CLI (CUI) and Desktop GUI versions
"""

import sys
import os
import time

def check_dependencies():
    """Check if required dependencies are installed"""
    missing_deps = []
    
    # Terminal version doesn't need any external dependencies
    # Only check for GUI dependencies
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

1️⃣  Terminal Version (Command Line Interface)
    • Simple and robust terminal interface
    • Works in any terminal/command prompt
    • No external dependencies required
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
    print("🚀 Starting Terminal Version...\n")
    input("Press Enter to continue...")
    
    try:
        # Import and run the robust terminal typing test
        import terminal_typing_test
        terminal_typing_test.terminal_typing_test()
        
        # After terminal version finishes, show return message
        print(f"\n{'-'*60}")
        print("🎯 Terminal Typing Test completed!")
        print("🔄 Returning to main launcher menu...")
        print(f"{'-'*60}")
        input("Press Enter to return to main menu...")
        
    except ImportError:
        print("❌ Error: Could not find terminal_typing_test.py file!")
        input("Press Enter to return to main menu...")
    except Exception as e:
        print(f"❌ Error running terminal version: {e}")
        input("Press Enter to return to main menu...")

def run_gui_version():
    """Run the GUI (desktop) version"""
    print("🚀 Starting Desktop GUI Version...\n")
    print("📱 The GUI window will open in a moment...")
    input("Press Enter to continue...")
    
    try:
        import typing_test_gui
        typing_test_gui.main()
        
        # After GUI version finishes, show return message
        print(f"\n{'-'*60}")
        print("🖥️ Desktop GUI Typing Test completed!")
        print("🔄 Returning to main launcher menu...")
        print(f"{'-'*60}")
        input("Press Enter to return to main menu...")
        
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
                # Terminal version doesn't need any external dependencies
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