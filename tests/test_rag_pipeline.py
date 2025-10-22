import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
import requests
import time
import json
from typing import Dict, List, Any
from dotenv import load_dotenv
from app.rag_pipeline import RAGPipeline

# Load environment variables for testing
load_dotenv()

class TestRAGPipeline:
    """
    Test suite for RAG Pipeline functionality.
    
    This test suite includes various test cases that students can use
    to learn about testing GenAI applications. Some tests may reveal
    intentional issues in the implementation.
    """
    
    @pytest.fixture(scope="class")
    def rag_pipeline(self):
        """Create a RAG pipeline instance for testing."""
        return RAGPipeline()
    
    def test_pipeline_initialization(self, rag_pipeline):
        """Test that the RAG pipeline initializes correctly."""
        assert rag_pipeline.cohere_client is not None
        assert rag_pipeline.vector_db is not None
        assert rag_pipeline.collection is not None
        assert hasattr(rag_pipeline, 'stats')
        assert isinstance(rag_pipeline.stats, dict)
    
    def test_health_check(self, rag_pipeline):
        """Test the health check functionality."""
        health = rag_pipeline.health_check()
        
        assert isinstance(health, dict)
        assert 'cohere_client' in health
        assert 'vector_db' in health
        assert 'collection' in health
        assert 'documents_loaded' in health
        
        # These should pass if properly configured
        assert health['cohere_client'] == True
        assert health['vector_db'] == True
        assert health['collection'] == True
    
    def test_document_loading(self, rag_pipeline):
        """Test that documents are loaded into the vector database."""
        stats = rag_pipeline.get_stats()
        assert stats['documents_loaded'] > 0, "No documents loaded"
        
        # Check that collection has documents
        doc_count = rag_pipeline.collection.count()
        assert doc_count > 0, "Collection is empty"
    
    def test_basic_query_processing(self, rag_pipeline):
        """Test basic query processing functionality."""
        query = "What are the key challenges in testing GenAI applications?"
        response = rag_pipeline.query(query)
        
        assert isinstance(response, dict)
        assert 'response' in response
        assert 'sources' in response
        assert 'total_time' in response
        
        assert len(response['response']) > 0, "Empty response"
        assert isinstance(response['sources'], list)
        assert response['total_time'] > 0
    
    def test_query_response_quality(self, rag_pipeline):
        """Test the quality of responses to various queries."""
        test_queries = [
            "What is hallucination in GenAI?",
            "How do I measure RAG system performance?",
            "What are best practices for testing chatbots?",
        ]
        
        for query in test_queries:
            response = rag_pipeline.query(query)
            
            # Basic quality checks
            assert len(response['response']) > 50, f"Response too short for query: {query}"
            assert not response['response'].startswith("I don't know"), f"Unhelpful response for: {query}"
            
            # Check for sources
            assert len(response['sources']) > 0, f"No sources returned for: {query}"
    
    def test_response_time_performance(self, rag_pipeline):
        """Test that response times are within acceptable limits."""
        query = "What are evaluation metrics for RAG systems?"
        
        start_time = time.time()
        response = rag_pipeline.query(query)
        end_time = time.time()
        
        total_time = end_time - start_time
        reported_time = response.get('total_time', float('inf'))
        
        # Response should be fast enough for good UX
        assert total_time < 10.0, f"Response too slow: {total_time:.2f}s"
        
        # Reported time should be accurate
        assert abs(total_time - reported_time) < 1.0, "Timing measurement inaccurate"
    
    def test_retrieval_relevance(self, rag_pipeline):
        """Test that retrieved documents are relevant to queries."""
        query = "testing GenAI applications"
        response = rag_pipeline.query(query)
        
        sources = response.get('sources', [])
        assert len(sources) > 0, "No sources retrieved"
        
        # Check that sources contain relevant keywords
        relevant_keywords = ['test', 'genai', 'evaluation', 'quality']
        
        for source in sources[:3]:  # Check top 3 sources
            content = source['content'].lower()
            has_relevant_keyword = any(keyword in content for keyword in relevant_keywords)
            
            # This might fail due to chunking issues - good for students to discover
            assert has_relevant_keyword, f"Source doesn't seem relevant: {content[:100]}"
    
    def test_empty_query_handling(self, rag_pipeline):
        """Test handling of empty or invalid queries."""
        test_cases = ["", "   ", "\n\t", None]
        
        for invalid_query in test_cases:
            try:
                response = rag_pipeline.query(invalid_query)
                # Should handle gracefully with error message
                assert 'error' in response or 'apologize' in response['response'].lower()
            except Exception as e:
                # Should not crash with unhandled exceptions
                pytest.fail(f"Unhandled exception for empty query: {e}")
    
    def test_very_long_query_handling(self, rag_pipeline):
        """Test handling of extremely long queries."""
        # Create a very long query
        long_query = "What is testing? " * 200  # 600+ words
        
        response = rag_pipeline.query(long_query)
        
        # Should handle without crashing
        assert isinstance(response, dict)
        assert 'response' in response
        
        # Response time should still be reasonable
        assert response.get('total_time', 0) < 15.0, "Very slow response for long query"
    
    def test_special_characters_query(self, rag_pipeline):
        """Test handling of queries with special characters."""
        special_queries = [
            "What is GenAI testing? 🤖",
            "How do I test APIs & endpoints?",
            "Testing with symbols: @#$%^&*()",
            "Query with\nnewlines\nand\ttabs"
        ]
        
        for query in special_queries:
            response = rag_pipeline.query(query)
            
            # Should handle gracefully
            assert isinstance(response, dict)
            assert 'response' in response
            assert len(response['response']) > 0
    
    def test_out_of_domain_queries(self, rag_pipeline):
        """Test handling of queries outside the knowledge domain."""
        off_topic_queries = [
            "What's the weather today?",
            "How do I cook pasta?",
            "What is the capital of France?",
            "Tell me about quantum physics"
        ]
        
        for query in off_topic_queries:
            response = rag_pipeline.query(query)
            
            # Should acknowledge when information isn't available
            response_text = response['response'].lower()
            
            # Look for appropriate responses to out-of-domain queries
            appropriate_responses = [
                'don\'t have information',
                'not in my knowledge',
                'context doesn\'t contain',
                'can\'t find relevant',
                'outside my domain'
            ]
            
            # This test might fail if the model hallucinates - good discovery for students
            has_appropriate_response = any(phrase in response_text for phrase in appropriate_responses)
            
            if not has_appropriate_response:
                print(f"Warning: Potential hallucination for off-topic query: {query}")
                print(f"Response: {response['response'][:200]}...")
    
    def test_consistency_across_similar_queries(self, rag_pipeline):
        """Test that similar queries get consistent responses."""
        similar_queries = [
            "What is hallucination in AI?",
            "How do I detect AI hallucinations?",
            "What are AI hallucination problems?"
        ]
        
        responses = []
        for query in similar_queries:
            response = rag_pipeline.query(query)
            responses.append(response['response'])
        
        # Responses should have some similarity in content
        # This is a simplified check - in practice, you'd use semantic similarity
        common_words = set()
        for response in responses:
            words = set(response.lower().split())
            if not common_words:
                common_words = words
            else:
                common_words = common_words.intersection(words)
        
        # Should have some common vocabulary
        assert len(common_words) > 3, "Responses too inconsistent for similar queries"
    
    def test_source_attribution_accuracy(self, rag_pipeline):
        """Test that source attribution is accurate."""
        query = "What are evaluation metrics for RAG systems?"
        response = rag_pipeline.query(query)
        
        sources = response.get('sources', [])
        response_text = response['response']
        
        if sources:
            # Check if response content can be traced to sources
            # This is a simplified check - production would need more sophisticated verification
            
            source_content = ' '.join([source['content'] for source in sources])
            response_words = set(response_text.lower().split())
            source_words = set(source_content.lower().split())
            
            # Response should share significant vocabulary with sources
            overlap = len(response_words.intersection(source_words))
            overlap_ratio = overlap / len(response_words) if response_words else 0
            
            # This might fail if the model adds too much external knowledge
            assert overlap_ratio > 0.3, f"Low overlap between response and sources: {overlap_ratio:.2f}"
    
    def test_concurrent_query_handling(self, rag_pipeline):
        """Test handling multiple concurrent queries."""
        import concurrent.futures
        
        query = "What is the importance of testing GenAI applications?"
        num_concurrent = 5
        
        def process_query():
            return rag_pipeline.query(query)
        
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            futures = [executor.submit(process_query) for _ in range(num_concurrent)]
            responses = [future.result() for future in futures]
        
        total_time = time.time() - start_time
        
        # All responses should be successful
        for i, response in enumerate(responses):
            assert isinstance(response, dict), f"Response {i} is not a dict"
            assert 'response' in response, f"Response {i} missing response field"
            assert len(response['response']) > 0, f"Response {i} is empty"
        
        # Total time should be reasonable for concurrent processing
        avg_time_per_query = total_time / num_concurrent
        assert avg_time_per_query < 5.0, f"Concurrent processing too slow: {avg_time_per_query:.2f}s per query"
    
    def test_statistics_tracking(self, rag_pipeline):
        """Test that statistics are properly tracked."""
        initial_stats = rag_pipeline.get_stats()
        initial_count = initial_stats['queries_processed']
        
        # Process a few queries
        for i in range(3):
            rag_pipeline.query(f"Test query number {i}")
        
        updated_stats = rag_pipeline.get_stats()
        
        # Stats should be updated
        assert updated_stats['queries_processed'] == initial_count + 3
        assert updated_stats['average_response_time'] > 0
        assert updated_stats['documents_loaded'] > 0
    
    def test_error_handling_robustness(self, rag_pipeline):
        """Test error handling in various failure scenarios."""
        # Test with malformed input
        malformed_inputs = [
            {"not": "a string"},
            123,
            ["list", "input"],
            object()
        ]
        
        for malformed_input in malformed_inputs:
            try:
                # This should handle gracefully or raise appropriate exceptions
                response = rag_pipeline.query(malformed_input)
                assert 'error' in response or isinstance(response.get('response'), str)
            except (TypeError, ValueError) as e:
                # These are acceptable exceptions for malformed input
                pass
            except Exception as e:
                pytest.fail(f"Unexpected exception for malformed input {malformed_input}: {e}")


