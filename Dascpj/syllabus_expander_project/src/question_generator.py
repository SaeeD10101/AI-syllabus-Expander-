# question_generator.py

import random
from knowledge_base import BLOOM_TAXONOMY

class QuestionGenerator:
    """Generate sample assessment questions across Bloom's taxonomy levels"""
    
    def __init__(self):
        self.bloom_levels = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
        
        # Distractor generation helpers
        self.distractor_patterns = [
            "Similar but incorrect concept",
            "Partially correct answer",
            "Common misconception",
            "Opposite or inverse concept"
        ]
    
    def clean_concept(self, concept):
        """Clean concept for question generation"""
        import re
        concept = concept.strip().lower()
        concept = re.sub(r'\b(the|a|an)\b', '', concept).strip()
        return concept
    
    def generate_mcq(self, module, bloom_level):
        """Generate a multiple-choice question"""
        
        # Get question template
        templates = BLOOM_TAXONOMY[bloom_level]['question_templates']
        template = random.choice(templates)
        
        # Extract concept from module
        concept = self.clean_concept(module['title'])
        subtopics = module.get('subtopics', [])
        
        # Select context
        if subtopics and len(subtopics) > 1:
            concept1 = self.clean_concept(subtopics[0])
            concept2 = self.clean_concept(subtopics[1]) if len(subtopics) > 1 else concept1
        else:
            concept1 = concept
            concept2 = concept
        
        # Generate question text
        try:
            if '{concept1}' in template and '{concept2}' in template:
                question_text = template.format(concept1=concept1, concept2=concept2)
            elif '{concept}' in template:
                question_text = template.format(concept=concept)
            elif '{problem}' in template:
                question_text = template.format(concept=concept, problem=f"a problem involving {concept}")
            elif '{context}' in template:
                question_text = template.format(concept=concept, context=f"practical {concept} scenarios")
            elif '{goal}' in template:
                question_text = template.format(concept=concept, goal=f"optimal {concept}")
            elif '{target}' in template:
                question_text = template.format(concept=concept, target=f"the {concept} value")
            elif '{alternative}' in template:
                question_text = template.format(concept=concept, alternative=f"alternative {concept} methods")
            else:
                question_text = template.format(concept=concept)
        except:
            question_text = f"What is the primary purpose of {concept1}?"
        
        # Capitalize first letter
        question_text = question_text[0].upper() + question_text[1:]
        
        # Generate options
        options = self.generate_mcq_options(concept1, bloom_level)
        
        # Select correct answer
        correct_answer = random.choice(['A', 'B', 'C', 'D'])
        
        return {
            'type': 'MCQ',
            'bloomLevel': bloom_level,
            'difficulty': self.get_difficulty(bloom_level),
            'question': question_text,
            'options': options,
            'correctAnswer': correct_answer,
            'explanation': f"Option {correct_answer} is correct because it accurately describes {concept1}.",
            'estimatedTime': self.estimate_time('MCQ', bloom_level),
            'tags': [concept1, bloom_level.lower()]
        }
    
    def generate_mcq_options(self, concept, bloom_level):
        """Generate 4 MCQ options"""
        
        options = [
            f"A) {concept.title()} serves as the primary mechanism for data processing",
            f"B) It provides a framework for implementing {concept}",
            f"C) {concept.title()} enables systematic analysis and evaluation",
            f"D) It represents an alternative approach to {concept}"
        ]
        
        return options
    
    def generate_short_answer(self, module, bloom_level):
        """Generate short answer question"""
        
        templates = BLOOM_TAXONOMY[bloom_level]['question_templates']
        template = random.choice(templates)
        
        concept = self.clean_concept(module['title'])
        subtopics = module.get('subtopics', [])
        
        if subtopics and len(subtopics) > 1:
            concept1 = self.clean_concept(subtopics[0])
            concept2 = self.clean_concept(subtopics[1])
        else:
            concept1 = concept
            concept2 = concept
        
        # Generate question
        try:
            if '{concept1}' in template and '{concept2}' in template:
                question_text = template.format(concept1=concept1, concept2=concept2)
            elif '{concept}' in template:
                question_text = template.format(concept=concept)
            elif '{problem}' in template:
                question_text = template.format(concept=concept, problem=f"real-world {concept} challenges")
            elif '{context}' in template:
                question_text = template.format(concept=concept, context=f"industry applications")
            else:
                question_text = template.format(concept=concept)
        except:
            question_text = f"Explain how {concept1} works in practice."
        
        question_text = question_text[0].upper() + question_text[1:]
        
        # Generate rubric
        rubric = self.generate_rubric(bloom_level)
        
        return {
            'type': 'Short Answer',
            'bloomLevel': bloom_level,
            'difficulty': self.get_difficulty(bloom_level),
            'question': question_text,
            'rubric': rubric,
            'sampleAnswer': f"A comprehensive answer should address the key principles of {concept1}, "
                          f"demonstrate understanding of its applications, and provide relevant examples.",
            'estimatedTime': self.estimate_time('Short Answer', bloom_level),
            'tags': [concept1, bloom_level.lower(), 'written-response']
        }
    
    def generate_case_study(self, module, bloom_level):
        """Generate case study question"""
        
        concept = self.clean_concept(module['title'])
        subtopics = module.get('subtopics', [])
        
        # Generate scenario
        scenario = f"A company is implementing {concept} to improve their operations. "
        scenario += f"They face challenges with {subtopics[0] if subtopics else 'system integration'}. "
        scenario += f"Current metrics show suboptimal performance in key areas."
        
        # Generate question based on Bloom level
        if bloom_level in ['Analyze', 'Evaluate']:
            question = f"Analyze the scenario and evaluate the effectiveness of their {concept} approach. "
            question += f"What improvements would you recommend?"
        elif bloom_level == 'Create':
            question = f"Design a comprehensive solution that addresses the challenges. "
            question += f"Your solution should incorporate best practices in {concept}."
        else:
            question = f"Apply {concept} principles to solve the company's challenges. "
            question += f"Provide a step-by-step implementation plan."
        
        return {
            'type': 'Case Study',
            'bloomLevel': bloom_level,
            'difficulty': 'Hard',
            'scenario': scenario,
            'question': question,
            'rubric': {
                'Analysis (30%)': 'Depth of problem analysis and identification of key issues',
                'Solution Quality (40%)': 'Effectiveness and feasibility of proposed solution',
                'Justification (20%)': 'Quality of reasoning and evidence provided',
                'Presentation (10%)': 'Clarity and organization of response'
            },
            'estimatedTime': '30-45 minutes',
            'tags': [concept, bloom_level.lower(), 'case-study', 'applied']
        }
    
    def generate_practical_lab(self, module, bloom_level):
        """Generate practical lab/project question"""
        
        concept = self.clean_concept(module['title'])
        
        question = f"Implement a solution that demonstrates {concept}. "
        question += f"Your implementation should be functional and well-documented."
        
        return {
            'type': 'Practical Lab',
            'bloomLevel': bloom_level,
            'difficulty': 'Hard',
            'question': question,
            'requirements': [
                f"Implement core {concept} functionality",
                f"Include appropriate error handling",
                f"Provide comprehensive documentation",
                f"Demonstrate testing and validation"
            ],
            'deliverables': [
                'Complete implementation code/artifact',
                'Technical documentation',
                'Test results and analysis',
                'Reflection on design decisions'
            ],
            'rubric': {
                'Functionality (40%)': 'Implementation meets requirements and works correctly',
                'Code Quality (25%)': 'Code is well-structured, readable, and maintainable',
                'Documentation (20%)': 'Clear and comprehensive documentation',
                'Testing (15%)': 'Thorough testing and validation'
            },
            'estimatedTime': '2-3 hours',
            'tags': [concept, bloom_level.lower(), 'hands-on', 'implementation']
        }
    
    def generate_rubric(self, bloom_level):
        """Generate grading rubric based on Bloom level"""
        
        if bloom_level in ['Remember', 'Understand']:
            return {
                'Excellent (9-10 pts)': 'Complete and accurate response with clear explanations',
                'Good (7-8 pts)': 'Mostly correct with minor gaps',
                'Adequate (5-6 pts)': 'Basic understanding demonstrated',
                'Poor (0-4 pts)': 'Significant gaps or misconceptions'
            }
        else:
            return {
                'Excellent (9-10 pts)': 'Sophisticated analysis with strong justification',
                'Good (7-8 pts)': 'Solid understanding with reasonable justification',
                'Adequate (5-6 pts)': 'Basic application with limited depth',
                'Poor (0-4 pts)': 'Superficial or incorrect application'
            }
    
    def get_difficulty(self, bloom_level):
        """Map Bloom level to difficulty"""
        difficulty_map = {
            'Remember': 'Easy',
            'Understand': 'Easy',
            'Apply': 'Medium',
            'Analyze': 'Medium',
            'Evaluate': 'Hard',
            'Create': 'Hard'
        }
        return difficulty_map.get(bloom_level, 'Medium')
    
    def estimate_time(self, question_type, bloom_level):
        """Estimate time to complete question"""
        
        base_times = {
            'MCQ': 2,
            'Short Answer': 10,
            'Case Study': 30,
            'Practical Lab': 120
        }
        
        bloom_multipliers = {
            'Remember': 1.0,
            'Understand': 1.2,
            'Apply': 1.5,
            'Analyze': 1.8,
            'Evaluate': 2.0,
            'Create': 2.5
        }
        
        base = base_times.get(question_type, 10)
        multiplier = bloom_multipliers.get(bloom_level, 1.0)
        
        time = int(base * multiplier)
        
        if question_type == 'MCQ':
            return f"{time} minutes"
        elif question_type == 'Short Answer':
            return f"{time} minutes"
        else:
            return f"{time} minutes"
    
    def generate_questions_for_module(self, module, num_questions=5):
        """Generate multiple questions for a module"""
        
        questions = []
        question_id_counter = 1
        
        # Determine distribution: 60% MCQ, 25% Short Answer, 15% Case/Lab
        num_mcq = max(1, int(num_questions * 0.6))
        num_short = max(1, int(num_questions * 0.25))
        num_case = max(1, num_questions - num_mcq - num_short)
        
        # Generate MCQs (lower Bloom levels)
        for _ in range(num_mcq):
            bloom_level = random.choice(['Remember', 'Understand', 'Apply'])
            question = self.generate_mcq(module, bloom_level)
            question['id'] = f"Q-M{module['id']}-{question_id_counter:03d}"
            question['moduleId'] = module['id']
            questions.append(question)
            question_id_counter += 1
        
        # Generate Short Answer (middle Bloom levels)
        for _ in range(num_short):
            bloom_level = random.choice(['Apply', 'Analyze'])
            question = self.generate_short_answer(module, bloom_level)
            question['id'] = f"Q-M{module['id']}-{question_id_counter:03d}"
            question['moduleId'] = module['id']
            questions.append(question)
            question_id_counter += 1
        
        # Generate Case Studies or Labs (higher Bloom levels)
        for i in range(num_case):
            bloom_level = random.choice(['Analyze', 'Evaluate', 'Create'])
            if i % 2 == 0:
                question = self.generate_case_study(module, bloom_level)
            else:
                question = self.generate_practical_lab(module, bloom_level)
            question['id'] = f"Q-M{module['id']}-{question_id_counter:03d}"
            question['moduleId'] = module['id']
            questions.append(question)
            question_id_counter += 1
        
        return questions
    
    def generate_all_questions(self, modules, questions_per_module=5):
        """Generate questions for all modules"""
        
        all_questions = []
        
        for module in modules:
            questions = self.generate_questions_for_module(module, questions_per_module)
            all_questions.extend(questions)
        
        return all_questions


