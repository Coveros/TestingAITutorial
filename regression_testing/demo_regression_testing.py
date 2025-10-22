#!/usr/bin/env python3
"""
Regression Testing Demo

This script demonstrates the regression testing framework
and shows how to use it for GenAI system validation.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def demo_regression_testing():
    """Demonstrate the regression testing framework."""
    
    print("🧪 REGRESSION TESTING DEMO")
    print("=" * 60)
    print()
    print("This demo shows how to use regression testing for GenAI systems.")
    print("Regression testing compares system responses to 'gold standard' answers")
    print("using semantic similarity and other quality metrics.")
    print()
    
    # Import the regression testing framework
    try:
        from regression_testing import RegressionTestFramework, run_regression_tests, run_quick_regression
        print("✅ Regression testing framework loaded successfully!")
    except ImportError as e:
        print(f"❌ Failed to import regression testing: {str(e)}")
        return
    
    print("\n📋 Available Test Cases:")
    framework = RegressionTestFramework()
    
    for i, test_case in enumerate(framework.test_cases, 1):
        print(f"{i}. {test_case['id']} ({test_case['category']}, {test_case['priority']} priority)")
        print(f"   Query: {test_case['query'][:60]}{'...' if len(test_case['query']) > 60 else ''}")
    
    print(f"\n🎯 Current Configuration:")
    config = framework.config
    print(f"   Semantic Similarity Threshold: {config['semantic_similarity_threshold']}")
    print(f"   Keyword Match Threshold: {config['keyword_match_threshold']}")
    print(f"   Response Time Threshold: {config['response_time_threshold']}s")
    print(f"   Minimum Response Length: {config['minimum_response_length']} chars")
    
    print(f"\n🤖 Available Similarity Models:")
    try:
        from sentence_transformers import SentenceTransformer
        print("   ✅ sentence-transformers available")
        print("   📊 Using semantic similarity for accurate comparisons")
    except ImportError:
        print("   ⚠️  sentence-transformers not available")
        print("   📊 Using fallback string similarity methods")
        print("   💡 Install with: pip install sentence-transformers")
    
    print(f"\n🔄 Demo Options:")
    print("1. Run quick regression test (high priority tests only)")
    print("2. Run single test case demonstration")
    print("3. Show test case details")
    print("4. Validate framework functionality")
    print("0. Exit demo")
    
    while True:
        try:
            choice = input("\nSelect demo option (0-4): ").strip()
            
            if choice == "0":
                print("👋 Demo completed!")
                break
                
            elif choice == "1":
                print("\n🏃‍♂️ Running quick regression test...")
                results = run_quick_regression()
                
                print(f"\n📊 Quick Results Summary:")
                summary = results['summary']
                print(f"   Pass Rate: {summary['pass_rate']:.1%}")
                print(f"   Avg Similarity: {summary['avg_semantic_similarity']:.3f}")
                print(f"   Critical Failures: {summary['critical_failures']}")
                
            elif choice == "2":
                print("\n🔍 Single Test Demonstration:")
                test_case = framework.test_cases[0]  # Use first test case
                
                print(f"Testing: {test_case['id']}")
                print(f"Query: {test_case['query']}")
                print(f"Expected keywords: {', '.join(test_case['keywords'][:3])}...")
                
                try:
                    response_data = framework.pipeline.query(test_case['query'])
                    evaluation = framework.evaluate_response_quality(test_case, response_data)
                    
                    print(f"\n📝 Response: {response_data['response'][:100]}...")
                    print(f"🎯 Semantic Similarity: {evaluation['semantic_similarity']:.3f}")
                    print(f"🔑 Keyword Match: {evaluation['keyword_match']:.3f}")
                    print(f"📊 Overall Score: {evaluation['overall_score']:.3f}")
                    print(f"✅ Test {'PASSED' if evaluation['test_passed'] else 'FAILED'}")
                    
                except Exception as e:
                    print(f"❌ Error running test: {str(e)}")
            
            elif choice == "3":
                print("\n📋 Test Case Details:")
                for test_case in framework.test_cases:
                    print(f"\n🔍 {test_case['id']} ({test_case['priority']} priority)")
                    print(f"   Category: {test_case['category']}")
                    print(f"   Query: {test_case['query']}")
                    print(f"   Gold Standard: {test_case['gold_standard'][:100]}...")
                    print(f"   Keywords: {', '.join(test_case['keywords'])}")
                    print(f"   Expected Length: {test_case['expected_length_range'][0]}-{test_case['expected_length_range'][1]} chars")
            
            elif choice == "4":
                print("\n🧪 Validating Framework...")
                try:
                    from tests.test_regression_framework import run_framework_tests
                    success = run_framework_tests()
                    if success:
                        print("✅ Framework validation successful!")
                    else:
                        print("❌ Framework validation found issues!")
                except ImportError:
                    print("❌ Test framework not available")
                except Exception as e:
                    print(f"❌ Validation error: {str(e)}")
            
            else:
                print("❌ Invalid choice. Please select 0-4.")
                
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted!")
            break
        except Exception as e:
            print(f"❌ Demo error: {str(e)}")

def show_regression_testing_guide():
    """Show a guide for using regression testing effectively."""
    
    print("\n📚 REGRESSION TESTING GUIDE")
    print("=" * 50)
    print()
    print("🎯 WHAT IS REGRESSION TESTING?")
    print("Regression testing ensures that changes to your GenAI system")
    print("don't break existing functionality. It compares current responses")
    print("to established 'gold standard' answers using multiple metrics.")
    print()
    print("📊 KEY METRICS:")
    print("1. Semantic Similarity - How similar is the meaning?")
    print("2. Keyword Match - Does it contain expected terms?")
    print("3. Length Appropriateness - Is the response the right length?")
    print("4. Source Quality - Are enough sources provided?")
    print("5. Performance - Does it respond quickly enough?")
    print()
    print("🚪 QUALITY GATES:")
    print("Quality gates are pass/fail criteria that determine if your")
    print("system is ready for deployment:")
    print("• Pass rate >= 80%")
    print("• No critical test failures")
    print("• Average similarity >= threshold")
    print()
    print("🔄 WHEN TO RUN REGRESSION TESTS:")
    print("• Before deploying changes to production")
    print("• After optimizing system parameters")
    print("• During continuous integration")
    print("• When investigating quality issues")
    print()
    print("💡 BEST PRACTICES:")
    print("1. Create gold standards based on domain expertise")
    print("2. Include diverse test cases (edge cases, typical use)")
    print("3. Set realistic thresholds based on your requirements")
    print("4. Regularly update test cases as system evolves")
    print("5. Use baseline comparisons to detect regressions")
    print()
    print("🛠️ CUSTOMIZATION:")
    print("Edit regression_config.json to customize:")
    print("• Similarity thresholds")
    print("• Scoring weights")
    print("• Quality gate criteria")
    print("• Environment-specific settings")

if __name__ == "__main__":
    print("🎓 REGRESSION TESTING FOR GENAI SYSTEMS")
    print("=" * 70)
    print()
    print("Welcome to the regression testing educational module!")
    print("This demo will teach you about testing GenAI systems against")
    print("gold standard answers with automated pass/fail criteria.")
    print()
    
    print("What would you like to learn about?")
    print("1. Run interactive regression testing demo")
    print("2. Learn about regression testing concepts")
    print("3. Both - concepts first, then demo")
    print("0. Exit")
    
    choice = input("\nSelect option (0-3): ").strip()
    
    if choice == "1":
        demo_regression_testing()
    elif choice == "2":
        show_regression_testing_guide()
    elif choice == "3":
        show_regression_testing_guide()
        input("\nPress Enter to start the demo...")
        demo_regression_testing()
    elif choice == "0":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")