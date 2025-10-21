# Experiments Package

This package contains all optimization experiments for the GenAI Testing Tutorial.

## 📁 Files

- **`run_experiments.py`** - Master experiment runner with menu interface
- **`chunking_experiments.py`** - Document chunking strategy optimization
- **`embedding_experiments.py`** - Embedding model comparison
- **`generation_experiments.py`** - Response generation parameter tuning  
- **`retrieval_experiments.py`** - Document retrieval strategy optimization
- **`system_optimization_experiments.py`** - End-to-end system optimization

## 🚀 Usage

### From project root:
```bash
python -m experiments.run_experiments
```

### From experiments directory:
```bash
cd experiments
python run_experiments.py
```

### Individual experiments:
```bash
python -m experiments.chunking_experiments
python -m experiments.embedding_experiments
# etc...
```

## 📊 Learning Objectives

Each experiment teaches specific optimization techniques:

1. **Chunking** - How document segmentation affects retrieval quality
2. **Embeddings** - Impact of different embedding models on similarity
3. **Generation** - Optimizing response quality and consistency  
4. **Retrieval** - Balancing relevance and performance
5. **System** - Integration and end-to-end optimization

See the main documentation in `docs/EXPERIMENTS_README.md` for detailed information.