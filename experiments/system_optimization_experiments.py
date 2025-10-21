#!/usr/bin/env python3
"""
End-to-End System Optimization Experiments for Students

This experiment demonstrates how to optimize the entire RAG pipeline
by combining the best settings from individual experiments.

🎯 Learning Objectives:
- Understand how different optimizations interact
- Learn to balance multiple quality metrics
- Practice systematic optimization methodology
- Compare baseline vs optimized system performance
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag_pipeline import RAGPipeline
import time
import statistics
import json
import chromadb
import hashlib

class OptimizedRAGPipeline(RAGPipeline):
    """Fully optimized RAG pipeline for comparison experiments."""
    
    def __init__(self, config):
        self.config = config
        # Create unique collection name based on config to avoid dimension conflicts
        config_hash = hashlib.md5(json.dumps(config, sort_keys=True).encode()).hexdigest()[:8]
        self.collection_name = f"system_opt_{config_hash}"
        super().__init__()
    
    def _initialize_vector_db(self):
        """Initialize ChromaDB with a unique collection for this configuration."""
        try:
            # Create database path for experiment
            db_path = f"./system_optimization_db"
            os.makedirs(db_path, exist_ok=True)
            
            self.vector_db = chromadb.PersistentClient(path=db_path)
            
            # Delete existing collection if it exists
            try:
                self.vector_db.delete_collection(self.collection_name)
            except:
                pass
            
            # Create new collection for this configuration
            self.collection = self.vector_db.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine", "experiment": "system_optimization"}
            )
            
            # Load documents
            self._load_documents()
            
            return True
        except Exception as e:
            print(f"Failed to initialize vector database: {str(e)}")
            return False
    
    def _split_text(self, text, **kwargs):
        """Use optimized chunking strategy."""
        return super()._split_text(
            text, 
            chunk_size=self.config.get('chunk_size', 2000),
            chunk_overlap=self.config.get('chunk_overlap', 200)
        )
    
    def _generate_embeddings(self, texts):
        """Use optimized embedding model."""
        try:
            response = self.cohere_client.embed(
                texts=texts,
                model=self.config.get('embedding_model', 'embed-english-v2.0'),
                input_type="search_document"
            )
            return response.embeddings
        except Exception as e:
            print(f"❌ Error with embedding model: {str(e)}")
            raise
    
    def _generate_query_embedding(self, query):
        """Use optimized embedding model."""
        try:
            response = self.cohere_client.embed(
                texts=[query],
                model=self.config.get('embedding_model', 'embed-english-v2.0'),
                input_type="search_query"
            )
            return response.embeddings[0]
        except Exception as e:
            print(f"❌ Error with embedding model: {str(e)}")
            raise
    
    def _retrieve_documents(self, query, n_results=None):
        """Use optimized retrieval strategy."""
        start_time = time.time()
        
        try:
            n_results = self.config.get('n_results', 5)
            similarity_threshold = self.config.get('similarity_threshold', 0.0)
            
            query_embedding = self._generate_query_embedding(query)
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            retrieval_time = time.time() - start_time
            
            # Filter by similarity threshold
            filtered_docs = []
            filtered_metadata = []
            filtered_distances = []
            
            if results['documents'] and results['distances']:
                for doc, meta, dist in zip(
                    results['documents'][0], 
                    results['metadatas'][0], 
                    results['distances'][0]
                ):
                    similarity = 1 / (1 + (dist / 100))
                    if similarity >= similarity_threshold:
                        filtered_docs.append(doc)
                        filtered_metadata.append(meta)
                        filtered_distances.append(dist)
            
            return {
                'documents': filtered_docs,
                'metadatas': filtered_metadata,
                'distances': filtered_distances,
                'retrieval_time': retrieval_time
            }
            
        except Exception as e:
            self.stats['errors'] += 1
            raise
    
    def _generate_response(self, query, context_docs):
        """Use optimized generation parameters."""
        try:
            context = "\n\n".join(context_docs[:3])
            
            response = self.cohere_client.chat(
                model="command-r-08-2024",
                message=f"""Question: {query}

Context:
{context}

