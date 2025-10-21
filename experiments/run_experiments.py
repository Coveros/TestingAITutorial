#!/usr/bin/env python3
"""
Master Experiment Runner for GenAI Testing Tutorial

This script provides a menu-driven interface for students to run
different optimization experiments and learn about GenAI system testing.

🎯 Learning Objectives:
- Systematic approach to GenAI system optimization
- Understanding component interactions and trade-offs
- Hands-on experience with different testing methodologies
- Practice with performance measurement and analysis
"""

import os
import sys

# Add parent directory to path to import other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def print_banner():
    """Print welcome banner."""
    print("=" * 80)
    print("🧪 GenAI Testing Tutorial - Optimization Experiments")
    print("=" * 80)
    print("Welcome! This tutorial teaches you how to test and optimize")
    print("Retrieval-Augmented Generation (RAG) systems through hands-on experiments.")
    print()
    print("Each experiment focuses on a different aspect of the system:")
    print("• Chunking Strategy - How documents are split affects retrieval")
    print("• Embedding Models - Which model creates the best representations")
    print("• Generation Parameters - How to optimize response quality")
    print("• Retrieval Strategy - Finding the right documents efficiently")
    print("• System Integration - Combining optimizations for best results")
    print()

def print_menu():
    """Print experiment menu."""
    print("📋 Available Experiments:")
    print()
    print("1. 🔄 Chunking Strategy Optimization")
    print("   Learn how document chunking affects similarity scores")
    print("   Current issue: Chunks too large (2000 chars)")
    print()
    print("2. 🎯 Embedding Model Comparison") 
    print("   Compare different embedding models for retrieval quality")
    print("   Current issue: May have dimension compatibility issues")
    print()
    print("3. ⚙️  Generation Parameters Tuning")
    print("   Optimize response length and consistency")
    print("   Current issues: max_tokens=300 (too short), temperature=0.7 (inconsistent)")
    print()
    print("4. 🔍 Retrieval Strategy Optimization")
    print("   Find optimal number of documents and filtering")
    print("   Current issue: No similarity filtering, fixed retrieval count")
    print()
    print("5. 🚀 End-to-End System Optimization")
    print("   Compare baseline vs fully optimized system")
    print("   Systematic evaluation of all improvements combined")
    print()
    print("6. 📊 Run All Experiments (Full Tutorial)")
    print("   Complete optimization workflow - recommended for learning")
    print()
    print("7. 🧪 Regression Testing with Gold Standards")
    print("   Test system against gold standard answers with pass/fail criteria")
    print("   Includes semantic similarity scoring and quality gates")
    print()
    print("8. ❓ Help - Understanding the Issues")
    print("   Learn about each intentional issue in the system")
    print()
    print("9. 🔧 Quick Fix Implementation Guide")
    print("   Step-by-step guide to implement optimizations")
    print()
    print("0. Exit")
    print()

def run_chunking_experiments():
    """Run chunking optimization experiments."""
    print("\n🔄 Starting Chunking Strategy Experiments...")
    try:
        from experiments import chunking_experiments
        chunking_experiments.run_chunking_experiments()
    except ImportError:
        print("❌ chunking_experiments.py not found!")
    except Exception as e:
        print(f"❌ Error running chunking experiments: {str(e)}")

def run_embedding_experiments():
    """Run embedding model experiments."""
    print("\n🎯 Starting Embedding Model Experiments...")
    try:
        from experiments import embedding_experiments
        embedding_experiments.run_embedding_experiments()
    except ImportError:
        print("❌ embedding_experiments.py not found!")
    except Exception as e:
        print(f"❌ Error running embedding experiments: {str(e)}")

def run_generation_experiments():
    """Run generation parameter experiments."""
    print("\n⚙️ Starting Generation Parameters Experiments...")
    try:
        from experiments import generation_experiments
        generation_experiments.run_generation_experiments()
    except ImportError:
        print("❌ generation_experiments.py not found!")
    except Exception as e:
        print(f"❌ Error running generation experiments: {str(e)}")

