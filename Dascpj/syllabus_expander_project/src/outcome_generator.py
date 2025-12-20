# src/outcome_generator.py - FIXED VERSION

import random
from .knowledge_base import BLOOM_TAXONOMY
import re

class LearningOutcomeGenerator:
    """Generate Bloom's Taxonomy-aligned learning outcomes"""
    
    def __init__(self):
        self.bloom_levels = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
        
        # Recommended distribution based on course type
        self.bloom_distributions = {
            'technical': {
                'Remember': 0.10,
                'Understand': 0.15,
                'Apply': 0.35,
                'Analyze': 0.25,
                'Evaluate': 0.10,
                'Create': 0.05
            },
            'theoretical': {
                'Remember': 0.15,
                'Understand': 0.30,
                'Apply': 0.20,
                'Analyze': 0.25,
                'Evaluate': 0.10,
                'Create': 0.00
            },
            'practical': {
                'Remember': 0.05,
                'Understand': 0.10,
                'Apply': 0.40,
                'Analyze': 0.25,
                'Evaluate': 0.10,
                'Create': 0.10
            }
        }
    
    def clean_concept(self, concept):
        """Clean and normalize concept text"""
        # Remove extra spaces, lowercase
        concept = concept.strip().lower()
        
        # Remove articles
        concept = re.sub(r'\b(the|a|an)\b', '', concept).strip()
        
        return concept
    
    def select_bloom_level(self, module_position, total_modules, course_type):
        """Select appropriate Bloom level based on module position"""
        # Early modules: lower Bloom levels
        # Later modules: higher Bloom levels
        
        position_ratio = module_position / total_modules
        
        if position_ratio < 0.33:  # First third - foundational
            weights = [0.4, 0.4, 0.15, 0.05, 0, 0]  # Focus on Remember, Understand
        elif position_ratio < 0.67:  # Middle third - application
            weights = [0.1, 0.2, 0.4, 0.25, 0.05, 0]  # Focus on Apply, Analyze
        else:  # Last third - synthesis
            weights = [0, 0.1, 0.2, 0.3, 0.25, 0.15]  # Focus on Analyze, Evaluate, Create
        
        # Adjust based on course type
        if course_type == 'practical':
            weights[2] += 0.1  # Boost Apply
            weights[5] += 0.05  # Boost Create
        elif course_type == 'theoretical':
            weights[1] += 0.1  # Boost Understand
            weights[3] += 0.05  # Boost Analyze
        
        # Normalize weights
        total_weight = sum(weights)
        if total_weight > 0:
            weights = [w/total_weight for w in weights]
        
        return random.choices(self.bloom_levels, weights=weights)[0]
    
    def generate_module_outcome(self, module_title, subtopics, bloom_level):
        """Generate a single learning outcome for a module"""
        
        # Get template from knowledge base
        templates = BLOOM_TAXONOMY[bloom_level]['outcome_templates']
        template = random.choice(templates)
        
        # Extract main concept from module title
        concept = module_title.lower()
        
        # Remove common prefixes
        prefixes = ['introduction to', 'fundamentals of', 'advanced', 'practical', 
                   'theory of', 'principles of', 'understanding', 'working with',
                   'hands-on', 'exploring', 'implementing', 'applied', 'deep dive into',
                   'mastering', 'capstone project:']
        
        for prefix in prefixes:
            if concept.startswith(prefix):
                concept = concept[len(prefix):].strip()
        
        # Use first subtopic as additional context if available
        context = subtopics[0] if subtopics else concept
        context = self.clean_concept(context)
        
        # Clean concept
        concept = self.clean_concept(concept)
        
        # Generate outcome - FIXED: Handle all template placeholders
        try:
            # Check what placeholders the template has
            if '{context}' in template:
                outcome = template.format(concept=concept, context=context)
            else:
                outcome = template.format(concept=concept)
        except KeyError as e:
            # Fallback: create simple outcome
            verb = BLOOM_TAXONOMY[bloom_level]['verbs'][0]
            outcome = f"Students will be able to {verb} {concept}"
        
        # Capitalize first letter
        outcome = outcome[0].upper() + outcome[1:]
        
        return {
            'outcome': outcome,
            'bloomLevel': bloom_level,
            'bloomTier': 'Cognitive',
            'module_context': concept
        }
    
    def generate_module_outcomes(self, module, module_position, total_modules, course_type):
        """Generate 1-3 learning outcomes per module"""
        
        # Determine number of outcomes (1-3)
        num_outcomes = random.randint(1, 3)
        
        outcomes = []
        used_bloom_levels = set()
        
        for i in range(num_outcomes):
            # Select Bloom level (avoid duplicates when possible)
            attempts = 0
            while attempts < 10:
                bloom_level = self.select_bloom_level(module_position, total_modules, course_type)
                if bloom_level not in used_bloom_levels or attempts > 5:
                    break
                attempts += 1
            
            used_bloom_levels.add(bloom_level)
            
            # Generate outcome
            outcome = self.generate_module_outcome(
                module['title'],
                module['subtopics'],
                bloom_level
            )
            
            outcomes.append(outcome)
        
        return outcomes
    
    def generate_course_level_outcomes(self, modules, course_title, course_type):
        """Generate 3-6 course-level learning outcomes"""
        
        num_outcomes = random.randint(3, 6)
        outcomes = []
        
        # Get Bloom distribution for course type
        distribution = self.bloom_distributions[course_type]
        
        # Calculate how many outcomes per Bloom level
        bloom_counts = {}
        for bloom_level, ratio in distribution.items():
            count = max(0, round(ratio * num_outcomes))
            if count > 0:
                bloom_counts[bloom_level] = count
        
        # Adjust to match exact count
        current_total = sum(bloom_counts.values())
        if current_total < num_outcomes:
            # Add to most common level
            highest = max(distribution, key=distribution.get)
            bloom_counts[highest] = bloom_counts.get(highest, 0) + (num_outcomes - current_total)
        elif current_total > num_outcomes:
            # Remove from least common level
            lowest = min(bloom_counts, key=bloom_counts.get)
            bloom_counts[lowest] = max(0, bloom_counts[lowest] - (current_total - num_outcomes))
        
        # Generate outcomes for each Bloom level
        for bloom_level, count in bloom_counts.items():
            for i in range(count):
                # Use course concepts
                concept = course_title.lower()
                
                # Remove "introduction to" etc.
                prefixes = ['introduction to', 'fundamentals of', 'advanced', 'basics of']
                for prefix in prefixes:
                    if concept.startswith(prefix):
                        concept = concept[len(prefix):].strip()
                
                concept = self.clean_concept(concept)
                
                # Get random template
                templates = BLOOM_TAXONOMY[bloom_level]['outcome_templates']
                template = random.choice(templates)
                
                # Generate outcome text - FIXED: Handle all placeholders
                try:
                    if '{context}' in template:
                        outcome_text = template.format(concept=concept, context=f"practical {concept} scenarios")
                    else:
                        outcome_text = template.format(concept=concept)
                except KeyError:
                    # Fallback
                    verb = BLOOM_TAXONOMY[bloom_level]['verbs'][0]
                    outcome_text = f"Students will be able to {verb} {concept}"
                
                outcome_text = outcome_text[0].upper() + outcome_text[1:]
                
                outcomes.append({
                    'id': f"CLO-{len(outcomes)+1}",
                    'outcome': outcome_text,
                    'bloomLevel': bloom_level,
                    'bloomTier': 'Cognitive',
                    'mappedModules': []  # Will be populated later
                })
        
        return outcomes
    
    def map_course_outcomes_to_modules(self, course_outcomes, modules):
        """Map course-level outcomes to relevant modules"""
        
        for outcome in course_outcomes:
            bloom_level = outcome['bloomLevel']
            
            # Find modules with matching or compatible Bloom levels
            for module in modules:
                if 'learningOutcomes' in module:
                    for module_outcome in module['learningOutcomes']:
                        if module_outcome['bloomLevel'] == bloom_level:
                            if module['id'] not in outcome['mappedModules']:
                                outcome['mappedModules'].append(module['id'])
        
        # Ensure each outcome maps to at least 1-2 modules
        for outcome in course_outcomes:
            if len(outcome['mappedModules']) == 0:
                # Map to random modules
                num_mappings = random.randint(1, min(2, len(modules)))
                outcome['mappedModules'] = random.sample(
                    [m['id'] for m in modules],
                    num_mappings
                )
        
        return course_outcomes
    
    def generate_complete_outcomes(self, modules, course_title, course_type):
        """Generate all learning outcomes (course-level and module-level)"""
        
        # Generate module-level outcomes
        total_modules = len(modules)
        for i, module in enumerate(modules):
            outcomes = self.generate_module_outcomes(
                module,
                i + 1,
                total_modules,
                course_type
            )
            module['learningOutcomes'] = outcomes
        
        # Generate course-level outcomes
        course_outcomes = self.generate_course_level_outcomes(
            modules,
            course_title,
            course_type
        )
        
        # Map course outcomes to modules
        course_outcomes = self.map_course_outcomes_to_modules(
            course_outcomes,
            modules
        )
        
        return {
            'modules': modules,
            'courseLearningOutcomes': course_outcomes,
            'statistics': self.calculate_bloom_statistics(modules, course_outcomes)
        }
    
    def calculate_bloom_statistics(self, modules, course_outcomes):
        """Calculate Bloom taxonomy distribution statistics"""
        
        # Count module-level outcomes
        module_bloom_counts = {level: 0 for level in self.bloom_levels}
        total_module_outcomes = 0
        
        for module in modules:
            if 'learningOutcomes' in module:
                for outcome in module['learningOutcomes']:
                    module_bloom_counts[outcome['bloomLevel']] += 1
                    total_module_outcomes += 1
        
        # Count course-level outcomes
        course_bloom_counts = {level: 0 for level in self.bloom_levels}
        for outcome in course_outcomes:
            course_bloom_counts[outcome['bloomLevel']] += 1
        
        # Calculate percentages
        module_percentages = {}
        if total_module_outcomes > 0:
            for level, count in module_bloom_counts.items():
                module_percentages[level] = round((count / total_module_outcomes) * 100, 1)
        
        course_percentages = {}
        if len(course_outcomes) > 0:
            for level, count in course_bloom_counts.items():
                course_percentages[level] = round((count / len(course_outcomes)) * 100, 1)
        
        return {
            'module_level': {
                'counts': module_bloom_counts,
                'percentages': module_percentages,
                'total': total_module_outcomes
            },
            'course_level': {
                'counts': course_bloom_counts,
                'percentages': course_percentages,
                'total': len(course_outcomes)
            }
        }