# Test question generator
if __name__ == "__main__":
    import json
    from topic_extractor import TopicExtractor
    from module_structurer import ModuleStructurer
    
    # Load sample course
    with open('synthetic_courses.json', 'r') as f:
        courses = json.load(f)
    
    sample_course = courses[0]
    
    # Generate modules
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
    
    # Generate questions
    question_gen = QuestionGenerator()
    all_questions = question_gen.generate_all_questions(structured['modules'], questions_per_module=5)
    
    # Display results
    print("=" * 90)
    print(f"GENERATED QUESTIONS: {sample_course['title']}")
    print("=" * 90)
    print(f"\nTotal Questions: {len(all_questions)}")
    
    # Group by type
    by_type = {}
    by_bloom = {}
    
    for q in all_questions:
        by_type[q['type']] = by_type.get(q['type'], 0) + 1
        by_bloom[q['bloomLevel']] = by_bloom.get(q['bloomLevel'], 0) + 1
    
    print(f"\n📊 Question Distribution:")
    print(f"   By Type:")
    for qtype, count in by_type.items():
        print(f"      {qtype}: {count}")
    
    print(f"   By Bloom Level:")
    for bloom, count in sorted(by_bloom.items()):
        print(f"      {bloom}: {count}")
    
    # Show sample questions
    print(f"\n" + "=" * 90)
    print("SAMPLE QUESTIONS:")
    print("=" * 90)
    
    for q in all_questions[:6]:  # Show first 6
        print(f"\n{q['id']} - Module {q['moduleId']}")
        print(f"Type: {q['type']} | Bloom: {q['bloomLevel']} | Difficulty: {q['difficulty']}")
        print(f"Time: {q['estimatedTime']}")
        print(f"\nQuestion: {q['question']}")
        
        if q['type'] == 'MCQ':
            for opt in q['options']:
                marker = " ✓" if opt.startswith(q['correctAnswer']) else ""
                print(f"   {opt}{marker}")
            print(f"Explanation: {q['explanation']}")
        
        elif q['type'] == 'Short Answer':
            print(f"\nRubric:")
            for criteria, desc in q['rubric'].items():
                print(f"   {criteria}: {desc}")
        
        elif q['type'] == 'Case Study':
            print(f"\nScenario: {q['scenario']}")
            print(f"\nRubric:")
            for criteria, desc in q['rubric'].items():
                print(f"   {criteria}: {desc}")
        
        print("-" * 90)