# assessment_generator.py

import random
from .knowledge_base import ASSESSMENT_TYPES, BLOOM_TAXONOMY

class AssessmentGenerator:
    """Generate assessment blueprint with weights and LO mappings"""
    
    def __init__(self):
        self.assessment_types = ASSESSMENT_TYPES
        
        # Assessment recommendations by course type
        self.course_type_weights = {
            'technical': {
                'Pre-Test': (0, 10),
                'Quizzes': (15, 25),
                'Midterm Exam': (15, 20),
                'Labs/Assignments': (30, 40),
                'Project': (15, 25),
                'Final Exam': (10, 20)
            },
            'theoretical': {
                'Pre-Test': (5, 10),
                'Quizzes': (20, 30),
                'Midterm Exam': (20, 30),
                'Labs/Assignments': (10, 20),
                'Project': (10, 15),
                'Final Exam': (20, 30)
            },
            'practical': {
                'Pre-Test': (0, 5),
                'Quizzes': (10, 20),
                'Midterm Exam': (10, 15),
                'Labs/Assignments': (35, 45),
                'Project': (20, 30),
                'Final Exam': (10, 15)
            }
        }
    
    def select_assessment_types(self, course_type, num_modules):
        """Select appropriate assessment types based on course characteristics"""
        
        selected = []
        
        # Always include quizzes and final exam
        base_assessments = ['Quizzes', 'Final Exam']
        
        # Add based on course type
        if course_type == 'technical':
            selected = ['Pre-Test', 'Quizzes', 'Labs/Assignments', 'Project', 'Final Exam']
            if num_modules >= 6:
                selected.insert(3, 'Midterm Exam')
        
        elif course_type == 'theoretical':
            selected = ['Pre-Test', 'Quizzes', 'Midterm Exam', 'Labs/Assignments', 'Final Exam']
            if num_modules >= 6:
                selected.append('Project')
        
        elif course_type == 'practical':
            selected = ['Quizzes', 'Labs/Assignments', 'Project', 'Final Exam']
            if num_modules >= 7:
                selected.insert(2, 'Midterm Exam')
        
        return selected
    
    def allocate_weights(self, selected_types, course_type):
        """Allocate weights to selected assessment types (must sum to 100)"""
        
        weights = {}
        weight_ranges = self.course_type_weights[course_type]
        
        # First pass: assign random weights within ranges
        total = 0
        for assessment_type in selected_types:
            min_weight, max_weight = weight_ranges[assessment_type]
            weight = random.randint(min_weight, max_weight)
            weights[assessment_type] = weight
            total += weight
        
        # Second pass: normalize to exactly 100
        if total != 100:
            adjustment_factor = 100 / total
            for assessment_type in weights:
                weights[assessment_type] = round(weights[assessment_type] * adjustment_factor)
        
        # Final adjustment to ensure exact 100
        current_total = sum(weights.values())
        if current_total != 100:
            diff = 100 - current_total
            # Add/subtract from largest component
            largest = max(weights, key=weights.get)
            weights[largest] += diff
        
        return weights
    
    def map_assessments_to_blooms(self, assessment_type):
        """Map assessment type to suitable Bloom levels"""
        
        if assessment_type in self.assessment_types:
            return self.assessment_types[assessment_type]['suitable_bloom']
        
        # Default mapping
        return ['Understand', 'Apply']
    
    def map_assessments_to_outcomes(self, assessment_type, bloom_levels, 
                                     course_outcomes, modules):
        """Map assessment to specific learning outcomes"""
        
        suitable_blooms = self.map_assessments_to_blooms(assessment_type)
        linked_outcomes = []
        
        # Map to course-level outcomes
        for outcome in course_outcomes:
            if outcome['bloomLevel'] in suitable_blooms:
                linked_outcomes.append(outcome['id'])
        
        # Map to module-level outcomes
        module_outcomes = []
        for module in modules:
            if 'learningOutcomes' in module:
                for outcome in module['learningOutcomes']:
                    if outcome['bloomLevel'] in suitable_blooms:
                        module_outcomes.append(f"M{module['id']}-LO{len(module_outcomes)+1}")
        
        return {
            'course_outcomes': linked_outcomes[:4],  # Limit to top 4
            'module_outcomes': module_outcomes[:6]    # Limit to top 6
        }
    
    def determine_timing(self, assessment_type, num_modules, duration):
        """Determine when assessment should occur"""
        
        timings = {
            'Pre-Test': 'Week 1',
            'Quizzes': 'Weekly (Weeks 2-{end})',
            'Midterm Exam': f'Week {num_modules // 2 + 1}',
            'Labs/Assignments': 'Weekly (Weeks 2-{end})',
            'Project': f'Weeks {num_modules - 2}-{num_modules + 1}',
            'Final Exam': 'Final Week'
        }
        
        # Parse duration
        import re
        duration_match = re.search(r'(\d+)', str(duration))
        if duration_match:
            weeks = int(duration_match.group(1))
            timing = timings.get(assessment_type, 'Throughout course')
            timing = timing.replace('{end}', str(weeks))
            return timing
        
        return timings.get(assessment_type, 'Throughout course')
    
    def generate_assessment_description(self, assessment_type, course_type):
        """Generate detailed description for assessment"""
        
        base_desc = self.assessment_types[assessment_type]['description']
        
        # Add course-type specific details
        if assessment_type == 'Labs/Assignments':
            if course_type == 'technical':
                return f"{base_desc}. Focus on coding exercises and algorithm implementation."
            elif course_type == 'practical':
                return f"{base_desc}. Emphasis on real-world applications and case studies."
            else:
                return f"{base_desc}. Problem sets and analytical exercises."
        
        elif assessment_type == 'Project':
            if course_type == 'technical':
                return f"{base_desc}. Build a complete application demonstrating course concepts."
            elif course_type == 'practical':
                return f"{base_desc}. Apply course knowledge to solve a real-world problem."
            else:
                return f"{base_desc}. Research-based project with written report."
        
        return base_desc
    
    def generate_blueprint(self, course_type, num_modules, duration, 
                          course_outcomes, modules):
        """Generate complete assessment blueprint"""
        
        # Select assessment types
        selected_types = self.select_assessment_types(course_type, num_modules)
        
        # Allocate weights
        weights = self.allocate_weights(selected_types, course_type)
        
        # Build blueprint components
        components = []
        
        for assessment_type in selected_types:
            # Get Bloom levels
            bloom_levels = self.map_assessments_to_blooms(assessment_type)
            
            # Map to outcomes
            outcome_mapping = self.map_assessments_to_outcomes(
                assessment_type,
                bloom_levels,
                course_outcomes,
                modules
            )
            
            # Get timing
            timing = self.determine_timing(assessment_type, num_modules, duration)
            
            # Get format
            format_type = self.assessment_types[assessment_type]['format']
            
            # Generate description
            description = self.generate_assessment_description(assessment_type, course_type)
            
            component = {
                'type': assessment_type,
                'weight': weights[assessment_type],
                'description': description,
                'timing': timing,
                'format': format_type,
                'linkedLOs': outcome_mapping['course_outcomes'],
                'linkedModuleLOs': outcome_mapping['module_outcomes'],
                'bloomLevels': bloom_levels
            }
            
            components.append(component)
        
        # Sort by weight (descending)
        components.sort(key=lambda x: x['weight'], reverse=True)
        
        # Generate grading scale suggestion
        grading_scale = self.suggest_grading_scale(components)
        
        return {
            'totalWeight': 100,
            'components': components,
            'gradingScale': grading_scale,
            'recommendations': self.generate_recommendations(components, course_type)
        }
    
    def suggest_grading_scale(self, components):
        """Suggest grading scale based on assessment mix"""
        
        return {
            'A': '90-100%',
            'B': '80-89%',
            'C': '70-79%',
            'D': '60-69%',
            'F': 'Below 60%'
        }
    
    def generate_recommendations(self, components, course_type):
        """Generate recommendations for instructors"""
        
        recommendations = []
        
        # Check for heavy exam weighting
        exam_weight = sum(c['weight'] for c in components if 'Exam' in c['type'])
        if exam_weight > 50:
            recommendations.append("Consider reducing exam weight to allow more formative assessment opportunities.")
        
        # Check for adequate continuous assessment
        continuous = sum(c['weight'] for c in components if c['type'] in ['Quizzes', 'Labs/Assignments'])
        if continuous < 30:
            recommendations.append("Consider adding more continuous assessment to track student progress.")
        
        # Course-type specific recommendations
        if course_type == 'technical':
            labs_weight = sum(c['weight'] for c in components if 'Labs' in c['type'])
            if labs_weight < 25:
                recommendations.append("For technical courses, consider increasing hands-on lab/assignment weight.")
        
        elif course_type == 'practical':
            project_weight = sum(c['weight'] for c in components if 'Project' in c['type'])
            if project_weight < 15:
                recommendations.append("For practical courses, consider adding a capstone project component.")
        
        if not recommendations:
            recommendations.append("Assessment blueprint is well-balanced for this course type.")
        
        return recommendations


