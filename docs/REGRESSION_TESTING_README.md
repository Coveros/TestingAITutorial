# Regression Testing Framework for GenAI Systems

This comprehensive regression testing framework allows you to test GenAI systems against gold standard answers with automated pass/fail criteria, semantic similarity scoring, and quality gates.

## 🎯 Overview

Regression testing is critical for GenAI systems because:
- **Ensures consistency** - Responses should remain stable across system changes
- **Validates quality** - Compares outputs to expert-curated gold standards  
- **Enables automation** - Pass/fail criteria allow for CI/CD integration
- **Tracks performance** - Monitors degradation over time

## 📁 Files Overview

### Core Framework
- **`regression_testing.py`** - Main regression testing framework
- **`regression_config.json`** - Configuration file for thresholds and settings
- **`demo_regression_testing.py`** - Interactive demo and tutorial

### Test Infrastructure  
- **`tests/test_regression_framework.py`** - Unit tests for the framework
- **`regression_test_results/`** - Directory for saved test results (auto-created)

## 🚀 Quick Start

### 1. Basic Usage

```python
from regression_testing import run_regression_tests

# Run full regression test suite
results = run_regression_tests()

# Run quick test (high priority only)
from regression_testing import run_quick_regression
results = run_quick_regression()
```

### 2. From Command Line

```bash
# Full regression test
python regression_testing.py

# Quick regression test  
python regression_testing.py --quick

# Compare with baseline
python regression_testing.py --baseline regression_test_results/baseline.json
```

### 3. Interactive Demo

```bash
python demo_regression_testing.py
```

### 4. Integrated in Experiments

```bash
python run_experiments.py
# Select option 7 for regression testing
```

## 📊 Understanding the Metrics

### Semantic Similarity (40% weight)
- **What**: Measures how similar the response meaning is to gold standard
- **Range**: 0.0 - 1.0 (higher is better)
- **Threshold**: 0.75 (default)
- **Method**: Uses sentence-transformers or fallback string similarity

### Keyword Match (25% weight)  
- **What**: Percentage of expected keywords found in response
- **Range**: 0.0 - 1.0 (higher is better)
- **Threshold**: 0.6 (default)
- **Purpose**: Ensures key concepts are mentioned

### Length Appropriateness (15% weight)
- **What**: Whether response length is within expected range
- **Calculation**: Based on expected_length_range in test cases
- **Tolerance**: ±30% by default
- **Purpose**: Prevents too short or excessively long responses

### Source Quality (10% weight)
- **What**: Whether sufficient source documents are provided
- **Minimum**: 1 source (default)
- **Purpose**: Ensures responses are grounded in retrieved content

### Performance (5% weight)
- **What**: Response time within acceptable limits
- **Threshold**: 5.0 seconds (default)
- **Purpose**: Ensures system performance requirements

### Content Quality (5% weight)
- **What**: Basic content validation (minimum length, no error messages)
- **Purpose**: Catches obvious failures and empty responses

## 🎯 Test Cases Structure

Each test case includes:

```python
{
    'id': 'unique_identifier',
    'category': 'factual|technical|process|deployment|metrics|edge_case',
    'query': 'The question to ask the system',
    'gold_standard': 'Expert-curated correct answer',
    'keywords': ['expected', 'key', 'terms'],
    'expected_length_range': (min_chars, max_chars),
    'priority': 'high|medium|low'
}
```

### Current Test Cases

1. **hallucination_basic** (high) - Tests understanding of hallucination concept
2. **rag_evaluation** (high) - Tests knowledge of RAG evaluation methods  
3. **testing_best_practices** (medium) - Tests GenAI testing best practices
4. **production_deployment** (medium) - Tests production deployment considerations
5. **evaluation_metrics** (high) - Tests understanding of AI metrics
6. **edge_case_empty** (low) - Tests empty query handling
7. **edge_case_irrelevant** (medium) - Tests irrelevant query handling

## ⚙️ Configuration

Edit `regression_config.json` to customize:

### Thresholds
```json
{
  "semantic_similarity_threshold": 0.75,
  "keyword_match_threshold": 0.6,
  "response_time_threshold": 5.0,
  "minimum_response_length": 50
}
```

### Environment-Specific Settings
- **Development** - Relaxed thresholds for testing
- **Staging** - Standard thresholds  
- **Production** - Strict thresholds for deployment

### Quality Gate Criteria
- Minimum pass rate: 80%
- Allow critical failures: false
- Minimum average similarity: 0.75

## 🚪 Quality Gates

Quality gates determine if your system is ready for deployment:

### Automatic Pass Criteria
✅ **Pass Rate ≥ 80%** - Most tests must pass  
✅ **No Critical Failures** - All high-priority tests must pass  
✅ **Average Similarity ≥ Threshold** - Overall quality must meet standards

### Quality Gate Assessment
```
🚪 QUALITY GATE ASSESSMENT:
   ✅ QUALITY GATE PASSED - Ready for deployment
```

or

```
🚪 QUALITY GATE ASSESSMENT:  
   ❌ QUALITY GATE FAILED - Issues need resolution
     • Overall pass rate too low
     • Critical test failures present
```

## 📈 Regression Detection

Compare current results with baseline to detect regressions:

```python
from regression_testing import compare_regression_results

compare_regression_results('baseline.json', current_results)
```

Tracks changes in:
- Pass rate
- Semantic similarity  
- Keyword matching
- Response times
- Overall scores

## 🔬 Advanced Usage

### Custom Test Cases

Add your own test cases:

```python
framework = RegressionTestFramework()
framework.test_cases.append({
    'id': 'custom_test',
    'category': 'custom',
    'query': 'Your custom question',
    'gold_standard': 'Expected answer',
    'keywords': ['key', 'terms'],
    'expected_length_range': (100, 300),
    'priority': 'medium'
})
```

### Custom Similarity Models

Use different embedding models:

```python
framework = RegressionTestFramework(similarity_model="all-mpnet-base-v2")
```

### Programmatic Access

```python
# Get detailed evaluation for single test
evaluation = framework.evaluate_response_quality(test_case, response_data)

# Access individual scores
print(f"Similarity: {evaluation['semantic_similarity']:.3f}")
print(f"Keywords: {evaluation['keyword_match']:.3f}")
print(f"Passed: {evaluation['test_passed']}")
```

## 🛠️ Integration with CI/CD

### GitHub Actions Example

```yaml
- name: Run Regression Tests
  run: |
    python regression_testing.py --quick
    if [ $? -ne 0 ]; then
      echo "Regression tests failed"
      exit 1
    fi
```

### Quality Gate Script

```bash
#!/bin/bash
python regression_testing.py > results.json
if grep -q "QUALITY GATE PASSED" results.json; then
    echo "✅ Quality gate passed - deploying"
    exit 0
else
    echo "❌ Quality gate failed - blocking deployment"
    exit 1
fi
```

## 📊 Results and Reporting

### Automatic File Saving
- **JSON Results**: `regression_test_results/regression_results_TIMESTAMP.json`
- **Summary Report**: `regression_test_results/regression_summary_TIMESTAMP.txt`

### Result Structure
```json
{
  "results": [...],  // Individual test results
  "summary": {       // Aggregated statistics
    "total_tests": 7,
    "passed_tests": 6,
    "pass_rate": 0.857,
    "avg_semantic_similarity": 0.782
  },
  "config": {...}    // Configuration used
}
```

## 🎓 Educational Value

This framework teaches:

1. **Gold Standard Evaluation** - How to create and use reference answers
2. **Semantic Similarity** - Understanding meaning-based comparisons vs. string matching  
3. **Multi-Metric Assessment** - Combining different quality dimensions
4. **Threshold Setting** - Balancing strictness vs. practicality
5. **Quality Gates** - Implementing automated go/no-go decisions
6. **Regression Detection** - Monitoring system degradation over time

## 🤝 Contributing

To add new test cases:
1. Add to the `test_cases` list in `RegressionTestFramework._load_test_cases()`
2. Include all required fields
3. Test with the demo framework
4. Update this documentation

## 🔧 Troubleshooting

### Common Issues

**Import Error**: `sentence-transformers not available`
```bash
pip install sentence-transformers
```

**Low Similarity Scores**: Check if your gold standards are too different from actual responses
- Review gold standard quality
- Adjust similarity thresholds
- Check embedding model choice

**All Tests Failing**: Verify system is running correctly
- Test individual queries manually
- Check error messages in detailed results
- Validate test case format

### Debugging Tips

1. **Use Demo Mode**: `python demo_regression_testing.py` for interactive testing
2. **Check Individual Tests**: Run single test demonstration to debug specific cases
3. **Review Detailed Results**: Examine JSON output for specific failure reasons
4. **Validate Framework**: Run `tests/test_regression_framework.py` to check framework functionality

---

🎯 **Remember**: Regression testing is most effective when:
- Gold standards are created by domain experts
- Test cases cover diverse scenarios including edge cases  
- Thresholds are tuned to your specific requirements
- Tests are run consistently as part of your development workflow