def run_retrieval_experiments():
    """Run retrieval strategy experiments."""
    print("\n🔍 Starting Retrieval Strategy Experiments...")
    try:
        from experiments import retrieval_experiments
        retrieval_experiments.run_retrieval_experiments()
    except ImportError:
        print("❌ retrieval_experiments.py not found!")
    except Exception as e:
        print(f"❌ Error running retrieval experiments: {str(e)}")

def run_regression_tests():
    """Run regression tests with gold standard comparison."""
    print("\n🧪 Starting Regression Testing with Gold Standards...")
    try:
        from regression_testing import regression_testing
        
        print("\nSelect regression test type:")
        print("1. Full regression test suite")
        print("2. Quick regression test (high priority only)")
        print("3. Test framework validation")
        
        choice = input("Choose test type (1-3): ").strip()
        
        if choice == "1":
            print("\n🔄 Running full regression test suite...")
            results = regression_testing.run_regression_tests()
            
        elif choice == "2":
            print("\n🏃‍♂️ Running quick regression test...")
            results = regression_testing.run_quick_regression()
            
        elif choice == "3":
            print("\n🧪 Running framework validation tests...")
            from tests.test_regression_framework import run_framework_tests
            success = run_framework_tests()
            if success:
                print("\n✅ Framework validation completed successfully!")
            else:
                print("\n❌ Framework validation found issues!")
            return
        else:
            print("❌ Invalid choice. Returning to menu.")
            return
        
        # Ask about baseline comparison
        baseline_choice = input("\nCompare with baseline results? (y/n): ").strip().lower()
        if baseline_choice == 'y':
            baseline_file = input("Enter baseline results file path: ").strip()
            if baseline_file and os.path.exists(baseline_file):
                regression_testing.compare_regression_results(baseline_file, results)
            else:
                print("❌ Baseline file not found or not specified.")
        
    except ImportError:
        print("❌ regression_testing.py not found!")
        print("Make sure the regression testing framework is available.")
    except Exception as e:
        print(f"❌ Error running regression tests: {str(e)}")

def run_system_experiments():
    """Run end-to-end system experiments."""
    print("\n🚀 Starting End-to-End System Experiments...")
    try:
        from experiments import system_optimization_experiments
        system_optimization_experiments.run_optimization_experiments()
    except ImportError:
        print("❌ system_optimization_experiments.py not found!")
    except Exception as e:
        print(f"❌ Error running system experiments: {str(e)}")

def run_all_experiments():
    """Run complete tutorial workflow."""
    print("\n🧪 COMPLETE OPTIMIZATION TUTORIAL")
    print("=" * 60)
    print("Running all experiments in recommended order...")
    print("This will take several minutes - grab a coffee! ☕")
    print()
    
    experiments = [
        ("Chunking Strategy", run_chunking_experiments),
        ("Embedding Models", run_embedding_experiments),
        ("Generation Parameters", run_generation_experiments),
        ("Retrieval Strategy", run_retrieval_experiments),
        ("End-to-End Optimization", run_system_experiments),
    ]
    
    for name, func in experiments:
        print(f"\n{'='*20} {name} {'='*20}")
        try:
            func()
            print(f"\n✅ {name} experiments completed!")
        except Exception as e:
            print(f"\n❌ {name} experiments failed: {str(e)}")
        
        input("\nPress Enter to continue to next experiment...")
    
    print("\n🏆 TUTORIAL COMPLETED!")
    print("You've now explored all aspects of RAG system optimization.")
    print("Use option 9 for implementation guidance.")

