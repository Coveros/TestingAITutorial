#!/usr/bin/env python3
"""
Generation Parameters Experiments for Students

This experiment demonstrates how different generation parameters affect
RAG system response quality, consistency, and completeness.

🎯 Learning Objectives:
- Understand impact of max_tokens on response completeness
- Learn how temperature affects response consistency and creativity
- Analyze trade-offs between response length and quality
- Optimize generation parameters for specific use cases
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag_pipeline import RAGPipeline
import time
import statistics
import chromadb

class GenerationExperimentPipeline(RAGPipeline):
    """Modified RAG pipeline for generation parameter experiments."""
    
    def __init__(self, max_tokens=300, temperature=0.7):
        self.experiment_max_tokens = max_tokens
        self.experiment_temperature = temperature
        # Create unique collection to avoid dimension conflicts
        self.collection_name = f"generation_test_{max_tokens}_{int(temperature*100)}"
        super().__init__()
    
    def _initialize_vector_db(self):
        """Initialize ChromaDB with a unique collection for this experiment."""
        try:
            # Create database path for experiment
            db_path = f"./generation_experiment_db"
            os.makedirs(db_path, exist_ok=True)
            
            self.vector_db = chromadb.PersistentClient(path=db_path)
            
            # Delete existing collection if it exists
            try:
                self.vector_db.delete_collection(self.collection_name)
            except:
                pass
            
            # Create new collection for this experiment
            self.collection = self.vector_db.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine", "experiment": "generation"}
            )
            
            # Load documents
            self._load_documents()
            
            return True
        except Exception as e:
            print(f"Failed to initialize vector database: {str(e)}")
            return False
    
    def _generate_response(self, query, context_docs):
        """Override to use experimental generation parameters."""
        try:
            context = "\n\n".join(context_docs[:3])
            
            response = self.cohere_client.chat(
                model="command-r-08-2024",
                message=f"""Question: {query}

Context:
{context}

Based on the provided context, please answer the question about testing generative AI applications. If the context doesn't contain relevant information, say so clearly.""",
                max_tokens=self.experiment_max_tokens,
                temperature=self.experiment_temperature,
            )
            
            return response.text.strip()
            
        except Exception as e:
            self.stats['errors'] += 1
            raise

