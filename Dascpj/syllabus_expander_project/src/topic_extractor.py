# topic_extractor.py

import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter
import re
import numpy as np

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

class TopicExtractor:
    """Extract topics and generate module structure from course description"""
    
    def __init__(self):
        self.stop_words = set(['course', 'student', 'students', 'learn', 'learning', 
                               'will', 'including', 'include', 'covers', 'cover',
                               'provides', 'provide', 'introduction', 'basic', 'fundamental'])
    
    def extract_keywords(self, text, top_n=15):
        """Extract important keywords using TF-IDF"""
        # Combine all text
        corpus = [text]
        
        # TF-IDF extraction
        vectorizer = TfidfVectorizer(
            max_features=top_n,
            stop_words='english',
            ngram_range=(1, 2),  # unigrams and bigrams
            min_df=1,
            max_df=0.8
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform(corpus)
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf_matrix.toarray()[0]
            
            # Get top keywords with scores
            keyword_scores = list(zip(feature_names, scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Filter out stop words
            keywords = [kw for kw, score in keyword_scores 
                       if kw.lower() not in self.stop_words and len(kw) > 2]
            
            return keywords[:top_n]
        except:
            return self.extract_keywords_fallback(text, top_n)
    
    def extract_keywords_fallback(self, text, top_n=15):
        """Fallback keyword extraction using spaCy"""
        doc = nlp(text)
        
        # Extract noun chunks
        noun_chunks = [chunk.text.lower() for chunk in doc.noun_chunks]
        
        # Count frequency
        word_freq = Counter(noun_chunks)
        
        # Remove stop words
        filtered = [(word, freq) for word, freq in word_freq.most_common() 
                   if word not in self.stop_words and len(word) > 2]
        
        return [word for word, freq in filtered[:top_n]]
    
    def extract_noun_phrases(self, text):
        """Extract noun phrases using spaCy"""
        doc = nlp(text)
        noun_phrases = []
        
        for chunk in doc.noun_chunks:
            # Clean and filter
            phrase = chunk.text.lower().strip()
            if (len(phrase.split()) <= 3 and 
                phrase not in self.stop_words and 
                len(phrase) > 3):
                noun_phrases.append(phrase)
        
        return list(set(noun_phrases))
    
    def extract_entities(self, text):
        """Extract named entities"""
        doc = nlp(text)
        entities = []
        
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'GPE', 'NORP', 'FAC', 'EVENT']:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_
                })
        
        return entities
    
    def cluster_keywords(self, keywords, n_clusters=6):
        """Cluster keywords into potential topics"""
        if len(keywords) < n_clusters:
            n_clusters = len(keywords)
        
        # Simple clustering based on word similarity
        # For pure NLP, we'll use character-based similarity
        clusters = {i: [] for i in range(n_clusters)}
        
        # Distribute keywords across clusters
        for idx, keyword in enumerate(keywords):
            cluster_id = idx % n_clusters
            clusters[cluster_id].append(keyword)
        
        return clusters
    
    def generate_module_title(self, keywords):
        """Generate module title from keywords"""
        if not keywords:
            return "General Concepts"
        
        # Use first 1-2 keywords
        main_keyword = keywords[0].title()
        
        # Add context
        prefixes = ["Introduction to", "Fundamentals of", "Advanced", "Practical"]
        suffixes = ["Concepts", "Principles", "Applications", "Techniques"]
        
        # Simple heuristic
        if len(main_keyword.split()) == 1:
            return f"{prefixes[0]} {main_keyword}"
        else:
            return main_keyword.title()
    
    def estimate_hours(self, subtopic_count, total_duration):
        """Estimate hours per module"""
        # Parse duration (e.g., "12 weeks" -> 12)
        duration_match = re.search(r'(\d+)', str(total_duration))
        if duration_match:
            weeks = int(duration_match.group(1))
            total_hours = weeks * 3  # Assume 3 hours per week
            hours_per_module = total_hours / max(subtopic_count, 1)
            return max(4, min(12, int(hours_per_module)))
        return 6  # Default
    
    def extract_topics_and_modules(self, course_title, description, scope, duration):
        """Main method: Extract topics and generate module structure"""
        
        # Combine all text
        full_text = f"{course_title}. {description}. {scope}"
        
        # Step 1: Extract keywords
        keywords = self.extract_keywords(full_text, top_n=20)
        
        # Step 2: Extract noun phrases
        noun_phrases = self.extract_noun_phrases(full_text)
        
        # Step 3: Combine and deduplicate
        all_topics = list(set(keywords + noun_phrases))[:15]
        
        # Step 4: Cluster into modules (4-8 modules)
        n_modules = min(max(4, len(all_topics) // 3), 8)
        clusters = self.cluster_keywords(all_topics, n_modules)
        
        # Step 5: Generate module structure
        modules = []
        for i, (cluster_id, cluster_keywords) in enumerate(clusters.items()):
            if not cluster_keywords:
                continue
                
            module = {
                'id': i + 1,
                'title': self.generate_module_title(cluster_keywords),
                'subtopics': cluster_keywords[:4],  # Max 4 subtopics per module
                'keywords': cluster_keywords,
                'hours': self.estimate_hours(n_modules, duration)
            }
            modules.append(module)
        
        # Step 6: Ensure we have 4-8 modules
        if len(modules) < 4:
            # Add generic modules
            while len(modules) < 4:
                modules.append({
                    'id': len(modules) + 1,
                    'title': f"Additional Concepts",
                    'subtopics': ["Related topics", "Case studies"],
                    'keywords': [],
                    'hours': 6
                })
        
        return {
            'modules': modules[:8],  # Max 8 modules
            'extracted_keywords': keywords,
            'total_topics': len(all_topics)
        }


# Test the extractor
if __name__ == "__main__":
    import json
    
    # Load sample course
    with open('synthetic_courses.json', 'r') as f:
        courses = json.load(f)
    
    sample_course = courses[0]
    
    extractor = TopicExtractor()
    result = extractor.extract_topics_and_modules(
        sample_course['title'],
        sample_course['description'],
        sample_course['scope'],
        sample_course['duration']
    )
    
    print("=" * 60)
    print(f"COURSE: {sample_course['title']}")
    print("=" * 60)
    print(f"\nExtracted {len(result['modules'])} modules:")
    print(f"Keywords found: {', '.join(result['extracted_keywords'][:10])}")
    print("\nMODULES:")
    for module in result['modules']:
        print(f"\n{module['id']}. {module['title']} ({module['hours']} hours)")
        print(f"   Subtopics: {', '.join(module['subtopics'])}")