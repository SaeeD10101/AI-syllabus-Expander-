# test_extraction.py

import json
from .topic_extractor import TopicExtractor
from .module_structurer import ModuleStructurer

def test_extraction_pipeline():
    """Test complete extraction and structuring pipeline"""
    
    # Load courses
    with open('synthetic_courses.json', 'r') as f:
        courses = json.load(f)
    
    extractor = TopicExtractor()
    structurer = ModuleStructurer()
    
    print("Testing Topic Extraction & Module Generation")
    print("=" * 80)
    
    for i, course in enumerate(courses[:3]):  # Test first 3 courses
        print(f"\n\n{'='*80}")
        print(f"TEST {i+1}: {course['title']}")
        print(f"Domain: {course['domain']}")
        print(f"{'='*80}")
        
        # Extract topics
        extraction = extractor.extract_topics_and_modules(
            course['title'],
            course['description'],
            course['scope'],
            course['duration']
        )
        
        # Structure modules
        structured = structurer.structure_complete_outline(
            extraction['modules'],
            extraction['extracted_keywords']
        )
        
        # Display results
        print(f"\n📊 EXTRACTION RESULTS:")
        print(f"   Keywords Found: {len(extraction['extracted_keywords'])}")
        print(f"   Top Keywords: {', '.join(extraction['extracted_keywords'][:8])}")
        print(f"   Course Type: {structured['course_type']}")
        print(f"   Modules Generated: {structured['total_modules']}")
        print(f"   Total Hours: {structured['total_hours']}")
        
        print(f"\n📚 MODULE STRUCTURE:")
        for module in structured['modules']:
            print(f"\n   Module {module['id']}: {module['title']}")
            print(f"   ⏱️  {module['hours']} hours")
            print(f"   📝 Subtopics: {', '.join(module['subtopics'][:3])}")
        
        print("\n" + "-" * 80)

if __name__ == "__main__":

    test_extraction_pipeline()