def test_generation_parameters(max_tokens, temperature, description):
    """Test specific generation parameters."""
    print(f"\n{'='*70}")
    print(f"🧪 Testing: {description}")
    print(f"📊 Max Tokens: {max_tokens}, Temperature: {temperature}")
    print(f"{'='*70}")
    
    try:
        pipeline = GenerationExperimentPipeline(
            max_tokens=max_tokens, 
            temperature=temperature
        )
        
        # Test queries of varying complexity
        test_queries = [
            ("Simple", "What is hallucination?"),
            ("Medium", "How do you evaluate RAG system performance?"),
            ("Complex", "Explain the complete process of testing a GenAI chatbot application including metrics, evaluation frameworks, and best practices."),
            ("Technical", "What are the differences between precision, recall, and F1-score in the context of GenAI evaluation?"),
        ]
        
        results = []
        
        for complexity, query in test_queries:
            print(f"\n📝 {complexity} Query: {query[:60]}...")
            
            # Run query multiple times to test consistency
            responses = []
            times = []
            
            for run in range(3):  # 3 runs to test consistency
                max_retries = 3
                retry_count = 0
                
                while retry_count < max_retries:
                    try:
                        # Measure ONLY the actual API call time, not wait times
                        api_start_time = time.time()
                        result = pipeline.query(query)
                        api_end_time = time.time()
                        query_time = api_end_time - api_start_time
                        
                        responses.append(result['response'])
                        times.append(query_time)
                        
                        print(f"   Run {run+1}: {len(result['response'])} chars, {query_time:.2f}s")
                        break  # Success, exit retry loop
                        
                    except Exception as e:
                        retry_count += 1
                        if "rate limit" in str(e).lower() or "too many requests" in str(e).lower():
                            wait_time = 15 * retry_count  # Exponential backoff
                            print(f"   ⚠️  Rate limit hit, waiting {wait_time}s (attempt {retry_count}/{max_retries})...")
                            time.sleep(wait_time)
                            # Note: Wait time is NOT included in query_time measurement
                        else:
                            print(f"   ❌ API error: {str(e)}")
                            break
                
                if retry_count >= max_retries:
                    print(f"   ❌ Failed after {max_retries} retries, skipping this run")
                    continue
                
                # Add delay between API calls to respect rate limits
                if run < 2:  # Don't wait after the last run
                    print(f"   ⏳ Waiting 7s for rate limiting...")
                    time.sleep(7)
            
            # Analyze results (only if we have responses)
            if not responses:
                print(f"   ❌ No successful responses for this query")
                continue
                
            response_lengths = [len(r) for r in responses]
            avg_length = statistics.mean(response_lengths)
            length_std = statistics.stdev(response_lengths) if len(response_lengths) > 1 else 0
            avg_time = statistics.mean(times) if times else 0
            
            # Check for truncation (responses ending abruptly)
            truncated_responses = sum(1 for r in responses if not r.endswith(('.', '!', '?', '"')))
            
            # Check consistency (similar response lengths)
            consistency_score = 1 - (length_std / avg_length) if avg_length > 0 else 0
            
            result_data = {
                'complexity': complexity,
                'query': query,
                'responses': responses,
                'avg_length': avg_length,
                'length_std': length_std,
                'consistency_score': consistency_score,
                'truncated_count': truncated_responses,
                'avg_time': avg_time,
                'response_lengths': response_lengths
            }
            
            results.append(result_data)
            
            print(f"   📊 Avg Length: {avg_length:.0f} chars (±{length_std:.0f})")
            print(f"   🎯 Consistency: {consistency_score:.3f}")
            print(f"   ✂️  Truncated: {truncated_responses}/3 responses")
            print(f"   ⏱️  Avg Time: {avg_time:.2f}s")
            
            # Show response quality indicators
            if truncated_responses > 0:
                print(f"   ⚠️  Warning: {truncated_responses} responses appear truncated")
            if consistency_score < 0.8:
                print(f"   🔄 High variability in response length (low consistency)")
            
            # Add delay between different query complexities
            if complexity != "Technical":  # Don't wait after the last query
                print(f"   ⏳ Waiting 3s before next query...")
                time.sleep(3)
        
        # Calculate overall metrics (only for successful results)
        successful_results_data = [r for r in results if r['responses']]
        
        if not successful_results_data:
            print(f"\n❌ No successful queries for this parameter set")
            return None
            
        overall_avg_length = statistics.mean([r['avg_length'] for r in successful_results_data])
        overall_consistency = statistics.mean([r['consistency_score'] for r in successful_results_data])
        total_truncated = sum(r['truncated_count'] for r in successful_results_data)
        overall_time = statistics.mean([r['avg_time'] for r in successful_results_data])
        total_possible_responses = len(successful_results_data) * 3
        
        print(f"\n📊 OVERALL RESULTS:")
        print(f"   📝 Average Response Length: {overall_avg_length:.0f} characters")
        print(f"   🎯 Average Consistency: {overall_consistency:.3f}")
        print(f"   ✂️  Total Truncated Responses: {total_truncated}/{total_possible_responses}")
        print(f"   ⏱️  Average Response Time: {overall_time:.2f}s (API time only, excludes rate limiting waits)")
        print(f"   ✅ Successful Queries: {len(successful_results_data)}/{len(test_queries)}")
        
        return {
            'max_tokens': max_tokens,
            'temperature': temperature,
            'description': description,
            'overall_avg_length': overall_avg_length,
            'overall_consistency': overall_consistency,
            'total_truncated': total_truncated,
            'overall_time': overall_time,
            'results': results
        }
        
    except Exception as e:
        print(f"❌ Failed to test parameters: {str(e)}")
        return None

