#!/usr/bin/env python3
"""
Quick launcher for GenAI Testing Tutorial experiments.

This script provides easy access to all testing and experiment capabilities
in the reorganized project structure.
"""

import os
import sys
import subprocess

def show_menu():
    """Show main menu."""
    print("🧪 GenAI Testing Tutorial - Quick Launcher")
    print("=" * 60)
    print()
    print("1. 🔬 Run Optimization Experiments")
    print("   Interactive menu-driven experiments")
    print()
    print("2. 🧪 Run Regression Testing")
    print("   Test against gold standards with quality gates")
    print()
    print("3. 🎮 Regression Testing Demo")
    print("   Interactive tutorial and framework validation")
    print()
    print("4. 🧑‍💻 Run Unit Tests")
    print("   Traditional pytest-based testing")
    print()
    print("5. 📊 Run Evaluation Framework")
    print("   Advanced quality assessment tools")
    print()
    print("6. 🚀 Start Flask Application")
    print("   Launch the chat interface")
    print()
    print("7. 🧪 Lightweight Regression Demo")
    print("   Works without heavy dependencies")
    print()
    print("8. 📚 Open Documentation")
    print("   View comprehensive guides and documentation")
    print()
    print("0. Exit")
    print()

def run_experiments():
    """Launch optimization experiments."""
    print("🔬 Launching Optimization Experiments...")
    try:
        subprocess.run([sys.executable, "-m", "experiments.run_experiments"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running experiments: {e}")
    except FileNotFoundError:
        print("❌ Python not found. Make sure Python is in your PATH.")

def run_regression_testing():
    """Launch regression testing."""
    print("🧪 Launching Regression Testing...")
    venv_python = r"c:\Users\jpayne\Documents\Training\Notebooks for ML classes\training-env\Scripts\python.exe"
    
    if os.path.exists(venv_python):
        print("Using training-env virtual environment with tf-keras...")
        try:
            subprocess.run([venv_python, "-m", "regression_testing.regression_testing"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running regression tests: {e}")
    else:
        try:
            subprocess.run([sys.executable, "-m", "regression_testing.regression_testing"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running regression tests: {e}")
        except FileNotFoundError:
            print("❌ Python not found. Make sure Python is in your PATH.")

def run_regression_demo():
    """Launch regression testing demo."""
    print("🎮 Launching Regression Testing Demo...")
    venv_python = r"c:\Users\jpayne\Documents\Training\Notebooks for ML classes\training-env\Scripts\python.exe"
    
    if os.path.exists(venv_python):
        print("Using training-env virtual environment with tf-keras...")
        try:
            demo_path = os.path.join(os.path.dirname(__file__), "regression_testing", "demo_regression_testing.py")
            subprocess.run([venv_python, demo_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running regression demo: {e}")
    else:
        try:
            subprocess.run([sys.executable, "-m", "regression_testing.demo_regression_testing"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running regression demo: {e}")
        except FileNotFoundError:
            print("❌ Python not found. Make sure Python is in your PATH.")

def run_unit_tests():
    """Run unit tests."""
    print("🧑‍💻 Running Unit Tests...")
    try:
        subprocess.run([sys.executable, "-m", "pytest", "tests/test_rag_pipeline.py", "-v"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running unit tests: {e}")
        print("Make sure pytest is installed: pip install pytest")
    except FileNotFoundError:
        print("❌ Python not found. Make sure Python is in your PATH.")

def run_evaluation_framework():
    """Run evaluation framework."""
    print("📊 Running Evaluation Framework...")
    try:
        subprocess.run([sys.executable, "tests/evaluation_framework.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running evaluation framework: {e}")
    except FileNotFoundError:
        print("❌ Python not found. Make sure Python is in your PATH.")

def start_flask_app():
    """Start the Flask application."""
    print("🚀 Starting Flask Application...")
    print("The chat interface will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server.")
    try:
        subprocess.run([sys.executable, "run.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting Flask app: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
    except FileNotFoundError:
        print("❌ Python not found. Make sure Python is in your PATH.")

def run_lightweight_demo():
    """Run lightweight regression testing demo."""
    print("🧪 Launching Lightweight Regression Demo...")
    try:
        subprocess.run([sys.executable, "lightweight_regression_demo.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running lightweight demo: {e}")
    except FileNotFoundError:
        print("❌ Python not found. Make sure Python is in your PATH.")

def open_documentation():
    """Show documentation options."""
    print("📚 Available Documentation:")
    print()
    print("Main documentation files:")
    print("• README.md - Main project overview (this directory)")
    print("• docs/EXPERIMENTS_README.md - Detailed experiment guide")
    print("• docs/REGRESSION_TESTING_README.md - Regression testing guide")
    print("• docs/STUDENT_GUIDE.md - Complete student tutorial")
    print("• docs/PROJECT_PLAN.md - Implementation details")
    print("• experiments/README.md - Experiments package overview")
    print("• regression_testing/README.md - Regression testing overview")
    print()
    print("Online documentation:")
    print("• Open any .md file in a text editor or markdown viewer")
    print("• Use VS Code or similar for best viewing experience")
    
    # Try to open main README
    doc_choice = input("Open main README.md? (y/n): ").strip().lower()
    if doc_choice == 'y':
        try:
            if os.name == 'nt':  # Windows
                os.startfile("README.md")
            elif os.name == 'posix':  # macOS and Linux
                subprocess.run(["open", "README.md"], check=True)
        except Exception as e:
            print(f"❌ Could not open README.md automatically: {e}")
            print("Please open README.md in your preferred text editor.")

def main():
    """Main launcher."""
    while True:
        show_menu()
        
        try:
            choice = input("Select option (0-8): ").strip()
            
            if choice == "0":
                print("👋 Happy testing! Remember to explore all the testing approaches!")
                break
            elif choice == "1":
                run_experiments()
            elif choice == "2":
                run_regression_testing()
            elif choice == "3":
                run_regression_demo()
            elif choice == "4":
                run_unit_tests()
            elif choice == "5":
                run_evaluation_framework()
            elif choice == "6":
                start_flask_app()
            elif choice == "7":
                run_lightweight_demo()
            elif choice == "8":
                open_documentation()
            else:
                print("❌ Invalid choice. Please select 0-8.")
            
            if choice != "0" and choice != "6":  # Don't pause after Flask app
                input("\nPress Enter to return to menu...")
                print("\n" + "="*80)
                
        except KeyboardInterrupt:
            print("\n\n👋 Launcher interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("🔧 GenAI Testing Tutorial Quick Launcher")
    print("Working directory:", os.getcwd())
    print()
    
    main()