# Test the assessment generator
if __name__ == "__main__":
    import json
    from topic_extractor import TopicExtractor
    from module_structurer import ModuleStructurer
    from outcome_generator import LearningOutcomeGenerator
    
    # Load sample course
    with open('synthetic_courses.json', 'r') as f:
        courses = json.load(f)
    
    sample_course = courses[0]
    
    # Generate structure and outcomes
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
    
    outcome_gen = LearningOutcomeGenerator()
    outcomes_result = outcome_gen.generate_complete_outcomes(
        structured['modules'],
        sample_course['title'],
        structured['course_type']
    )
    
    # Generate assessment blueprint
    assessment_gen = AssessmentBlueprintGenerator()
    blueprint = assessment_gen.generate_blueprint(
        structured['course_type'],
        len(structured['modules']),
        sample_course['duration'],
        outcomes_result['courseLearningOutcomes'],
        outcomes_result['modules']
    )
    
    # Display results
    print("=" * 90)
    print(f"ASSESSMENT BLUEPRINT: {sample_course['title']}")
    print("=" * 90)
    print(f"Course Type: {structured['course_type'].upper()}")
    print(f"Duration: {sample_course['duration']}")
    print(f"Number of Modules: {len(structured['modules'])}")
    
    print(f"\n📊 ASSESSMENT COMPONENTS:")
    print("=" * 90)
    
    for component in blueprint['components']:
        print(f"\n{component['type']} - {component['weight']}%")
        print(f"   📝 Description: {component['description']}")
        print(f"   ⏰ Timing: {component['timing']}")
        print(f"   📋 Format: {component['format']}")
        print(f"   🎯 Bloom Levels: {', '.join(component['bloomLevels'])}")
        print(f"   🔗 Linked Course LOs: {', '.join(component['linkedLOs'][:3])}")
        if component['linkedModuleLOs']:
            print(f"   🔗 Linked Module LOs: {', '.join(component['linkedModuleLOs'][:3])}")
    
    print(f"\n" + "=" * 90)
    print("📊 WEIGHT DISTRIBUTION:")
    print("=" * 90)
    
    # Visual representation
    for component in blueprint['components']:
        bars = "█" * (component['weight'] // 2)
        print(f"{component['type']:20s} {component['weight']:3d}% {bars}")
    
    print(f"\nTotal: {blueprint['totalWeight']}%")
    
    print(f"\n" + "=" * 90)
    print("📝 GRADING SCALE:")
    print("=" * 90)
    for grade, range_val in blueprint['gradingScale'].items():
        print(f"   {grade}: {range_val}")
    
    print(f"\n" + "=" * 90)
    print("💡 RECOMMENDATIONS:")
    print("=" * 90)
    for rec in blueprint['recommendations']:
        print(f"   • {rec}")
    

    print("\n" + "=" * 90)

