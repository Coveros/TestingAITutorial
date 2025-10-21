#!/usr/bin/env python3
"""
Wrapper script to run regression testing demo with correct virtual environment
This ensures the tf-keras installation in training-env is used
"""

import subprocess
import sys
import os

def main():
    """Run the regression demo with the correct virtual environment."""
    
    print("🧪 REGRESSION TESTING DEMO LAUNCHER")
    print("=" * 50)
    print()
    print("This launcher uses the training-env virtual environment")
    print("where tf-keras has been properly installed.")
    print()
    
    # Path to the virtual environment Python executable
    venv_python = r"c:\Users\jpayne\Documents\Training\Notebooks for ML classes\training-env\Scripts\python.exe"
    
    # Path to the demo script
    demo_script = os.path.join(os.path.dirname(__file__), "regression_testing", "demo_regression_testing.py")
    
    # Check if the virtual environment Python exists
    if not os.path.exists(venv_python):
        print(f"❌ Virtual environment not found at: {venv_python}")
        print("Please ensure the training-env virtual environment exists.")
        return
    
    # Check if the demo script exists
    if not os.path.exists(demo_script):
        print(f"❌ Demo script not found at: {demo_script}")
        return
    
    print(f"✅ Using Python: {venv_python}")
    print(f"✅ Running demo: {demo_script}")
    print()
    print("🚀 Launching demo...")
    print("=" * 50)
    
    try:
        # Run the demo with the virtual environment Python
        subprocess.run([venv_python, demo_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running demo: {e}")
    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()