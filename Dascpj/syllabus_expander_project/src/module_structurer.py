# module_structurer.py

import random
from knowledge_base import DOMAIN_INDICATORS

class ModuleStructurer:
    """Enhance module structure with additional metadata"""
    
    def __init__(self):
        self.module_prefixes = [
            "Introduction to",
            "Fundamentals of",
            "Advanced",
            "Practical Applications of",
            "Theory and Practice of",
            "Deep Dive into",
            "Exploring",
            "Mastering"
        ]
    
    def detect_course_type(self, keywords):
        """Detect if course is technical, theoretical, or practical"""
        technical_count = sum(1 for kw in keywords if any(tech in kw.lower() for tech in DOMAIN_INDICATORS['technical']))
        theoretical_count = sum(1 for kw in keywords if any(theory in kw.lower() for theory in DOMAIN_INDICATORS['theoretical']))
        practical_count = sum(1 for kw in keywords if any(prac in kw.lower() for prac in DOMAIN_INDICATORS['practical']))
        
        scores = {
            'technical': technical_count,
            'theoretical': theoretical_count,
            'practical': practical_count
        }
        
        return max(scores, key=scores.get)
    
    def enhance_module_titles(self, modules, course_type):
        """Improve module titles based on course type"""
        enhanced_modules = []
        
        for idx, module in enumerate(modules):
            # First module is usually introduction
            if idx == 0:
                prefix = "Introduction to"
            # Last module is usually advanced/project
            elif idx == len(modules) - 1:
                prefix = "Advanced Topics in" if course_type == 'theoretical' else "Capstone Project:"
            # Middle modules
            else:
                if course_type == 'technical':
                    prefix = random.choice(["Practical", "Applied", "Implementing"])
                elif course_type == 'theoretical':
                    prefix = random.choice(["Theory of", "Principles of", "Understanding"])
                else:
                    prefix = random.choice(["Working with", "Hands-on", "Exploring"])
            
            # Clean title
            original_title = module['title']
            # Remove existing prefix if present
            for p in self.module_prefixes:
                if original_title.startswith(p):
                    original_title = original_title[len(p):].strip()
            
            module['title'] = f"{prefix} {original_title}"
            enhanced_modules.append(module)
        
        return enhanced_modules
    
    def add_module_descriptions(self, modules):
        """Generate brief descriptions for modules"""
        descriptions = []
        
        for module in modules:
            subtopics_str = ", ".join(module['subtopics'][:3])
            description = f"This module covers {subtopics_str}, "
            description += f"providing a comprehensive understanding of {module['subtopics'][0]}."
            module['description'] = description
            descriptions.append(description)
        
        return modules
    
    def sequence_modules(self, modules):
        """Ensure logical sequencing (intro -> intermediate -> advanced)"""
        # Simple heuristic: keep first as intro, last as advanced
        if len(modules) < 3:
            return modules
        
        # Ensure first is introductory
        if not any(word in modules[0]['title'].lower() for word in ['introduction', 'fundamentals', 'basics']):
            modules[0]['title'] = f"Introduction to {modules[0]['title']}"
        
        # Ensure last is advanced/capstone
        if not any(word in modules[-1]['title'].lower() for word in ['advanced', 'capstone', 'project', 'integration']):
            modules[-1]['title'] = f"Advanced {modules[-1]['title']}"
        
        return modules
    
    def structure_complete_outline(self, modules, keywords):
        """Create complete structured outline"""
        course_type = self.detect_course_type(keywords)
        
        # Enhance modules
        enhanced = self.enhance_module_titles(modules, course_type)
        enhanced = self.add_module_descriptions(enhanced)
        enhanced = self.sequence_modules(enhanced)
        
        return {
            'modules': enhanced,
            'course_type': course_type,
            'total_modules': len(enhanced),
            'total_hours': sum(m['hours'] for m in enhanced)
        }


# Test module structurer
if __name__ == "__main__":
    import json
    from topic_extractor import TopicExtractor
    
    # Load sample course
    with open('synthetic_courses.json', 'r') as f:
        courses = json.load(f)
    
    sample_course = courses[0]
    
    # Extract topics
    extractor = TopicExtractor()
    extraction_result = extractor.extract_topics_and_modules(
        sample_course['title'],
        sample_course['description'],
        sample_course['scope'],
        sample_course['duration']
    )
    
    # Structure modules
    structurer = ModuleStructurer()
    structured = structurer.structure_complete_outline(
        extraction_result['modules'],
        extraction_result['extracted_keywords']
    )
    
    print("=" * 70)
    print(f"STRUCTURED COURSE OUTLINE: {sample_course['title']}")
    print("=" * 70)
    print(f"Course Type: {structured['course_type'].upper()}")
    print(f"Total Modules: {structured['total_modules']}")
    print(f"Total Hours: {structured['total_hours']}")
    print("\nMODULE OUTLINE:")
    print("=" * 70)
    
    for module in structured['modules']:
        print(f"\nModule {module['id']}: {module['title']}")
        print(f"Duration: {module['hours']} hours")
        print(f"Description: {module['description']}")
        print(f"Subtopics:")
        for subtopic in module['subtopics']:
            print(f"  • {subtopic.title()}")
    
    print("\n" + "=" * 70)