Based on the provided context, please answer the question about testing generative AI applications. If the context doesn't contain relevant information, say so clearly.""",
                max_tokens=self.config.get('max_tokens', 300),
                temperature=self.config.get('temperature', 0.7),
            )
            
            return response.text.strip()
            
        except Exception as e:
            self.stats['errors'] += 1
            raise

def run_comprehensive_evaluation(config, description):
    """Run comprehensive evaluation of a configuration."""
    print(f"\n{'='*80}")
    print(f"🧪 Evaluating: {description}")
    print(f"📊 Config: {json.dumps(config, indent=2)}")
    print(f"{'='*80}")
    
    try:
        pipeline = OptimizedRAGPipeline(config)
        
        # Comprehensive test queries covering different scenarios
        test_queries = [
            # Factual questions
            ("Factual", "What is hallucination in GenAI?"),
            ("Factual", "What are the main types of AI testing?"),
            
            # Process questions
            ("Process", "How do you evaluate RAG system performance?"),
            ("Process", "What steps are involved in testing a chatbot?"),
            
            # Technical questions
            ("Technical", "What metrics measure retrieval accuracy?"),
            ("Technical", "How do you calculate precision and recall for GenAI?"),
            
            # Complex questions
            ("Complex", "Explain the complete testing framework for production GenAI applications including evaluation metrics and best practices."),
            ("Complex", "What are the challenges in testing GenAI systems and how can they be addressed?"),
            
            # Edge cases
            ("Edge", "What is the best color for testing?"),  # Irrelevant question
            ("Edge", ""),  # Empty query (will be handled by validation)
        ]
        
        results = []
        total_time = 0
        successful_queries = 0
        
        for query_type, query in test_queries:
            if not query.strip():  # Skip empty queries
                continue
                
            print(f"\n📝 {query_type}: {query[:60]}...")
            
            try:
                start_time = time.time()
                result = pipeline.query(query)
                query_time = time.time() - start_time
                total_time += query_time
                successful_queries += 1
                
                # Calculate metrics
                similarity_scores = [s['similarity'] for s in result['sources']]
                avg_similarity = statistics.mean(similarity_scores) if similarity_scores else 0
                max_similarity = max(similarity_scores) if similarity_scores else 0
                response_length = len(result['response'])
                
                # Quality checks
                has_sources = len(result['sources']) > 0
                response_complete = not result['response'].endswith('...')
                response_relevant = 'I don\'t know' not in result['response'] and 'cannot answer' not in result['response'].lower()
                
                quality_score = sum([
                    avg_similarity > 0.005,  # Decent similarity
                    response_length > 100,   # Adequate length
                    has_sources,             # Has supporting sources
                    response_complete,       # Complete response
                    response_relevant        # Relevant response
                ]) / 5.0
                
                result_data = {
                    'query_type': query_type,
                    'query': query,
                    'avg_similarity': avg_similarity,
                    'max_similarity': max_similarity,
                    'response_length': response_length,
                    'sources_count': len(result['sources']),
                    'retrieval_time': result.get('retrieval_time', 0),
                    'generation_time': result.get('generation_time', 0),
                    'total_time': query_time,
                    'quality_score': quality_score,
                    'has_sources': has_sources,
                    'response_complete': response_complete,
                    'response_relevant': response_relevant
                }
                
                results.append(result_data)
                
                print(f"   📊 Similarity: {avg_similarity:.4f} (max: {max_similarity:.4f})")
                print(f"   📝 Response: {response_length} chars, {len(result['sources'])} sources")
                print(f"   🎯 Quality: {quality_score:.2f}/1.0")
                print(f"   ⏱️  Time: {query_time:.2f}s")
                
                # Add rate limiting delay between queries
                if query_type != "Edge":  # Don't wait after the last query type
                    print(f"   ⏳ Waiting 6s for rate limiting...")
                    time.sleep(6)
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                continue
        
        if not results:
            print("❌ No successful queries")
            return None
        
        # Calculate aggregate metrics
        avg_similarity = statistics.mean([r['avg_similarity'] for r in results])
        avg_quality = statistics.mean([r['quality_score'] for r in results])
        avg_response_length = statistics.mean([r['response_length'] for r in results])
        avg_total_time = total_time / successful_queries
        avg_sources = statistics.mean([r['sources_count'] for r in results])
        
        # Performance by query type
        type_performance = {}
        for result in results:
            qtype = result['query_type']
            if qtype not in type_performance:
                type_performance[qtype] = []
            type_performance[qtype].append(result['quality_score'])
        
        type_averages = {k: statistics.mean(v) for k, v in type_performance.items()}
        
        print(f"\n📊 AGGREGATE RESULTS:")
        print(f"   🎯 Average Similarity: {avg_similarity:.4f}")
        print(f"   ⭐ Average Quality Score: {avg_quality:.3f}/1.0")
        print(f"   📝 Average Response Length: {avg_response_length:.0f} chars")
        print(f"   📋 Average Sources: {avg_sources:.1f}")
        print(f"   ⏱️  Average Time: {avg_total_time:.2f}s")
        print(f"   ✅ Success Rate: {successful_queries}/{len([q for q in test_queries if q[1].strip()])*100:.0f}%")
        
        print(f"\n📊 Performance by Query Type:")
        for qtype, score in type_averages.items():
            print(f"   {qtype}: {score:.3f}/1.0")
        
        return {
            'config': config,
            'description': description,
            'avg_similarity': avg_similarity,
            'avg_quality': avg_quality,
            'avg_response_length': avg_response_length,
            'avg_total_time': avg_total_time,
            'avg_sources': avg_sources,
            'success_rate': successful_queries / len([q for q in test_queries if q[1].strip()]),
            'type_performance': type_averages,
            'results': results
        }
        
    except Exception as e:
        print(f"❌ Configuration failed: {str(e)}")
        return None

