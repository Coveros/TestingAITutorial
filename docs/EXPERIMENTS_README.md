# GenAI Testing Tutorial - Experiment Files

## 🎯 Overview

This tutorial provides hands-on experiments for learning how to test and optimize Retrieval-Augmented Generation (RAG) systems. Each experiment focuses on a specific aspect of the system that has intentional issues for educational purposes.

## 🧪 Available Experiments

### 1. Chunking Strategy Optimization (`chunking_experiments.py`)
**Issue**: Document chunks are too large (2000 characters), reducing embedding focus
**Learn**: How chunk size affects similarity scores and retrieval quality
**Try**: Different chunk sizes (300-800 chars) and overlap strategies

### 2. Embedding Model Comparison (`embedding_experiments.py`)
**Issue**: Using older embedding model (`embed-english-v2.0`)
**Learn**: Impact of embedding model choice on retrieval accuracy
**Try**: Newer models like `embed-english-v3.0` (if available)

### 3. Generation Parameters Tuning (`generation_experiments.py`)
**Issue**: `max_tokens=300` (too short) and `temperature=0.7` (inconsistent)
**Learn**: How generation parameters affect response quality and consistency
**Try**: Longer responses (600-800 tokens) and lower temperature (0.1-0.3)

### 4. Retrieval Strategy Optimization (`retrieval_experiments.py`)
**Issue**: No similarity filtering, fixed retrieval count
**Learn**: Optimizing document retrieval for relevance and performance
**Try**: Different retrieval counts and similarity thresholds

### 5. End-to-End System Optimization (`system_optimization_experiments.py`)
**Learn**: How different optimizations interact and combine
**Compare**: Baseline vs optimized system performance across all metrics

## 🚀 Getting Started

### Quick Start (Recommended)
```bash
python run_experiments.py
```
This provides a menu-driven interface to run all experiments.

### Individual Experiments
```bash
# Test chunking strategies
python chunking_experiments.py

# Compare embedding models  
python embedding_experiments.py

# Optimize generation parameters
python generation_experiments.py

# Improve retrieval strategy
python retrieval_experiments.py

# Full system optimization
python system_optimization_experiments.py
```

## 📊 Understanding Results

### Similarity Scores
- **Good**: > 0.01 (documents are relevant to query)
- **Poor**: < 0.005 (documents may not be relevant)
- **Terrible**: < 0.001 (likely retrieval issues)

### Quality Metrics
- **Response Length**: 200-800 characters is usually good
- **Consistency**: Low temperature = more consistent responses
- **Sources**: 3-5 relevant sources per response is optimal
- **Response Time**: < 2 seconds for good user experience

### Common Issues to Look For
- **Truncated Responses**: Increase `max_tokens`
- **Inconsistent Answers**: Lower `temperature`
- **Poor Similarity**: Try smaller chunks or better embedding model
- **Slow Performance**: Reduce retrieval count or add filtering

## 🔧 Implementing Optimizations

After running experiments, implement the best configurations:

1. **Edit `app/rag_pipeline.py`**
2. **Update the following methods:**
   - `_split_text()`: Chunk size and overlap
   - `_generate_embeddings()`: Embedding model
   - `_generate_response()`: Generation parameters
   - `_retrieve_documents()`: Retrieval strategy

3. **Restart the Flask application**
4. **Test improvements in the chat interface**

## 📚 Learning Objectives

By completing these experiments, students will learn:

### Technical Skills
- How to systematically test GenAI systems
- Performance measurement and optimization techniques
- Understanding of RAG pipeline components
- Hands-on experience with different AI models and parameters

### Testing Methodologies
- A/B testing for AI systems
- Metric-driven optimization
- Trade-off analysis (quality vs speed vs cost)
- Systematic evaluation frameworks

### Real-World Applications
- Production GenAI system optimization
- Common issues and their solutions
- Performance monitoring and alerting
- Continuous improvement processes

## 📈 Expected Learning Progression

1. **Discover Issues**: Run baseline tests to see current problems
2. **Hypothesize Solutions**: Predict what changes might help
3. **Test Systematically**: Run experiments to validate hypotheses
4. **Measure Impact**: Quantify improvements with metrics
5. **Implement Best**: Apply optimal configurations to the system
6. **Validate Results**: Confirm improvements in the live application

## 🛠️ Troubleshooting

### Common Experiment Errors

**"No module named 'cohere'"**
- Ensure you're in the correct virtual environment
- Run: `pip install cohere`

**"COHERE_API_KEY environment variable not set"**
- Check your `.env` file has the API key
- Restart the experiment after updating

**"Model 'embed-english-v3.0' was removed"**
- Some newer models may not be available
- The experiments will show which models work
- Use the available models shown in results

**Very low similarity scores (< 0.001)**
- This indicates a real problem to investigate
- Try the chunking experiments first
- Check if documents actually contain relevant content

### Performance Issues

**Experiments running slowly**
- Each configuration test takes time due to API calls
- Run individual experiments instead of full suite
- Reduce the number of test queries if needed

**API rate limits**
- Cohere has rate limits on trial accounts
- Add delays between experiments if needed
- Focus on the most promising configurations

## 💡 Tips for Success

1. **Start with chunking experiments** - biggest impact usually
2. **Document your findings** - note which configurations work best
3. **Understand the trade-offs** - faster isn't always better
4. **Test with real queries** - use questions your users would ask
5. **Implement incrementally** - change one thing at a time
6. **Measure everything** - use the provided metrics

## 🎓 Assessment Questions

After completing experiments, students should be able to answer:

1. Which chunking strategy provided the best similarity scores and why?
2. How does temperature affect response consistency and creativity?
3. What's the trade-off between retrieval count and performance?
4. How do you know if your embeddings are working well?
5. What metrics would you monitor in production?
6. How would you set up automated testing for a GenAI system?

## 🔗 Next Steps

After mastering these experiments:

1. **Implement monitoring** for production systems
2. **Create automated test suites** for continuous validation
3. **Design A/B testing frameworks** for ongoing optimization
4. **Explore advanced techniques** like reranking, hybrid search, etc.
5. **Build evaluation datasets** specific to your use case

Happy experimenting! 🧪✨