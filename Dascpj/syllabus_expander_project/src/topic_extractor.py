from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import re
from collections import Counter

class TopicExtractor:
    """Extract topics from course description using NLP techniques"""
    
    def __init__(self):
        """Initialize the topic extractor"""
        pass
    
    def extract_keywords_basic(self, text):
        """
        Extract keywords using basic text processing
        
        Args:
            text (str): Input text
            
        Returns:
            list: List of keywords
        """
        # Remove special characters and split
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'such', 'very', 'also', 'just', 'more', 'most',
            'about', 'into', 'through', 'during', 'before', 'after', 'above',
            'below', 'between', 'under', 'again', 'further', 'then', 'once'
        }
        
        # Filter stop words
        keywords = [w for w in words if w not in stop_words]
        
        # Count frequency
        word_freq = Counter(keywords)
        
        # Return top keywords
        return [word for word, _ in word_freq.most_common(20)]
    
    def split_into_sentences(self, text):
        """Split text into sentences"""
        # Basic sentence splitting
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    def extract_topics_tfidf(self, course_description, num_topics=6):
        """
        Extract topics using TF-IDF vectorization
        
        Args:
            course_description (str): Course description text
            num_topics (int): Number of topics to extract
            
        Returns:
            list: List of extracted topics
        """
        sentences = self.split_into_sentences(course_description)
        
        if len(sentences) < 2:
            return self.extract_keywords_basic(course_description)[:num_topics]
        
        try:
            vectorizer = TfidfVectorizer(
                max_features=min(50, len(sentences) * 10),
                stop_words='english',
                ngram_range=(1, 3)
            )
            tfidf_matrix = vectorizer.fit_transform(sentences)
            
            # Get feature names
            feature_names = vectorizer.get_feature_names_out()
            
            # Calculate mean TF-IDF scores
            tfidf_scores = np.asarray(tfidf_matrix.mean(axis=0)).ravel()
            
            # Get top topics
            top_indices = tfidf_scores.argsort()[-num_topics:][::-1]
            topics = [feature_names[i] for i in top_indices]
            
            return topics
            
        except Exception as e:
            print(f"TF-IDF extraction failed: {e}")
            return self.extract_keywords_basic(course_description)[:num_topics]
    
    def extract_topics(self, course_description, course_title="", num_topics=6, method='tfidf'):
        """
        Main method to extract topics from course description
        
        Args:
            course_description (str): Course description text
            course_title (str): Course title (optional, for context)
            num_topics (int): Number of topics to extract
            method (str): Extraction method ('tfidf')
            
        Returns:
            list: List of extracted topics
        """
        # Combine title and description
        full_text = f"{course_title}. {course_description}"
        
        topics = self.extract_topics_tfidf(full_text, num_topics)
        
        # Clean and format topics
        topics = [topic.strip().title() for topic in topics if topic.strip()]
        
        # Remove duplicates
        seen = set()
        unique_topics = []
        for topic in topics:
            if topic.lower() not in seen:
                seen.add(topic.lower())
                unique_topics.append(topic)
        
        return unique_topics[:num_topics]
    
    def enrich_topics(self, topics, course_description):
        """
        Enrich topics with additional context
        
        Args:
            topics (list): List of topics
            course_description (str): Course description
            
        Returns:
            dict: Dictionary of topics with enriched information
        """
        enriched_topics = {}
        sentences = self.split_into_sentences(course_description)
        
        for topic in topics:
            # Find sentences mentioning this topic
            relevant_sentences = []
            for sent in sentences:
                if topic.lower() in sent.lower():
                    relevant_sentences.append(sent)
            
            enriched_topics[topic] = {
                'name': topic,
                'context': relevant_sentences[:2] if relevant_sentences else [],
                'keywords': self.extract_keywords_basic(topic)
            }
        
        return enriched_topics


# Standalone function
def extract_topics_from_text(course_description, course_title="", num_topics=6):
    """Convenience function to extract topics"""
    extractor = TopicExtractor()
    return extractor.extract_topics(course_description, course_title, num_topics)
