import random
import re

# Fixed import - use relative import since both files are in src/
from .knowledge_base import DOMAIN_INDICATORS

class ModuleStructurer:
    """Structure extracted topics into organized modules"""
    
    def __init__(self):
        self.domain_indicators = DOMAIN_INDICATORS
    
    def detect_course_domain(self, course_description, course_title=""):
        """
        Detect the primary domain of the course
        
        Args:
            course_description (str): Course description
            course_title (str): Course title
            
        Returns:
            str: Detected domain (e.g., 'computer_science', 'business', 'engineering')
        """
        text = f"{course_title} {course_description}".lower()
        
        domain_scores = {}
        for domain, indicators in self.domain_indicators.items():
            score = sum(1 for indicator in indicators if indicator in text)
            domain_scores[domain] = score
        
        # Return domain with highest score, default to 'general'
        if max(domain_scores.values()) > 0:
            return max(domain_scores, key=domain_scores.get)
        return 'general'
    
    def group_topics_into_modules(self, topics, num_modules=4):
        """
        Group topics into logical modules
        
        Args:
            topics (list): List of topic strings
            num_modules (int): Desired number of modules
            
        Returns:
            list: List of modules, each containing grouped topics
        """
        if not topics:
            return []
        
        # Ensure we don't have more modules than topics
        num_modules = min(num_modules, len(topics))
        
        # Calculate topics per module
        topics_per_module = len(topics) // num_modules
        remainder = len(topics) % num_modules
        
        modules = []
        topic_index = 0
        
        for i in range(num_modules):
            # Distribute remainder topics across first modules
            module_size = topics_per_module + (1 if i < remainder else 0)
            module_topics = topics[topic_index:topic_index + module_size]
            
            if module_topics:  # Only add non-empty modules
                modules.append(module_topics)
                topic_index += module_size
        
        return modules
    
    def generate_module_names(self, modules, course_domain='general'):
        """
        Generate descriptive names for modules
        
        Args:
            modules (list): List of modules with topics
            course_domain (str): Course domain
            
        Returns:
            list: List of dictionaries with module info
        """
        module_prefixes = {
            'computer_science': ['Fundamentals of', 'Introduction to', 'Advanced', 'Applied'],
            'business': ['Principles of', 'Strategic', 'Operational', 'Advanced'],
            'engineering': ['Foundation of', 'Core Concepts in', 'Advanced Topics in', 'Applications of'],
            'mathematics': ['Introduction to', 'Theoretical', 'Applied', 'Advanced'],
            'science': ['Fundamentals of', 'Experimental', 'Theoretical', 'Advanced'],
            'general': ['Introduction to', 'Core Concepts in', 'Advanced Topics in', 'Applications of']
        }
        
        prefixes = module_prefixes.get(course_domain, module_prefixes['general'])
        
        structured_modules = []
        for i, module_topics in enumerate(modules):
            if not module_topics:
                continue
            
            # Generate module name based on first topic
            prefix = prefixes[i % len(prefixes)]
            main_topic = module_topics[0]
            
            module_name = f"Module {i+1}: {prefix} {main_topic}"
            
            structured_modules.append({
                'module_number': i + 1,
                'module_name': module_name,
                'topics': module_topics,
                'subtopics': self.generate_subtopics(module_topics)
            })
        
        return structured_modules
    
    def generate_subtopics(self, topics, subtopics_per_topic=3):
        """
        Generate subtopics for each topic
        
        Args:
            topics (list): List of topics
            subtopics_per_topic (int): Number of subtopics per topic
            
        Returns:
            dict: Dictionary mapping topics to their subtopics
        """
        subtopic_templates = [
            "Overview and Introduction",
            "Key Concepts and Principles",
            "Practical Applications",
            "Advanced Techniques",
            "Case Studies and Examples",
            "Best Practices",
            "Tools and Technologies",
            "Common Challenges",
            "Future Trends"
        ]
        
        subtopics_dict = {}
        for topic in topics:
            # Generate contextual subtopics
            subtopics = [
                f"{topic} - {subtopic_templates[j % len(subtopic_templates)]}"
                for j in range(subtopics_per_topic)
            ]
            subtopics_dict[topic] = subtopics
        
        return subtopics_dict
    
    def create_module_structure(self, topics, course_description="", course_title="", num_modules=4):
        """
        Main method to create complete module structure
        
        Args:
            topics (list): List of extracted topics
            course_description (str): Course description
            course_title (str): Course title
            num_modules (int): Desired number of modules
            
        Returns:
            dict: Complete module structure
        """
        # Detect course domain
        domain = self.detect_course_domain(course_description, course_title)
        
        # Group topics into modules
        module_groups = self.group_topics_into_modules(topics, num_modules)
        
        # Generate module names and structure
        structured_modules = self.generate_module_names(module_groups, domain)
        
        return {
            'course_domain': domain,
            'total_modules': len(structured_modules),
            'modules': structured_modules
        }
    
    def format_module_outline(self, module_structure):
        """
        Format module structure into readable outline
        
        Args:
            module_structure (dict): Module structure dictionary
            
        Returns:
            str: Formatted outline text
        """
        outline = f"Course Domain: {module_structure['course_domain'].replace('_', ' ').title()}\n"
        outline += f"Total Modules: {module_structure['total_modules']}\n\n"
        
        for module in module_structure['modules']:
            outline += f"{module['module_name']}\n"
            outline += "=" * len(module['module_name']) + "\n\n"
            
            for topic in module['topics']:
                outline += f"  • {topic}\n"
                if topic in module['subtopics']:
                    for subtopic in module['subtopics'][topic]:
                        outline += f"    - {subtopic}\n"
            outline += "\n"
        
        return outline


# Standalone function
def structure_topics_into_modules(topics, course_description="", course_title="", num_modules=4):
    """
    Convenience function to structure topics without instantiating the class
    
    Args:
        topics (list): List of topics
        course_description (str): Course description
        course_title (str): Course title
        num_modules (int): Number of modules
        
    Returns:
        dict: Module structure
    """
    structurer = ModuleStructurer()
    return structurer.create_module_structure(topics, course_description, course_title, num_modules)


# Example usage
if __name__ == "__main__":
    sample_topics = [
        "Machine Learning Fundamentals",
        "Neural Networks",
        "Natural Language Processing",
        "Computer Vision",
        "Reinforcement Learning",
        "Model Deployment"
    ]
    
    structurer = ModuleStructurer()
    module_structure = structurer.create_module_structure(
        topics=sample_topics,
        course_description="Advanced course in AI and ML",
        course_title="Artificial Intelligence",
        num_modules=3
    )
    
    print(structurer.format_module_outline(module_structure))