class TestAPIntegration:
    """Test the Flask API endpoints."""
    
    BASE_URL = "http://localhost:5000"
    
    def test_health_endpoint(self):
        """Test the health check endpoint."""
        response = requests.get(f"{self.BASE_URL}/api/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'status' in data
        assert 'rag_pipeline' in data
        assert 'cohere_api_key' in data
    
    def test_chat_endpoint_basic(self):
        """Test basic chat endpoint functionality."""
        payload = {"message": "What is testing GenAI applications?"}
        response = requests.post(f"{self.BASE_URL}/api/chat", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'response' in data
        assert 'sources' in data
        assert 'response_time' in data
        assert data['status'] == 'success'
    
    def test_chat_endpoint_error_handling(self):
        """Test chat endpoint error handling."""
        # Test empty message
        payload = {"message": ""}
        response = requests.post(f"{self.BASE_URL}/api/chat", json=payload)
        
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data
    
    def test_stats_endpoint(self):
        """Test the statistics endpoint."""
        response = requests.get(f"{self.BASE_URL}/api/stats")
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'queries_processed' in data
        assert 'average_response_time' in data
        assert 'documents_loaded' in data


class TestQualityMetrics:
    """Test quality metrics for evaluation."""
    
    @pytest.fixture(scope="class")
    def rag_pipeline(self):
        return RAGPipeline()
    
    def test_response_length_distribution(self, rag_pipeline):
        """Test that responses have appropriate length distribution."""
        queries = [
            "What is GenAI testing?",
            "How do I evaluate RAG systems comprehensively?",
            "Quick question about testing",
            "Can you explain in detail the complete process of testing generative AI applications?"
        ]
        
        response_lengths = []
        for query in queries:
            response = rag_pipeline.query(query)
            response_lengths.append(len(response['response']))
        
        # Responses should vary in length based on query complexity
        assert max(response_lengths) > min(response_lengths) * 1.5, "Response lengths too uniform"
        
        # All responses should be substantive
        assert all(length > 30 for length in response_lengths), "Some responses too short"
    
    def test_keyword_relevance(self, rag_pipeline):
        """Test that responses contain relevant keywords from queries."""
        test_cases = [
            {
                "query": "evaluation metrics for RAG",
                "expected_keywords": ["evaluation", "metrics", "rag", "performance"]
            },
            {
                "query": "hallucination detection methods",
                "expected_keywords": ["hallucination", "detection", "methods"]
            }
        ]
        
        for case in test_cases:
            response = rag_pipeline.query(case["query"])
            response_text = response['response'].lower()
            
            found_keywords = []
            for keyword in case["expected_keywords"]:
                if keyword.lower() in response_text:
                    found_keywords.append(keyword)
            
            # Should find most relevant keywords
            relevance_ratio = len(found_keywords) / len(case["expected_keywords"])
            assert relevance_ratio >= 0.5, f"Low keyword relevance for '{case['query']}': {found_keywords}"
    
    def test_factual_consistency(self, rag_pipeline):
        """Test for basic factual consistency in responses."""
        # Ask the same question in different ways
        base_query = "What is the purpose of testing GenAI applications?"
        variations = [
            "Why do we test GenAI applications?",
            "What's the goal of GenAI testing?",
            "Why is testing important for GenAI?"
        ]
        
        responses = []
        for query in [base_query] + variations:
            response = rag_pipeline.query(query)
            responses.append(response['response'])
        
        # Check for contradictory statements (simplified check)
        # In practice, you'd use more sophisticated consistency checking
        
        all_text = ' '.join(responses).lower()
        
        # Look for contradictory patterns
        contradictions = [
            ('important' in all_text and 'not important' in all_text),
            ('necessary' in all_text and 'unnecessary' in all_text),
            ('should test' in all_text and 'should not test' in all_text)
        ]
        
        assert not any(contradictions), "Potential contradictions found in responses"


# STUDENTS: Utility functions for test data and evaluation
def generate_test_queries() -> List[str]:
    """Generate a set of test queries for evaluation."""
    return [
        "What are the main challenges in testing GenAI applications?",
        "How do I measure hallucination rates?",
        "What evaluation metrics should I use for RAG systems?",
        "How can I test for bias in AI responses?",
        "What are best practices for production GenAI monitoring?",
        "How do I validate retrieval quality?",
        "What is the difference between unit and integration testing for GenAI?",
        "How do I handle non-deterministic behavior in tests?",
        "What safety measures should I implement?",
        "How do I test model performance under load?"
    ]

def calculate_response_quality_score(response: str, sources: List[Dict]) -> float:
    """Calculate a simple quality score for responses."""
    score = 0.0
    
    # Length check (responses should be substantive)
    if len(response) > 50:
        score += 0.2
    if len(response) > 150:
        score += 0.2
    
    # Source utilization
    if len(sources) > 0:
        score += 0.2
    if len(sources) >= 3:
        score += 0.1
    
    # Content quality indicators
    quality_indicators = [
        'test', 'evaluation', 'metric', 'genai', 'important', 
        'system', 'quality', 'performance', 'measure'
    ]
    
    found_indicators = sum(1 for indicator in quality_indicators 
                          if indicator in response.lower())
    
    score += min(found_indicators / len(quality_indicators), 0.3)
    
    return min(score, 1.0)


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"])