def run_optimization_experiments():
    """Run end-to-end optimization experiments."""
    
    print("🚀 END-TO-END RAG SYSTEM OPTIMIZATION")
    print("=" * 80)
    print("Students: Compare baseline vs optimized configurations!")
    print()
    
    # Different system configurations to test
    configurations = [
        # Baseline (current problematic settings)
        ({
            'chunk_size': 2000,
            'chunk_overlap': 200,
            'embedding_model': 'embed-english-v2.0',
            'n_results': 5,
            'similarity_threshold': 0.0,
            'max_tokens': 300,
            'temperature': 0.7
        }, "Baseline: Current System (All Issues Present)"),
        
        # Fix chunking only
        ({
            'chunk_size': 500,
            'chunk_overlap': 50,
            'embedding_model': 'embed-english-v2.0',
            'n_results': 5,
            'similarity_threshold': 0.0,
            'max_tokens': 300,
            'temperature': 0.7
        }, "Optimization 1: Better Chunking Only"),
        
        # Fix generation parameters only
        ({
            'chunk_size': 2000,
            'chunk_overlap': 200,
            'embedding_model': 'embed-english-v2.0',
            'n_results': 5,
            'similarity_threshold': 0.0,
            'max_tokens': 600,
            'temperature': 0.3
        }, "Optimization 2: Better Generation Only"),
        
        # Fix retrieval only
        ({
            'chunk_size': 2000,
            'chunk_overlap': 200,
            'embedding_model': 'embed-english-v2.0',
            'n_results': 7,
            'similarity_threshold': 0.005,
            'max_tokens': 300,
            'temperature': 0.7
        }, "Optimization 3: Better Retrieval Only"),
        
        # Progressive optimizations
        ({
            'chunk_size': 500,
            'chunk_overlap': 50,
            'embedding_model': 'embed-english-v2.0',
            'n_results': 7,
            'similarity_threshold': 0.005,
            'max_tokens': 600,
            'temperature': 0.3
        }, "Optimization 4: Multiple Fixes (No Embedding)"),
        
        # Try newer embedding model if available
        ({
            'chunk_size': 500,
            'chunk_overlap': 50,
            'embedding_model': 'embed-english-v3.0',
            'n_results': 7,
            'similarity_threshold': 0.005,
            'max_tokens': 600,
            'temperature': 0.3
        }, "Optimization 5: All Optimizations + Better Embeddings"),
        
        # Conservative optimization
        ({
            'chunk_size': 400,
            'chunk_overlap': 40,
            'embedding_model': 'embed-english-v2.0',
            'n_results': 5,
            'similarity_threshold': 0.01,
            'max_tokens': 500,
            'temperature': 0.2
        }, "Optimization 6: Conservative All-Around"),
        
        # Aggressive optimization
        ({
            'chunk_size': 300,
            'chunk_overlap': 30,
            'embedding_model': 'embed-english-v2.0',
            'n_results': 10,
            'similarity_threshold': 0.002,
            'max_tokens': 800,
            'temperature': 0.1
        }, "Optimization 7: Aggressive All-Around"),
    ]
    
    successful_results = []
    
    for config, description in configurations:
        result = run_comprehensive_evaluation(config, description)
        if result:
            successful_results.append(result)
        
        # Add substantial delay between configurations for rate limiting
        print(f"⏳ Waiting 15s between configurations for rate limiting...")
        time.sleep(15)
    
    if not successful_results:
        print("❌ No configurations were successful.")
        return
    
    # Compare all results
    print(f"\n{'='*120}")
    print("🏆 OPTIMIZATION RESULTS COMPARISON")
    print(f"{'='*120}")
    
    # Sort by overall quality score
    successful_results.sort(key=lambda x: x['avg_quality'], reverse=True)
    
    print(f"{'Rank':<4} {'Configuration':<40} {'Quality':<8} {'Sim':<7} {'Time':<6} {'Len':<5} {'Success':<8}")
    print("-" * 120)
    
    for i, result in enumerate(successful_results, 1):
        print(f"{i:<4} {result['description'][:39]:<40} {result['avg_quality']:<8.3f} "
              f"{result['avg_similarity']:<7.4f} {result['avg_total_time']:<6.2f} "
              f"{result['avg_response_length']:<5.0f} {result['success_rate']:<8.1%}")
    
    if successful_results:
        baseline = next((r for r in successful_results if 'Baseline' in r['description']), None)
        best = successful_results[0]
        
        print(f"\n🎯 OPTIMIZATION IMPACT:")
        if baseline and best != baseline:
            quality_improvement = (best['avg_quality'] - baseline['avg_quality']) / baseline['avg_quality']
            similarity_improvement = (best['avg_similarity'] - baseline['avg_similarity']) / baseline['avg_similarity'] if baseline['avg_similarity'] > 0 else float('inf')
            time_change = (best['avg_total_time'] - baseline['avg_total_time']) / baseline['avg_total_time']
            
            print(f"   📈 Quality Improvement: {quality_improvement:+.1%}")
            print(f"   🎯 Similarity Improvement: {similarity_improvement:+.1%}")
            print(f"   ⏱️  Time Change: {time_change:+.1%}")
            print(f"   📝 Response Length Change: {(best['avg_response_length'] - baseline['avg_response_length'])/baseline['avg_response_length']:+.1%}")
        
        print(f"\n🏆 BEST CONFIGURATION:")
        print(f"   📊 System: {best['description']}")
        print(f"   ⭐ Quality Score: {best['avg_quality']:.3f}/1.0")
        print(f"   🎯 Similarity Score: {best['avg_similarity']:.4f}")
        print(f"   ⏱️  Average Response Time: {best['avg_total_time']:.2f}s")
        print(f"   ✅ Success Rate: {best['success_rate']:.1%}")
        
        print(f"\n🔧 RECOMMENDED IMPLEMENTATION:")
        config = best['config']
        print(f"   1. Update chunking: chunk_size={config['chunk_size']}, overlap={config['chunk_overlap']}")
        print(f"   2. Update embeddings: model='{config['embedding_model']}'")
        print(f"   3. Update retrieval: n_results={config['n_results']}, threshold={config['similarity_threshold']}")
        print(f"   4. Update generation: max_tokens={config['max_tokens']}, temperature={config['temperature']}")
        
        print(f"\n📊 PERFORMANCE BY QUERY TYPE (Best Config):")
        for qtype, score in best['type_performance'].items():
            status = "✅" if score > 0.7 else "⚠️" if score > 0.5 else "❌"
            print(f"   {status} {qtype}: {score:.3f}/1.0")

if __name__ == "__main__":
    run_optimization_experiments()