import spacy
import subprocess
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

# Global variable for lazy initialization
_nlp = None
_model_available = False

def check_model_available():
    """Check if spaCy model is available without downloading"""
    try:
        spacy.load("en_core_web_sm")
        return True
    except OSError:
        return False

def download_spacy_model():
    """Download spaCy model - call this explicitly when needed"""
    try:
        print("Downloading spaCy model 'en_core_web_sm'...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        return True
    except Exception as e:
        print(f"Failed to download spaCy model: {e}")
        return False

def get_nlp():
    """Get or initialize the spaCy NLP model"""
    global _nlp, _model_available
    
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
            _model_available = True
        except OSError:
            print("Warning: spaCy model 'en_core_web_sm' not found.")
            print("Please run: python -m spacy download en_core_web_sm")
            _model_available = False
            # Return a blank spaCy model as fallback
            _nlp = spacy.blank("en")
    
    return _nlp


class TopicExtractor:
    """Extract topics from course description using NLP techniques"""
    
    def __init__(self, skip_spacy=False):
        """
        Initialize the topic extractor
        
        Args:
            skip_spacy (bool): If True, use basic text processing instead of spaCy
        """
        self.skip_spacy = skip_spacy
        if not skip_spacy:
            self.nlp = get_nlp()
            self.model_available = _model_available
        else:
            self.nlp = None
            self.model_available = False
    
    def extract_keywords_basic(self, text):
        """
        Extract keywords using basic text processing (no spaCy required)
        
        Args:
            text (str): Input text
            
        Returns:
            list: List of keywords
        """
        import re
        
        # Remove special characters and split
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'such', 'very', 'also', 'just', 'more', 'most'
        }
        
        # Filter stop words
        keywords = [w for w in words if w not in stop_words]
        
        # Count frequency
        from collections import Counter
        word_freq = Counter(keywords)
        
        # Return top keywords
        return [word for word, _ in word_freq.most_common(20)]
    
    def extract_keywords(self, text):
        """
        Extract keywords from text
        
        Args:
            text (str): Input text to extract keywords from
            
        Returns:
            list: List of extracted keywords
        """
        # Fallback to basic extraction if spaCy not available
        if not self.model_available or self.skip_spacy:
            return self.extract_keywords_basic(text)
        
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
        # Split into sentences (basic splitting if spaCy unavailable)
        if self.model_available and not self.skip_spacy:
            doc = self.nlp(course_description)
            sentences = [sent.text for sent in doc.sents]
        else:
            # Basic sentence splitting
            import re
            sentences = re.split(r'[.!?]+', course_description)
            sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 2:
            return self.extract_keywords(course_description)[:num_topics]
        
        # TF-IDF Vectorization
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
            return self.extract_keywords(course_description)[:num_topics]
    
    def extract_topics_clustering(self, course_description, num_topics=6):
        """
        Extract topics using clustering
        
        Args:
            course_description (str): Course description text
            num_topics (int): Number of topic clusters
            
        Returns:
            list: List of representative topics from each cluster
        """
        # Only use clustering if spaCy model is available (for vectors)
        if not self.model_available or self.skip_spacy:
            return self.extract_topics_tfidf(course_description, num_topics)
        
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
        Enrich topics with additional context
        
        Args:
            topics (list): List of topics
            course_description (str): Course description
            
        Returns:
            dict: Dictionary of topics with enriched information
        """
        enriched_topics = {}
        
        if self.model_available and not self.skip_spacy:
            doc = self.nlp(course_description)
            sentences = list(doc.sents)
        else:
            import re
            sentences = re.split(r'[.!?]+', course_description)
            sentences = [s.strip() for s in sentences if s.strip()]
        
        for topic in topics:
            # Find sentences mentioning this topic
            relevant_sentences = []
            for sent in sentences:
                sent_text = sent.text if hasattr(sent, 'text') else sent
                if topic.lower() in sent_text.lower():
                    relevant_sentences.append(sent_text)
            
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
    """
    extractor = TopicExtractor(skip_spacy=not check_model_available())
    return extractor.extract_topics(course_description, course_title, num_topics)


if __name__ == "__main__":
    # Test the topic extractor
    sample_description = """
    This course covers the fundamentals of machine learning including supervised learning,
    unsupervised learning, and reinforcement learning.
    """
    
    extractor = TopicExtractor()
    topics = extractor.extract_topics(sample_description)
    print(topics)
