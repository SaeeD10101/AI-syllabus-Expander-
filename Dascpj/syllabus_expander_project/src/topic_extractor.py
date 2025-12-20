import spacy
import subprocess
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

# Lazy loading function for spaCy model
def load_spacy_model():
    """Load spaCy model, download if not available"""
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        print("Downloading spaCy model 'en_core_web_sm'...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        return spacy.load("en_core_web_sm")

# Global variable for lazy initialization
_nlp = None

def get_nlp():
    """Get or initialize the spaCy NLP model"""
    global _nlp
    if _nlp is None:
        _nlp = load_spacy_model()
    return _nlp


class TopicExtractor:
    """Extract topics from course description using NLP techniques"""
    
    def __init__(self):
        """Initialize the topic extractor with spaCy model"""
        self.nlp = get_nlp()
    
    def extract_keywords(self, text):
        """
        Extract keywords from text using noun chunks and named entities
        
        Args:
            text (str): Input text to extract keywords from
            
        Returns:
            list: List of extracted keywords
        """
        doc = self.nlp(text)
        
        # Extract noun chunks
        noun_chunks = [chunk.text.lower() for chunk in doc.noun_chunks]
        
        # Extract named entities
        entities = [ent.text.lower() for ent in doc.ents]
        
        # Combine and deduplicate
        keywords = list(set(noun_chunks + entities))
        
        return keywords
    
    def extract_topics_tfidf(self, course_description, num_topics=6):
        """
        Extract topics using TF-IDF vectorization
        
        Args:
            course_description (str): Course description text
            num_topics (int): Number of topics to extract
            
        Returns:
            list: List of extracted topics
        """
        # Process text with spaCy
        doc = self.nlp(course_description)
        
        # Get sentences
        sentences = [sent.text for sent in doc.sents]
        
        if len(sentences) < 2:
            # If too few sentences, extract keywords directly
            return self.extract_keywords(course_description)[:num_topics]
        
        # TF-IDF Vectorization
        try:
            vectorizer = TfidfVectorizer(
                max_features=min(50, len(sentences) * 10),
                stop_words='english',
                ngram_range=(1, 3)  # Unigrams to trigrams
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
            # Fallback to keyword extraction
            return self.extract_keywords(course_description)[:num_topics]
    
    def extract_topics_clustering(self, course_description, num_topics=6):
        """
        Extract topics using clustering on sentence embeddings
        
        Args:
            course_description (str): Course description text
            num_topics (int): Number of topic clusters
            
        Returns:
            list: List of representative topics from each cluster
        """
        doc = self.nlp(course_description)
        sentences = [sent.text for sent in doc.sents]
        
        if len(sentences) < num_topics:
            return self.extract_keywords(course_description)[:num_topics]
        
        try:
            # Get sentence vectors
            sentence_vectors = [self.nlp(sent).vector for sent in sentences]
            
            # Cluster sentences
            kmeans = KMeans(n_clusters=min(num_topics, len(sentences)), random_state=42)
            kmeans.fit(sentence_vectors)
            
            # Extract representative keywords from each cluster
            topics = []
            for i in range(kmeans.n_clusters):
                cluster_sentences = [sentences[j] for j in range(len(sentences)) if kmeans.labels_[j] == i]
                if cluster_sentences:
                    # Extract keywords from cluster sentences
                    cluster_text = ' '.join(cluster_sentences)
                    cluster_keywords = self.extract_keywords(cluster_text)
                    if cluster_keywords:
                        topics.append(cluster_keywords[0])
            
            return topics[:num_topics]
            
        except Exception as e:
            print(f"Clustering extraction failed: {e}")
            return self.extract_topics_tfidf(course_description, num_topics)
    
    def extract_topics(self, course_description, course_title="", num_topics=6, method='tfidf'):
        """
        Main method to extract topics from course description
        
        Args:
            course_description (str): Course description text
            course_title (str): Course title (optional, for context)
            num_topics (int): Number of topics to extract
            method (str): Extraction method ('tfidf' or 'clustering')
            
        Returns:
            list: List of extracted topics
        """
        # Combine title and description for better context
        full_text = f"{course_title}. {course_description}"
        
        if method == 'clustering':
            topics = self.extract_topics_clustering(full_text, num_topics)
        else:
            topics = self.extract_topics_tfidf(full_text, num_topics)
        
        # Clean and format topics
        topics = [topic.strip().title() for topic in topics if topic.strip()]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_topics = []
        for topic in topics:
            if topic.lower() not in seen:
                seen.add(topic.lower())
                unique_topics.append(topic)
        
        return unique_topics[:num_topics]
    
    def enrich_topics(self, topics, course_description):
        """
        Enrich topics with additional context from course description
        
        Args:
            topics (list): List of topics
            course_description (str): Course description
            
        Returns:
            dict: Dictionary of topics with enriched information
        """
        enriched_topics = {}
        doc = self.nlp(course_description)
        
        for topic in topics:
            # Find sentences mentioning this topic
            relevant_sentences = []
            for sent in doc.sents:
                if topic.lower() in sent.text.lower():
                    relevant_sentences.append(sent.text)
            
            enriched_topics[topic] = {
                'name': topic,
                'context': relevant_sentences[:2] if relevant_sentences else [],
                'keywords': self.extract_keywords(topic)
            }
        
        return enriched_topics


# Standalone function for quick topic extraction
def extract_topics_from_text(course_description, course_title="", num_topics=6):
    """
    Convenience function to extract topics without instantiating the class
    
    Args:
        course_description (str): Course description text
        course_title (str): Course title (optional)
        num_topics (int): Number of topics to extract
        
    Returns:
        list: List of extracted topics
    """
    extractor = TopicExtractor()
    return extractor.extract_topics(course_description, course_title, num_topics)


# Example usage and testing
if __name__ == "__main__":
    # Test the topic extractor
    sample_description = """
    This course covers the fundamentals of machine learning including supervised learning,
    unsupervised learning, and reinforcement learning. Students will learn about neural networks,
    decision trees, clustering algorithms, and natural language processing. The course includes
    hands-on projects using Python and popular ML libraries like scikit-learn and TensorFlow.
    Topics include data preprocessing, feature engineering, model evaluation, and deployment.
    """
    
    extractor = TopicExtractor()
    
    print("Testing TF-IDF method:")
    topics_tfidf = extractor.extract_topics(sample_description, method='tfidf')
    print(topics_tfidf)
    
    print("\nTesting Clustering method:")
    topics_clustering = extractor.extract_topics(sample_description, method='clustering')
    print(topics_clustering)
    
    print("\nEnriched topics:")
    enriched = extractor.enrich_topics(topics_tfidf, sample_description)
    for topic, info in enriched.items():
        print(f"\n{topic}:")
        print(f"  Context: {info['context']}")
        print(f"  Keywords: {info['keywords']}")