def show_help():
    """Show detailed help about the issues."""
    print("\n❓ UNDERSTANDING THE INTENTIONAL ISSUES")
    print("=" * 60)
    print()
    print("This RAG system has several intentional issues for educational purposes:")
    print()
    print("🔄 CHUNKING ISSUES:")
    print("   • Problem: chunk_size=2000 (too large)")
    print("   • Impact: Reduces embedding focus, lowers similarity scores")
    print("   • Location: app/rag_pipeline.py, _split_text method")
    print("   • Fix: Try 300-600 character chunks")
    print()
    print("🎯 EMBEDDING ISSUES:")
    print("   • Problem: Using models with incompatible dimensions")
    print("   • Impact: Dimension mismatch errors, failed queries")
    print("   • Location: app/rag_pipeline.py, _generate_embeddings method")
    print("   • Fix: Use consistent 'embed-english-v3.0' model (1024 dims)")
    print()
    print("⚙️ GENERATION ISSUES:")
    print("   • Problem 1: max_tokens=300 (too short for complex answers)")
    print("   • Problem 2: temperature=0.7 (causes inconsistency)")
    print("   • Impact: Truncated responses, variable quality")
    print("   • Location: app/rag_pipeline.py, _generate_response method")
    print("   • Fix: Try max_tokens=600-800, temperature=0.2-0.3")
    print()
    print("🔍 RETRIEVAL ISSUES:")
    print("   • Problem: No similarity filtering")
    print("   • Impact: Low-quality documents included in context")
    print("   • Location: app/rag_pipeline.py, _retrieve_documents method")
    print("   • Fix: Add similarity thresholds, optimize retrieval count")
    print()
    print("💡 WHY THESE ISSUES EXIST:")
    print("   These are common real-world problems in GenAI systems!")
    print("   Learning to identify and fix them is crucial for production systems.")

def show_implementation_guide():
    """Show step-by-step implementation guide."""
    print("\n🔧 QUICK FIX IMPLEMENTATION GUIDE")
    print("=" * 60)
    print()
    print("To implement optimizations in the actual system:")
    print()
    print("📁 FILE: app/rag_pipeline.py")
    print()
    print("1️⃣ FIX CHUNKING (Line ~151, _split_text method):")
    print("   Change: chunk_size: int = 2000")
    print("   To:     chunk_size: int = 500")
    print("   Change: chunk_overlap: int = 200") 
    print("   To:     chunk_overlap: int = 50")
    print()
    print("2️⃣ FIX EMBEDDINGS (Line ~207, _generate_embeddings method):")
    print("   Change: model=\"embed-english-v2.0\"")
    print("   To:     model=\"embed-english-v3.0\"")
    print("   Also update _generate_query_embedding method (Line ~223)")
    print("   💡 This ensures consistent 1024-dimension embeddings")
    print()
    print("3️⃣ FIX GENERATION (Line ~285, _generate_response method):")
    print("   Change: max_tokens=300")
    print("   To:     max_tokens=600")
    print("   Change: temperature=0.7")
    print("   To:     temperature=0.3")
    print()
    print("4️⃣ FIX RETRIEVAL (Line ~240, _retrieve_documents method):")
    print("   Add similarity filtering logic after line 248:")
    print("   ```python")
    print("   # Filter by similarity threshold")
    print("   filtered_docs = []")
    print("   for doc, meta, dist in zip(results['documents'][0], ...):")
    print("       similarity = 1 / (1 + (dist / 100))")
    print("       if similarity >= 0.005:  # Adjust threshold as needed")
    print("           filtered_docs.append(doc)")
    print("   ```")
    print()
    print("🔄 AFTER MAKING CHANGES:")
    print("   1. Save the file")
    print("   2. Restart the Flask application")
    print("   3. Test the chat interface")
    print("   4. Run experiments to verify improvements")
    print()
    print("📊 MEASURING SUCCESS:")
    print("   • Similarity scores should increase (>0.01 is good)")
    print("   • Responses should be longer and more complete")
    print("   • System should be more consistent")

def main():
    """Main experiment runner."""
    print_banner()
    
    while True:
        print_menu()
        
        try:
            choice = input("Choose an experiment (0-9): ").strip()
            
            if choice == "0":
                print("\n👋 Happy testing! Remember to implement your optimizations!")
                break
            elif choice == "1":
                run_chunking_experiments()
            elif choice == "2":
                run_embedding_experiments()
            elif choice == "3":
                run_generation_experiments()
            elif choice == "4":
                run_retrieval_experiments()
            elif choice == "5":
                run_system_experiments()
            elif choice == "6":
                run_all_experiments()
            elif choice == "7":
                run_regression_tests()
            elif choice == "8":
                show_help()
            elif choice == "9":
                show_implementation_guide()
            else:
                print("❌ Invalid choice. Please select 0-9.")
            
            if choice != "0":
                input("\nPress Enter to return to menu...")
                print("\n" + "="*80)
                
        except KeyboardInterrupt:
            print("\n\n👋 Experiment interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()