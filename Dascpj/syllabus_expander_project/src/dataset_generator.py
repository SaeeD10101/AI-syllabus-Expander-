# src/dataset_generator.py - FIXED VERSION

import json
import random

# Sample course templates for different domains
COURSE_TEMPLATES = [
    {
        "domain": "Computer Science",
        "titles": [
            "Introduction to Data Structures",
            "Web Development Fundamentals",
            "Machine Learning Basics",
            "Database Management Systems",
            "Software Engineering Principles",
            "Computer Networks",
            "Operating Systems",
            "Cybersecurity Fundamentals"
        ],
        "keywords": [
            "algorithm", "programming", "data", "software", "system", 
            "code", "development", "design", "implementation", "testing",
            "database", "network", "security", "architecture", "optimization"
        ],
        "subtopics": [
            "arrays", "linked lists", "trees", "graphs", "sorting", 
            "searching", "recursion", "complexity analysis", "hash tables",
            "stacks", "queues", "algorithms", "data modeling"
        ]
    },
    {
        "domain": "Business",
        "titles": [
            "Introduction to Marketing",
            "Financial Accounting Basics",
            "Business Strategy and Planning",
            "Operations Management",
            "Organizational Behavior",
            "Project Management",
            "Entrepreneurship",
            "Business Analytics"
        ],
        "keywords": [
            "management", "strategy", "finance", "marketing", "operations", 
            "planning", "analysis", "decision", "performance", "leadership",
            "innovation", "customer", "value", "growth", "profit"
        ],
        "subtopics": [
            "market research", "financial statements", "strategic planning", 
            "supply chain", "team dynamics", "risk management", "budgeting",
            "competitive analysis", "stakeholder management", "business models"
        ]
    },
    {
        "domain": "Healthcare",
        "titles": [
            "Human Anatomy and Physiology",
            "Nursing Fundamentals",
            "Public Health Management",
            "Medical Terminology",
            "Healthcare Ethics",
            "Patient Care Basics",
            "Health Informatics",
            "Pharmacology Basics"
        ],
        "keywords": [
            "patient", "care", "health", "medical", "diagnosis", 
            "treatment", "disease", "prevention", "clinical", "healthcare",
            "wellness", "safety", "quality", "practice", "evidence"
        ],
        "subtopics": [
            "cardiovascular system", "respiratory system", "patient assessment", 
            "infection control", "medical records", "vital signs", "medications",
            "patient safety", "health promotion", "clinical procedures"
        ]
    },
    {
        "domain": "Engineering",
        "titles": [
            "Thermodynamics Principles",
            "Circuit Analysis",
            "Mechanical Design",
            "Control Systems",
            "Materials Science",
            "Structural Analysis",
            "Fluid Mechanics",
            "Engineering Mathematics"
        ],
        "keywords": [
            "design", "analysis", "system", "process", "engineering", 
            "principles", "application", "measurement", "testing", "optimization",
            "modeling", "simulation", "calculation", "specification", "performance"
        ],
        "subtopics": [
            "heat transfer", "electrical circuits", "mechanical systems", 
            "feedback control", "material properties", "stress analysis",
            "force dynamics", "equilibrium", "energy conservation", "efficiency"
        ]
    },
    {
        "domain": "Education",
        "titles": [
            "Educational Psychology",
            "Curriculum Design",
            "Assessment and Evaluation",
            "Classroom Management",
            "Learning Theories",
            "Instructional Technology",
            "Special Education",
            "Educational Leadership"
        ],
        "keywords": [
            "learning", "teaching", "student", "education", "assessment",
            "curriculum", "instruction", "development", "pedagogy", "evaluation",
            "engagement", "motivation", "cognition", "diversity", "achievement"
        ],
        "subtopics": [
            "cognitive development", "lesson planning", "formative assessment",
            "behavior management", "learning styles", "educational technology",
            "differentiated instruction", "student engagement", "assessment design"
        ]
    }
]

def generate_course_description(domain_data, title):
    """Generate realistic course description"""
    # Safe sample - take minimum of available and needed
    num_keywords = min(len(domain_data["keywords"]), random.randint(5, 8))
    keywords = random.sample(domain_data["keywords"], k=num_keywords)
    
    description = f"This course provides a comprehensive introduction to {title.lower()}. "
    description += f"Students will learn fundamental concepts including {', '.join(keywords[:3])}. "
    
    if len(keywords) >= 5:
        description += f"The course covers {', '.join(keywords[3:5])} with emphasis on practical {keywords[-1]}. "
    
    if len(keywords) >= 3:
        description += f"Through hands-on exercises and real-world examples, students will develop skills in {keywords[-2]} and {keywords[-3]}."
    
    return description

def generate_course_scope(domain_data, title):
    """Generate course scope"""
    # Safe sample - take minimum of available and needed
    num_subtopics = min(len(domain_data["subtopics"]), random.randint(4, 6))
    subtopics = random.sample(domain_data["subtopics"], k=num_subtopics)
    
    scope = f"Topics covered include: {', '.join(subtopics[:3])}"
    
    if len(subtopics) > 3:
        scope += f", and {subtopics[-1]}. "
    else:
        scope += ". "
    
    if domain_data["keywords"]:
        scope += f"Students should have basic knowledge of {random.choice(domain_data['keywords'])}. "
    
    scope += f"Prerequisites: None or introductory {domain_data['domain'].lower()} course."
    
    return scope

def generate_dataset(num_courses=30):
    """Generate synthetic course dataset"""
    dataset = []
    
    for i in range(num_courses):
        # Select random domain
        domain_data = random.choice(COURSE_TEMPLATES)
        
        # Select random title from domain
        title = random.choice(domain_data["titles"])
        
        # Generate course data
        course = {
            "id": f"COURSE_{i+1:03d}",
            "domain": domain_data["domain"],
            "title": title,
            "description": generate_course_description(domain_data, title),
            "scope": generate_course_scope(domain_data, title),
            "duration": random.choice(["8 weeks", "10 weeks", "12 weeks", "15 weeks"]),
            "credit_hours": random.choice([3, 4]),
            "level": random.choice(["Undergraduate", "Graduate", "Professional"])
        }
        
        dataset.append(course)
    
    return dataset

# Generate and save dataset
if __name__ == "__main__":
    print("="*60)
    print("GENERATING SYNTHETIC COURSE DATASET")
    print("="*60)
    
    # Generate courses
    courses = generate_dataset(30)
    
    # Create data directory if it doesn't exist
    import os
    os.makedirs('data', exist_ok=True)
    
    # Save to JSON file
    output_file = 'data/synthetic_courses.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(courses, indent=2, fp=f)
    
    print(f"\n✅ Generated {len(courses)} synthetic courses")
    print(f"📁 Saved to: {output_file}")
    
    # Display sample
    print(f"\n{'='*60}")
    print("SAMPLE COURSES:")
    print("="*60)
    
    for i, course in enumerate(courses[:3], 1):
        print(f"\n{i}. {course['title']}")
        print(f"   Domain: {course['domain']}")
        print(f"   Duration: {course['duration']}")
        print(f"   Level: {course['level']}")
        print(f"   Description: {course['description'][:100]}...")
    
    print(f"\n{'='*60}")
    print("✅ DATASET GENERATION COMPLETE!")
    print("="*60)