# Test the outcome generator
if __name__ == "__main__":
    import json
    import sys
    sys.path.insert(0, '.')
    
    from topic_extractor import TopicExtractor
    from module_structurer import ModuleStructurer
    
    print("="*80)
    print("TESTING LEARNING OUTCOME GENERATOR")
    print("="*80)
    
    # Load sample course
    try:
        with open('data/synthetic_courses.json', 'r') as f:
            courses = json.load(f)
    except FileNotFoundError:
        print("❌ Error: data/synthetic_courses.json not found")
        print("Please run: python src/dataset_generator.py")
        sys.exit(1)
    
    sample_course = courses[0]
    
    print(f"\nProcessing: {sample_course['title']}")
    print("-"*80)
    
    # Extract topics and structure modules
    extractor = TopicExtractor()
    extraction = extractor.extract_topics_and_modules(
        sample_course['title'],
        sample_course['description'],
        sample_course['scope'],
        sample_course['duration']
    )
    
    structurer = ModuleStructurer()
    structured = structurer.structure_complete_outline(
        extraction['modules'],
        extraction['extracted_keywords']
    )
    
    # Generate learning outcomes
    outcome_gen = LearningOutcomeGenerator()
    result = outcome_gen.generate_complete_outcomes(
        structured['modules'],
        sample_course['title'],
        structured['course_type']
    )
    
    # Display results
    print("\n" + "="*80)
    print(f"LEARNING OUTCOMES: {sample_course['title']}")
    print("="*80)
    
    print("\n📊 BLOOM'S TAXONOMY DISTRIBUTION:")
    print("-"*80)
    stats = result['statistics']
    print(f"\nCourse-Level Outcomes ({stats['course_level']['total']} total):")
    for level in ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]:
        count = stats['course_level']['counts'][level]
        pct = stats['course_level']['percentages'].get(level, 0)
        print(f"  {level:12s}: {count:2d} ({pct:5.1f}%)")
    
    print(f"\nModule-Level Outcomes ({stats['module_level']['total']} total):")
    for level in ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]:
        count = stats['module_level']['counts'][level]
        pct = stats['module_level']['percentages'].get(level, 0)
        print(f"  {level:12s}: {count:2d} ({pct:5.1f}%)")
    
    print("\n" + "="*80)
    print("COURSE-LEVEL LEARNING OUTCOMES:")
    print("="*80)
    for outcome in result['courseLearningOutcomes']:
        print(f"\n{outcome['id']}: {outcome['outcome']}")
        print(f"   Bloom Level: {outcome['bloomLevel']}")
        print(f"   Mapped to Modules: {', '.join(map(str, outcome['mappedModules']))}")
    
    print("\n" + "="*80)
    print("MODULE-LEVEL LEARNING OUTCOMES:")
    print("="*80)
    for module in result['modules'][:3]:  # Show first 3
        print(f"\n📚 Module {module['id']}: {module['title']}")
        print(f"   Duration: {module['hours']} hours")
        print(f"   Learning Outcomes:")
        for outcome in module['learningOutcomes']:
            print(f"   • {outcome['outcome']} [{outcome['bloomLevel']}]")
    
    print("\n" + "="*80)
    print("✅ TEST COMPLETE")

    print("="*80)
