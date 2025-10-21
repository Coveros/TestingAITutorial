# GenAI Testing Tutorial - Complete Application

## Overview

This is a complete, production-ready RAG (Retrieval-Augmented Generation) chatbot application specifically designed for teaching GenAI testing concepts. The application is **intentionally built with common issues** that students will discover during testing exercises.

## Architecture

```
Frontend (HTML/CSS/JS) → Flask Backend → RAG Pipeline → Cohere API
                                    ↓
                               ChromaDB Vector Store
                                    ↑
                            Knowledge Base Documents
```

## Quick Start

### Prerequisites
- Python 3.8+
- Cohere API key (get one at https://cohere.com/)
- 2GB+ RAM for vector database
- Windows PowerShell (for Windows users)

### Installation

1. **Clone and Navigate**
   ```bash
   cd "c:\Users\jpayne\Documents\Training\Notebooks for ML classes\TestingAITutorial"
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv training-env
   training-env\Scripts\activate  # Windows
   # source training-env/bin/activate  # macOS/Linux
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   copy .env.example .env
   # Edit .env and add your Cohere API key
   ```

5. **Run Application**
   ```bash
   python run.py
   ```

6. **Access Application**
   - Open http://localhost:5000
   - Chat interface should load
   - Try: "What are the key challenges in testing GenAI applications?"

## 🚀 Quick Start (Alternative)

For easy access to all testing capabilities, use the wrapper script for the virtual environment:

```bash
python run_demo_with_venv.py
```

Or use the quick launcher:

```bash
python launch.py
```

These provide menu-driven interfaces to:
- Run optimization experiments
- Execute regression testing
- Launch interactive demos
- Run unit tests
- Start the Flask application
- Access documentation

## Project Structure

```
TestingAITutorial/
├── app/
│   ├── __init__.py          # Python package initialization
│   ├── main.py              # Flask application and API endpoints
│   ├── rag_pipeline.py      # RAG implementation with Cohere + ChromaDB
│   └── utils.py             # Utility functions and helpers
├── static/
│   ├── css/
│   │   └── style.css        # Professional styling with animations
│   └── js/
│       └── chat.js          # Interactive chat interface logic
├── templates/
│   └── index.html           # Main chat interface template
├── data/
│   ├── documents/           # Knowledge base documents (GenAI testing content)
│   │   ├── genai_testing_guide.md
│   │   ├── faq_genai_testing.md
│   │   ├── production_best_practices.md
│   │   └── evaluation_metrics.md
│   └── chroma_db/          # Vector database storage (auto-created)
├── tests/
│   ├── test_rag_pipeline.py         # Core RAG pipeline unit tests
│   ├── test_regression_framework.py # Regression testing framework tests
│   └── evaluation_framework.py      # Advanced evaluation tools
├── experiments/             # Educational optimization experiments
│   ├── __init__.py          # Package initialization
│   ├── run_experiments.py   # Master experiment runner with menu interface
│   ├── chunking_experiments.py     # Document chunking strategy testing
│   ├── embedding_experiments.py    # Embedding model comparison testing
│   ├── generation_experiments.py   # Response generation parameter tuning
│   ├── retrieval_experiments.py    # Document retrieval optimization
│   ├── system_optimization_experiments.py  # End-to-end system optimization
│   └── README.md           # Experiments package documentation
├── regression_testing/      # Production-ready regression testing
│   ├── __init__.py         # Package initialization
│   ├── regression_testing.py       # Comprehensive regression testing framework
│   ├── demo_regression_testing.py  # Interactive regression testing demo
│   ├── config.json         # Configurable testing thresholds and settings
│   ├── results/            # Auto-generated test results (created at runtime)
│   └── README.md           # Regression testing package documentation
├── docs/                   # All project documentation
│   ├── EXPERIMENTS_README.md       # Detailed experiment documentation
│   ├── REGRESSION_TESTING_README.md # Regression testing guide
│   ├── PROJECT_PLAN.md            # Detailed implementation plan
│   ├── IMPLEMENTATION_CHECKLIST.md # Step-by-step checklist
│   └── STUDENT_GUIDE.md           # Complete student tutorial
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variable template  
├── test_environment.py     # Environment validation script
├── run.py                  # Application entry point
├── run_demo_with_venv.py   # Virtual environment wrapper for demos
├── launch.py               # Interactive launcher menu
└── README.md               # This file (main project overview)
```

## Features

### 🤖 **RAG Chatbot**
- **Cohere Integration**: Uses Cohere's embeddings and Command model
- **ChromaDB Vector Store**: Local, persistent document storage
- **LangChain Framework**: Professional RAG implementation
- **Source Attribution**: Shows retrieved documents and similarity scores
- **Real-time Performance Metrics**: Response times and statistics

### 🎨 **Professional Frontend**
- **Modern UI**: Clean, responsive design with animations
- **Real-time Chat**: WebSocket-like experience with fetch API
- **Message History**: Persistent chat sessions
- **Loading States**: Typing indicators and progress feedback
- **Statistics Dashboard**: System health and performance metrics
- **Mobile Responsive**: Works on all device sizes

### 🧪 **Comprehensive Testing Suite**
- **Import Issues Fixed**: All test files now properly handle Python imports
- **Virtual Environment Integration**: `run_demo_with_venv.py` script for seamless execution
- **Unit Tests**: Individual component testing (`tests/test_rag_pipeline.py`)
- **Integration Tests**: End-to-end API testing  
- **Regression Testing**: Gold standard answer comparison with pass/fail thresholds (`regression_testing.py`)
- **Quality Metrics**: Response relevance and accuracy scoring
- **Performance Tests**: Load testing and concurrent request handling
- **Robustness Tests**: Edge cases and adversarial inputs
- **Evaluation Framework**: Automated quality assessment tools (`tests/evaluation_framework.py`)
- **Optimization Experiments**: 5 systematic testing approaches for parameter tuning:
  - **Chunking Strategy Testing** (`chunking_experiments.py`)
  - **Embedding Model Comparison** (`embedding_experiments.py`) 
  - **Generation Parameter Tuning** (`generation_experiments.py`)
  - **Retrieval Strategy Optimization** (`retrieval_experiments.py`)
  - **End-to-End System Optimization** (`system_optimization_experiments.py`)
- **Interactive Testing Framework**: Menu-driven experiment runner (`run_experiments.py`)
- **Semantic Similarity Analysis**: Meaning-based response comparison
- **Quality Gates**: Automated deployment readiness assessment
- **Evaluation Framework**: Automated quality assessment tools

### 📚 **Rich Knowledge Base**
- **GenAI Testing Guide**: Comprehensive testing strategies
- **FAQ**: Common questions about GenAI testing
- **Best Practices**: Production deployment guidelines
- **Evaluation Metrics**: Detailed metric explanations
- **Real-world Examples**: Practical testing scenarios

## 🔬 Testing Approaches Available

This tutorial provides multiple testing methodologies to comprehensively evaluate GenAI systems:

### 🧪 **Experimental Testing** (`run_experiments.py`)
**Purpose**: Systematic parameter optimization and component analysis  
**Approach**: Interactive menu-driven experiments  
**Files**: `*_experiments.py` files for each component  
**Learn**: How different parameters affect system performance

### 🎯 **Regression Testing** (`regression_testing.py`)
**Purpose**: Production-ready quality assurance with gold standards  
**Approach**: Compare responses to expert-curated correct answers  
**Metrics**: Semantic similarity, keyword matching, quality gates  
**Learn**: Automated pass/fail criteria and deployment readiness

### ⚡ **Unit Testing** (`tests/test_rag_pipeline.py`)
**Purpose**: Component-level validation and API testing  
**Approach**: Traditional pytest-based testing  
**Coverage**: Pipeline initialization, API endpoints, core functionality  
**Learn**: Standard software testing practices for AI systems

### 📊 **Evaluation Framework** (`tests/evaluation_framework.py`)
**Purpose**: Advanced quality assessment and metrics collection  
**Approach**: Multi-dimensional response evaluation  
**Features**: Custom scoring, consistency analysis, performance profiling  
**Learn**: How to measure AI system quality beyond simple accuracy

### 🎮 **Interactive Demos** (`demo_regression_testing.py`)
**Purpose**: Hands-on learning and concept demonstration  
**Approach**: Guided tutorials with real-time feedback  
**Features**: Live testing, framework validation, educational explanations  
**Learn**: Testing concepts through practical application

## API Endpoints

### `GET /`
Main chat interface

### `POST /api/chat`
Process chat messages
```json
{
  "message": "What are the key challenges in testing GenAI?"
}
```

**Response:**
```json
{
  "response": "The key challenges in testing GenAI applications include...",
  "sources": [
    {
      "content": "GenAI testing requires...",
      "metadata": {"source": "genai_testing_guide.md"},
      "similarity": 0.87
    }
  ],
  "response_time": 1.234,
  "retrieval_time": 0.456,
  "generation_time": 0.778,
  "status": "success"
}
```

### `GET /api/health`
System health check
```json
{
  "status": "healthy",
  "rag_pipeline": "initialized",
  "cohere_api_key": "configured"
}
```

### `GET /api/stats`
Performance statistics
```json
{
  "queries_processed": 42,
  "average_response_time": 1.23,
  "documents_loaded": 156,
  "error_rate": 0.02
}
```

## Configuration

### Environment Variables (.env)
```bash
# Required
COHERE_API_KEY=your_cohere_api_key_here

# Optional
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
CHUNK_SIZE=1000
CHUNK_OVERLAP=100
MAX_RETRIEVAL_DOCS=5
SIMILARITY_THRESHOLD=0.7
LOG_LEVEL=INFO
```

### Key Parameters

| Parameter | Description | Default | Impact |
|-----------|-------------|---------|---------|
| `CHUNK_SIZE` | Document chunk size for embeddings | 1000 | Affects retrieval granularity |
| `CHUNK_OVERLAP` | Overlap between chunks | 100 | Prevents information loss |
| `MAX_RETRIEVAL_DOCS` | Number of documents retrieved | 5 | Balances context vs. performance |
| `SIMILARITY_THRESHOLD` | Minimum similarity for retrieval | 0.7 | Filters irrelevant documents |

## Intentional Issues for Discovery

This application includes several intentional issues that represent common problems in production GenAI systems:

### 🐛 **Retrieval Issues**
1. **Suboptimal Chunk Size**: Chunks may be too large for effective retrieval
2. **Low Similarity Thresholds**: May retrieve irrelevant documents
3. **Outdated Embedding Model**: Using older Cohere model instead of latest

### 🤔 **Generation Issues**  
1. **Prompt Engineering**: Prompt may not effectively prevent hallucination
2. **Temperature Settings**: May be too high, causing inconsistency
3. **Max Token Limits**: May cut off responses prematurely

### ⚡ **Performance Issues**
1. **Inefficient Processing**: Some operations may be unnecessarily slow
2. **Memory Usage**: Vector database operations may not be optimized
3. **Concurrent Handling**: May not scale well under load

### 🎯 **Quality Issues**
1. **Response Consistency**: Similar queries may get very different responses
2. **Source Attribution**: Attribution accuracy may be questionable
3. **Edge Case Handling**: May not gracefully handle unusual inputs

## Testing Strategies

### 📊 **Quality Metrics**
- **Response Relevance**: Semantic similarity to expected answers
- **Faithfulness**: Grounding in retrieved documents
- **Consistency**: Similar responses to similar queries
- **Completeness**: Adequate depth and coverage

### 🔍 **Discovery Methods**
- **Behavioral Analysis**: Compare responses across similar queries
- **Code Review**: Examine parameters and configuration
- **Performance Profiling**: Measure component timing
- **Edge Case Testing**: Unusual inputs and adversarial queries

### 🛠 **Tools Provided**
- **Automated Test Suite**: `tests/test_rag_pipeline.py`
- **Evaluation Framework**: `tests/evaluation_framework.py`
- **Performance Benchmarks**: Built-in timing and statistics
- **Quality Scorers**: Response quality assessment functions

## Usage Examples

### Basic Chat Testing
```bash
curl -X POST http://localhost:5000/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "What is hallucination in GenAI?"}'
```

### Running Test Suite
```bash
# Install pytest if not included
pip install pytest

# Run all tests (with proper imports fixed)
python tests/test_rag_pipeline.py
python tests/test_regression_framework.py

# Or using pytest
python -m pytest tests/test_rag_pipeline.py -v
python -m pytest tests/test_regression_framework.py -v

# Run evaluation framework
python tests/evaluation_framework.py
```

### Running Experiments
```bash
# Interactive experiment menu
python -m experiments.run_experiments

# Individual experiments
python -m experiments.chunking_experiments
python -m experiments.embedding_experiments
python -m experiments.generation_experiments
python -m experiments.retrieval_experiments
python -m experiments.system_optimization_experiments
```

### Running Regression Tests
```bash
# Full regression test suite
python regression_testing/regression_testing.py

# Interactive demo (recommended - uses correct virtual environment)
python run_demo_with_venv.py
# Then select option 4 for framework validation

# Or run demo directly
python regression_testing/demo_regression_testing.py

# Quick regression test
python regression_testing/regression_testing.py --quick
```

### Quality Assessment
```python
from tests.evaluation_framework import EvaluationFramework
from app.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()
evaluator = EvaluationFramework(pipeline)

# Run comprehensive evaluation
results = evaluator.evaluate_response_quality([
    {"query": "What is GenAI testing?", "expected_topics": ["testing", "genai"]}
])

print(f"Average Quality Score: {results['average_quality_score']}")
```

### Regression Testing Integration
```python
from regression_testing.regression_testing import RegressionTestFramework

# Create framework
framework = RegressionTestFramework()

# Run tests programmatically
results = framework.run_regression_tests(save_results=True)

# Check quality gate
gate_passed = (
    results['summary']['pass_rate'] >= 0.8 and 
    results['summary']['critical_failures'] == 0
)

print(f"Quality Gate: {'PASSED' if gate_passed else 'FAILED'}")
```

## Learning Paths

### 🎓 **Beginner Track**
1. Explore the chat interface and basic functionality
2. Run simple API tests with curl
3. Use the provided test suite to understand testing concepts
4. Run experiments to see optimization effects

### 🔬 **Intermediate Track**  
1. Analyze the evaluation framework results
2. Run regression tests and understand quality metrics
3. Write custom test cases for specific scenarios
4. Investigate performance bottlenecks
5. Examine retrieval quality and source attribution

### 🚀 **Advanced Track**
1. Discover and document intentional issues using experiments
2. Propose and implement fixes in the actual system
3. Create custom regression test cases with gold standards
4. Develop custom evaluation metrics and quality gates
3. Develop custom evaluation metrics
4. Design production monitoring strategies

## Troubleshooting

### Common Setup Issues

**"ModuleNotFoundError: No module named 'app' or 'regression_testing'"**
- Import issues have been FIXED in the test files  
- Tests now properly add the project root to Python path
- Use `python tests/test_rag_pipeline.py` or `python tests/test_regression_framework.py`

**"KeyError: 'failed_tests' or 'avg_response_length'"**
- These issues have been FIXED in the test framework
- Test data now includes all required keys for proper execution

**"Import cohere could not be resolved"**
- Ensure virtual environment is activated: `training-env\Scripts\activate`
- Run `pip install -r requirements.txt`
- Use `run_demo_with_venv.py` for automatic virtual environment handling

**"tf-keras compatibility issues with Keras 3"**
- tf-keras has been added to requirements.txt
- Virtual environment should install tf-keras>=2.15.0 automatically  
- This resolves Keras 3 compatibility issues in the regression testing framework

**"COHERE_API_KEY not found"**
- Copy `.env.example` to `.env`
- Add your Cohere API key to the `.env` file

**"ChromaDB initialization failed"**
- Ensure you have write permissions in the project directory
- Delete `data/chroma_db/` folder and restart if corrupted

**"Flask app won't start"**
- Check that port 5000 is available
- Set `FLASK_PORT=5001` in `.env` to use a different port

### Performance Issues

**Slow first response**
- First query initializes the vector database (expected delay)
- Subsequent queries should be faster

**High memory usage**
- ChromaDB loads embeddings into memory
- Reduce document collection size if needed

### Quality Issues

**Poor response quality**
- This may be intentional! Part of the learning exercise
- Check if you're discovering the planted issues correctly

**Off-topic responses**
- Test the system's domain boundaries
- Document cases where it should vs. shouldn't know answers

## Educational Value

This application provides hands-on experience with:

### 🎯 **Core Concepts**
- **Non-deterministic Testing**: Dealing with probabilistic outputs
- **Quality vs. Performance Trade-offs**: Balancing response quality and speed
- **Evaluation Metrics**: Understanding different ways to measure success
- **Production Readiness**: What it takes to deploy GenAI systems

### 🛡️ **Safety and Robustness**
- **Hallucination Detection**: Identifying when AI generates false information
- **Bias Testing**: Checking for unfair or inappropriate responses  
- **Edge Case Handling**: System behavior with unusual inputs
- **Adversarial Robustness**: Resistance to malicious inputs

### 📈 **Performance Engineering**
- **Latency Optimization**: Making responses faster
- **Scalability Testing**: Handling multiple concurrent users
- **Resource Management**: Efficient use of CPU, memory, and API calls
- **Monitoring and Alerting**: Detecting issues in production

### 🔍 **Quality Assurance**
- **Multi-dimensional Evaluation**: Beyond simple accuracy metrics
- **Consistency Testing**: Ensuring reliable behavior
- **Regression Detection**: Catching quality degradation
- **User Experience Focus**: Testing from the user's perspective

## Contributing

This is an educational project. If you find additional issues or have suggestions for improvements:

1. Document your findings clearly
2. Propose educational value of the change
3. Consider impact on learning objectives
4. Share with the instructor or class

## License

This project is created for educational purposes. Use freely for learning and teaching GenAI testing concepts.

---

**Happy Testing!** 🧪🤖

Remember: The goal isn't just to build GenAI applications, but to build ones that are reliable, safe, and provide genuine value to users. Testing is how we ensure that promise is kept.