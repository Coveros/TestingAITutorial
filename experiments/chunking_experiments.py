#!/usr/bin/env python3
"""
Chunking Strategy Experiments for Students

This file demonstrates different chunking strategies students can try
to improve RAG system similarity scores and retrieval quality.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag_pipeline import RAGPipeline
import time
import chromadb

def test_chunking_strategy(chunk_size, chunk_overlap, description):
    """Test a specific chunking configuration."""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Chunk Size: {chunk_size}, Overlap: {chunk_overlap}")
    print(f"{'='*60}")
    
    # Create a custom pipeline class to force re-chunking
    class CustomChunkingPipeline(RAGPipeline):
        def __init__(self, chunk_size, chunk_overlap):
            self.custom_chunk_size = chunk_size
            self.custom_chunk_overlap = chunk_overlap
            super().__init__()
        
        def _initialize_vector_db(self):
            """Initialize ChromaDB with a unique collection name."""
            try:
                # Create persistent database in a test directory
                db_path = f"./test_chroma_db_{self.custom_chunk_size}_{self.custom_chunk_overlap}"
                import os
                os.makedirs(db_path, exist_ok=True)
                
                self.vector_db = chromadb.PersistentClient(path=db_path)
                
                # Create unique collection name for this test
                collection_name = f"test_collection_{self.custom_chunk_size}_{self.custom_chunk_overlap}"
                
                # Delete existing collection if it exists
                try:
                    self.vector_db.delete_collection(collection_name)
                except:
                    pass
                
                self.collection = self.vector_db.create_collection(
                    name=collection_name,
                    metadata={"hnsw:space": "cosine"}
                )
                
                # Load documents with custom chunking
                self._load_documents()
                
                return True
            except Exception as e:
                print(f"Failed to initialize vector database: {str(e)}")
                import traceback
                traceback.print_exc()
                return False
        
        def _split_text(self, text, **kwargs):
            """Override with custom chunking parameters."""
            return super()._split_text(text, chunk_size=self.custom_chunk_size, chunk_overlap=self.custom_chunk_overlap)
    
    # Test query
    test_query = "What is hallucination in GenAI?"
    
    try:
        # Create pipeline with custom chunking
        pipeline = CustomChunkingPipeline(chunk_size, chunk_overlap)
        
        result = pipeline.query(test_query)
        
        print(f"✅ Query: {test_query}")
        print(f"📊 Similarity Scores: {[s['similarity'] for s in result['sources']]}")
        print(f"⏱️  Response Time: {result['total_time']:.2f}s")
        print(f"📄 Source Preview: {result['sources'][0]['content'][:100]}...")
        print(f"🔢 Total Chunks in DB: {pipeline.collection.count()}")
        
        return result['sources'][0]['similarity']
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 0.0

def run_chunking_experiments():
    """Run different chunking experiments for comparison."""
    
    print("🧪 RAG Chunking Strategy Experiments")
    print("Students: Try different configurations to improve similarity scores!")
    
    # STUDENT: Add or modify additional strategies below
    strategies = [
        # Current (problematic) configuration
        (2000, 200, "Current Strategy (Large Chunks - Poor Performance)"),
        
        # Smaller chunks - better focus
        (500, 50, "Strategy 1: Smaller Chunks (Better Focus)"),
        (300, 30, "Strategy 2: Very Small Chunks (Maximum Focus)"),
        
        # Different overlap strategies
        (800, 100, "Strategy 3: Medium Chunks with Moderate Overlap"),
        (600, 150, "Strategy 4: High Overlap (Better Context Preservation)"),
        
        # Minimal overlap
        (400, 0, "Strategy 5: No Overlap (Faster Processing)"),
    ]
    
    results = []
    
    for chunk_size, chunk_overlap, description in strategies:
        score = test_chunking_strategy(chunk_size, chunk_overlap, description)
        results.append((description, score, chunk_size, chunk_overlap))
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print(f"\n{'='*80}")
    print("📈 CHUNKING STRATEGY COMPARISON RESULTS")
    print(f"{'='*80}")
    
    results.sort(key=lambda x: x[1], reverse=True)
    
    for i, (description, score, chunk_size, chunk_overlap) in enumerate(results, 1):
        print(f"{i}. {description}")
        print(f"   Similarity Score: {score:.4f} | Size: {chunk_size} | Overlap: {chunk_overlap}")
        print()
    
    best_strategy = results[0]
    print(f"🏆 BEST STRATEGY: {best_strategy[0]}")
    print(f"   Achieved similarity score: {best_strategy[1]:.4f}")
    print(f"   Configuration: chunk_size={best_strategy[2]}, chunk_overlap={best_strategy[3]}")

if __name__ == "__main__":
    run_chunking_experiments()