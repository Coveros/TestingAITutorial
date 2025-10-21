#!/usr/bin/env python3
"""
Embedding Model Experiments for Students

This experiment demonstrates how different embedding models affect
RAG system performance and similarity scores.

🎯 Learning Objectives:
- Understand impact of embedding model choice on retrieval quality
- Compare older vs newer embedding models
- Analyze similarity scores and retrieval accuracy
- Learn about embedding model trade-offs
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag_pipeline import RAGPipeline
import cohere
import time
import chromadb

class EmbeddingExperimentPipeline(RAGPipeline):
    """Modified RAG pipeline for embedding experiments."""
    
    def __init__(self, embedding_model="embed-english-v3.0"):
        self.embedding_model = embedding_model
        # Create unique collection for this model to avoid dimension conflicts
        self.collection_name = f"embedding_test_{embedding_model.replace('-', '_').replace('.', '_')}"
        super().__init__()
    
    def _initialize_vector_db(self):
        """Initialize ChromaDB with a unique collection for this embedding model."""
        try:
            # Create database path for experiment
            db_path = f"./embedding_experiment_db"
            os.makedirs(db_path, exist_ok=True)
            
            self.vector_db = chromadb.PersistentClient(path=db_path)
            
            # Delete existing collection if it exists (to handle dimension changes)
            try:
                self.vector_db.delete_collection(self.collection_name)
            except:
                pass
            
            # Create new collection for this embedding model
            self.collection = self.vector_db.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine", "model": self.embedding_model}
            )
            
            # Load documents with this embedding model
            self._load_documents()
            
            return True
        except Exception as e:
            print(f"Failed to initialize vector database for {self.embedding_model}: {str(e)}")
            return False
    
    def _generate_embeddings(self, texts):
        """Override to use experimental embedding model."""
        try:
            response = self.cohere_client.embed(
                texts=texts,
                model=self.embedding_model,
                input_type="search_document"
            )
            return response.embeddings
        except Exception as e:
            print(f"❌ Error with model {self.embedding_model}: {str(e)}")
            raise
    
    def _generate_query_embedding(self, query):
        """Override to use experimental embedding model."""
        try:
            response = self.cohere_client.embed(
                texts=[query],
                model=self.embedding_model,
                input_type="search_query"
            )
            return response.embeddings[0]
        except Exception as e:
            print(f"❌ Error with model {self.embedding_model}: {str(e)}")
            raise

def test_embedding_model(model_name, description):
    """Test a specific embedding model."""
    print(f"\n{'='*70}")
    print(f"🧪 Testing: {description}")
    print(f"📊 Model: {model_name}")
    print(f"{'='*70}")
    
    try:
        # Create pipeline with specific embedding model
        pipeline = EmbeddingExperimentPipeline(embedding_model=model_name)
        
        # Test queries that should have good matches in our knowledge base
        test_queries = [
            "What is hallucination in GenAI?",
            "How do you evaluate RAG systems?",
            "What are testing best practices for chatbots?",
            "What metrics measure AI performance?"
        ]
        
        results = []
        total_time = 0
        
        for query in test_queries:
            try:
                start_time = time.time()
                result = pipeline.query(query)
                query_time = time.time() - start_time
                total_time += query_time
                
                # Extract similarity scores
                similarity_scores = [s['similarity'] for s in result['sources']]
                
                # Handle empty similarity scores
                if not similarity_scores:
                    print(f"📝 Query: {query[:50]}...")
                    print(f"   ❌ No similarity scores returned")
                    continue
                
                avg_similarity = sum(similarity_scores) / len(similarity_scores)
                max_similarity = max(similarity_scores)
                
                results.append({
                    'query': query,
                    'avg_similarity': avg_similarity,
                    'max_similarity': max_similarity,
                    'response_length': len(result['response']),
                    'time': query_time,
                    'similarity_scores': similarity_scores
                })
                
                print(f"📝 Query: {query[:50]}...")
                print(f"   📈 Similarities: {[f'{s:.3f}' for s in similarity_scores]}")
                print(f"   🎯 Best Match: {max_similarity:.3f}")
                print(f"   ⏱️  Time: {query_time:.2f}s")
                print()
                
            except Exception as query_error:
                print(f"📝 Query: {query[:50]}...")
                print(f"   ❌ Query failed: {str(query_error)}")
                continue
        
        if not results:
            print(f"❌ No successful queries for model {model_name}")
            return None
        
        # Calculate aggregate metrics
        avg_similarity_overall = sum(r['avg_similarity'] for r in results) / len(results)
        max_similarity_overall = max(r['max_similarity'] for r in results)
        avg_response_length = sum(r['response_length'] for r in results) / len(results)
        
        print(f"📊 AGGREGATE RESULTS:")
        print(f"   🎯 Average Similarity: {avg_similarity_overall:.4f}")
        print(f"   🏆 Best Similarity: {max_similarity_overall:.4f}")
        print(f"   📝 Avg Response Length: {avg_response_length:.0f} chars")
        print(f"   ⏱️  Total Time: {total_time:.2f}s")
        
        return {
            'model': model_name,
            'description': description,
            'avg_similarity': avg_similarity_overall,
            'max_similarity': max_similarity_overall,
            'avg_response_length': avg_response_length,
            'total_time': total_time,
            'results': results
        }
        
    except Exception as e:
        print(f"❌ Failed to test model {model_name}: {str(e)}")
        return None

def run_embedding_experiments():
    """Run embedding model comparison experiments."""
    
    print("🔬 EMBEDDING MODEL EXPERIMENTS")
    print("=" * 80)
    print("Students: Compare different embedding models to improve similarity scores!")
    print("📝 Note: Some models may fail due to:")
    print("   • Model deprecation or availability")
    print("   • Embedding dimension incompatibilities")
    print("   • API limitations")
    print("This teaches real-world challenges in ML model selection!")
    print()
    
    # Different embedding models to test
    embedding_models = [
        # Current model
        ("embed-english-v3.0", "Current Model (Latest Generation)"),
        
        # Previous models students can compare
        ("embed-english-v2.0", "Previous Model (Higher Dimensions, 4096)"),
        ("embed-english-light-v3.0", "Light Model (Faster, Potentially Lower Quality)"),
        
        # Multilingual models (may have different dimensions)
        ("embed-multilingual-v3.0", "Multilingual Model (Broader Support)"),
        ("embed-multilingual-light-v3.0", "Multilingual Light Model"),
        
        # Alternative models
        ("embed-english-light-v2.0", "Alternative Light Model"),
    ]
    
    successful_results = []
    
    for model_name, description in embedding_models:
        result = test_embedding_model(model_name, description)
        if result:
            successful_results.append(result)
        time.sleep(2)  # Brief pause between experiments
    
    if not successful_results:
        print("❌ No embedding models were successful. Check your Cohere API key and model availability.")
        return
    
    # Compare results
    print(f"\n{'='*80}")
    print("📈 EMBEDDING MODEL COMPARISON RESULTS")
    print(f"{'='*80}")
    
    # Sort by average similarity score
    successful_results.sort(key=lambda x: x['avg_similarity'], reverse=True)
    
    print(f"{'Rank':<4} {'Model':<25} {'Avg Sim':<8} {'Max Sim':<8} {'Time':<6} {'Description'}")
    print("-" * 80)
    
    for i, result in enumerate(successful_results, 1):
        print(f"{i:<4} {result['model'][:24]:<25} {result['avg_similarity']:<8.4f} "
              f"{result['max_similarity']:<8.4f} {result['total_time']:<6.1f} {result['description']}")
    
    if successful_results:
        best_model = successful_results[0]
        print(f"\n🏆 BEST PERFORMING MODEL:")
        print(f"   📊 Model: {best_model['model']}")
        print(f"   📝 Description: {best_model['description']}")
        print(f"   🎯 Average Similarity: {best_model['avg_similarity']:.4f}")
        print(f"   🏆 Best Single Match: {best_model['max_similarity']:.4f}")
        print(f"   ⏱️  Performance: {best_model['total_time']:.2f}s total")
        
        print(f"\n💡 RECOMMENDATIONS FOR STUDENTS:")
        if best_model['avg_similarity'] > 50.0:  # Scores are in percentage format
            print("✅ Excellent! This model shows very strong similarity scores.")
            print("   Your retrieval system is working well with this embedding model.")
        elif best_model['avg_similarity'] > 30.0:
            print("✅ Good performance! This model shows solid similarity scores.")
            print("   Consider this as your production model.")
        elif best_model['avg_similarity'] > 10.0:
            print("⚠️  Moderate performance. Room for improvement.")
            print("   Try adjusting chunking strategy or consider newer models.")
        else:
            print("❌ Low similarity scores indicate retrieval issues.")
            print("   Check chunking strategy, document quality, or try different models.")
        
        print(f"\n🔧 TO IMPLEMENT THE BEST MODEL:")
        print(f"   1. In app/rag_pipeline.py, find the _generate_embeddings method")
        print(f"   2. Change model=\"embed-english-v3.0\" to model=\"{best_model['model']}\"")
        print(f"   3. Also update _generate_query_embedding method")
        print(f"   4. Restart the application and test!")

def run_detailed_analysis():
    """Run detailed analysis of embedding performance."""
    print(f"\n{'='*80}")
    print("🔍 DETAILED EMBEDDING ANALYSIS")
    print(f"{'='*80}")
    
    # Test with current model for baseline
    print("Testing current model for detailed analysis...")
    result = test_embedding_model("embed-english-v3.0", "Current Model (Detailed Analysis)")
    
    if result:
        print("\n📊 PER-QUERY ANALYSIS:")
        for i, query_result in enumerate(result['results'], 1):
            print(f"\n{i}. Query: {query_result['query']}")
            print(f"   🎯 Avg Similarity: {query_result['avg_similarity']:.4f}")
            print(f"   🏆 Max Similarity: {query_result['max_similarity']:.4f}")
            print(f"   📝 Response Length: {query_result['response_length']} characters")
            print(f"   ⏱️  Query Time: {query_result['time']:.2f}s")
            
            # Provide recommendations based on scores
            if query_result['max_similarity'] < 0.01:
                print(f"   ⚠️  Very low similarity - document may not contain relevant info")
            elif query_result['max_similarity'] < 0.05:
                print(f"   📈 Low similarity - try smaller chunks or better model")
            else:
                print(f"   ✅ Good similarity score")

if __name__ == "__main__":
    print("Choose experiment type:")
    print("1. Quick Model Comparison")
    print("2. Detailed Analysis")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        run_detailed_analysis()
    else:
        run_embedding_experiments()