def run_generation_experiments():
    """Run generation parameter comparison experiments."""
    
    print("🔬 GENERATION PARAMETERS EXPERIMENTS")
    print("=" * 80)
    print("Students: Optimize generation parameters for better response quality!")
    print("⏰ Note: This experiment includes rate limiting delays (7s between API calls)")
    print("   Total experiment time: ~15-20 minutes due to API rate limits")
    print()
    
    # STUDENTS: Different parameter combinations to test
    parameter_sets = [
        # Current (problematic) parameters
        (300, 0.7, "Current Settings (Short Responses, High Variability)"),
        
        # Fix max_tokens issue
        (500, 0.7, "Strategy 1: Longer Responses"),
        (800, 0.7, "Strategy 2: Much Longer Responses"),
        (1000, 0.7, "Strategy 3: Very Long Responses"),
        
        # Fix temperature issue
        (300, 0.3, "Strategy 4: Lower Temperature (More Consistent)"),
        (300, 0.1, "Strategy 5: Very Low Temperature (Highly Consistent)"),
        (300, 0.0, "Strategy 6: Zero Temperature (Deterministic)"),
        
        # Balanced approaches
        (600, 0.3, "Strategy 7: Balanced (Longer + Lower Temp)"),
        (800, 0.2, "Strategy 8: Conservative (Long + Very Low Temp)"),
        (500, 0.4, "Strategy 9: Moderate (Medium Length + Medium Temp)"),
    ]
    
    successful_results = []
    
    for max_tokens, temperature, description in parameter_sets:
        result = test_generation_parameters(max_tokens, temperature, description)
        if result:
            successful_results.append(result)
        
        # Longer pause between parameter sets to respect rate limits
        print(f"⏳ Waiting 10s before next parameter set...")
        time.sleep(10)
    
    if not successful_results:
        print("❌ No parameter combinations were successful.")
        return
    
    # Compare results
    print(f"\n{'='*100}")
    print("📈 GENERATION PARAMETERS COMPARISON RESULTS")
    print(f"{'='*100}")
    
    # Create comprehensive comparison
    print(f"{'Rank':<4} {'Description':<35} {'Tokens':<7} {'Temp':<5} {'Avg Len':<8} {'Consist':<8} {'Trunc':<6} {'Time':<5}")
    print("-" * 100)
    
    # Sort by a composite score (consistency - truncation_rate + length_adequacy)
    for result in successful_results:
        truncation_rate = result['total_truncated'] / (len(result['results']) * 3)
        length_adequacy = min(1.0, result['overall_avg_length'] / 400)  # Target ~400 chars
        composite_score = result['overall_consistency'] - truncation_rate + length_adequacy
        result['composite_score'] = composite_score
    
    successful_results.sort(key=lambda x: x['composite_score'], reverse=True)
    
    for i, result in enumerate(successful_results, 1):
        truncation_rate = result['total_truncated'] / (len(result['results']) * 3)
        print(f"{i:<4} {result['description'][:34]:<35} {result['max_tokens']:<7} "
              f"{result['temperature']:<5} {result['overall_avg_length']:<8.0f} "
              f"{result['overall_consistency']:<8.3f} {result['total_truncated']:<6} "
              f"{result['overall_time']:<5.1f}")
    
    if successful_results:
        best_params = successful_results[0]
        print(f"\n🏆 BEST PARAMETER COMBINATION:")
        print(f"   📊 Configuration: max_tokens={best_params['max_tokens']}, temperature={best_params['temperature']}")
        print(f"   📝 Description: {best_params['description']}")
        print(f"   📏 Average Length: {best_params['overall_avg_length']:.0f} characters")
        print(f"   🎯 Consistency Score: {best_params['overall_consistency']:.3f}")
        print(f"   ✂️  Truncated Responses: {best_params['total_truncated']}/{len(best_params['results'])*3}")
        print(f"   ⏱️  Average Time: {best_params['overall_time']:.2f}s")
        
        print(f"\n💡 ANALYSIS:")
        if best_params['total_truncated'] == 0:
            print("✅ No truncated responses - max_tokens is sufficient")
        else:
            print(f"⚠️  {best_params['total_truncated']} truncated responses - consider increasing max_tokens")
        
        if best_params['overall_consistency'] > 0.9:
            print("✅ High consistency - temperature setting is appropriate")
        elif best_params['overall_consistency'] > 0.7:
            print("⚠️  Moderate consistency - consider lowering temperature")
        else:
            print("❌ Low consistency - temperature may be too high")
        
        print(f"\n🔧 TO IMPLEMENT THE BEST PARAMETERS:")
        print(f"   1. In app/rag_pipeline.py, find the _generate_response method")
        print(f"   2. Change max_tokens=300 to max_tokens={best_params['max_tokens']}")
        print(f"   3. Change temperature=0.7 to temperature={best_params['temperature']}")
        print(f"   4. Restart the application and test!")

def run_detailed_temperature_analysis():
    """Run detailed analysis focusing on temperature effects."""
    print(f"\n{'='*80}")
    print("🌡️  DETAILED TEMPERATURE ANALYSIS")
    print(f"{'='*80}")
    
    temperatures = [0.0, 0.1, 0.3, 0.5, 0.7, 0.9]
    
    for temp in temperatures:
        print(f"\n🌡️  Testing Temperature: {temp}")
        result = test_generation_parameters(500, temp, f"Temperature {temp} Analysis")
        
        if result:
            print(f"   Consistency Impact: {result['overall_consistency']:.3f}")
            print(f"   Response Variability: {'Low' if result['overall_consistency'] > 0.9 else 'Medium' if result['overall_consistency'] > 0.7 else 'High'}")

if __name__ == "__main__":
    print("Choose experiment type:")
    print("1. Full Parameter Optimization")
    print("2. Temperature Analysis Only")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        run_detailed_temperature_analysis()
    else:
        run_generation_experiments()