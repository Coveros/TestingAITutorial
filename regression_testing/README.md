# Regression Testing Package

This package provides comprehensive regression testing capabilities for GenAI systems with gold standard answer comparison and quality gates.

## 📁 Files

- **`regression_testing.py`** - Core regression testing framework
- **`demo_regression_testing.py`** - Interactive demo and tutorial
- **`config.json`** - Configurable testing thresholds and settings
- **`results/`** - Auto-generated test results directory (created at runtime)

## 🚀 Usage

### From project root:
```bash
python -m regression_testing.regression_testing
```

### From regression_testing directory:
```bash
cd regression_testing
python regression_testing.py
```

### Interactive demo:
```bash
python -m regression_testing.demo_regression_testing
```

### Quick regression test:
```bash
python regression_testing.py --quick
```

## 🎯 Key Features

- **Gold Standard Comparison** - Test against expert-curated answers
- **Semantic Similarity Scoring** - Meaning-based response evaluation
- **Pass/Fail Thresholds** - Configurable quality gates
- **Quality Gate Assessment** - Deployment readiness evaluation
- **Baseline Comparison** - Regression detection over time
- **Comprehensive Reporting** - JSON results and human-readable summaries

## 📊 Quality Metrics

- **Semantic Similarity** (40% weight) - Meaning comparison using embeddings
- **Keyword Match** (25% weight) - Expected terminology validation
- **Length Appropriateness** (15% weight) - Response length validation
- **Source Quality** (10% weight) - Adequate source validation
- **Performance** (5% weight) - Response time validation
- **Content Quality** (5% weight) - Basic content validation

See the main documentation in `docs/REGRESSION_TESTING_README.md` for detailed information.