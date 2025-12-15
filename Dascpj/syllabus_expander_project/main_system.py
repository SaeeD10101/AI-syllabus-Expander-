# main_system.py - Complete Integrated System

import json
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, 'src')

from topic_extractor import TopicExtractor
from module_structurer import ModuleStructurer
from outcome_generator import LearningOutcomeGenerator
from outcome_validator import OutcomeValidator
from assessment_generator import AssessmentBlueprintGenerator
from assessment_analyzer import AssessmentAnalyzer
from question_generator import QuestionGenerator
from alignment_matrix import AlignmentMatrixGenerator
from export_utils import ExportUtilities

class SyllabusExpanderSystem:
    """Complete AI Syllabus Expander & Assessment Mapper"""
    
    def __init__(self):
        self.topic_extractor = TopicExtractor()
        self.module_structurer = ModuleStructurer()
        self.outcome_generator = LearningOutcomeGenerator()
        self.outcome_validator = OutcomeValidator()
        self.assessment_generator = AssessmentBlueprintGenerator()
        self.assessment_analyzer = AssessmentAnalyzer()
        self.question_generator = QuestionGenerator()
        self.alignment_generator = AlignmentMatrixGenerator()
        self.exporter = ExportUtilities()
    
    def process_course(self, course_title, course_description, course_scope, duration):
        """Process a complete course specification"""
        
        print(f"\n{'='*100}")
        print(f"PROCESSING: {course_title}")
        print(f"{'='*100}\n")
        
        results = {
            'metadata': {
                'courseTitle': course_title,
                'description': course_description,
                'scope': course_scope,
                'duration': duration,
                'generated_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        
        # STEP 1: Extract Topics
        print("📚 Step 1: Extracting topics...")
        extraction = self.topic_extractor.extract_topics_and_modules(
            course_title, course_description, course_scope, duration
        )
        
        structured = self.module_structurer.structure_complete_outline(
            extraction['modules'],
            extraction['extracted_keywords']
        )
        
        results['modules'] = structured['modules']
        results['courseType'] = structured['course_type']
        results['totalHours'] = structured['total_hours']
        print(f"   ✓ Generated {len(structured['modules'])} modules")
        
        # STEP 2: Generate Learning Outcomes
        print("\n🎯 Step 2: Generating learning outcomes...")
        outcomes_result = self.outcome_generator.generate_complete_outcomes(
            structured['modules'],
            course_title,
            structured['course_type']
        )
        
        results['modules'] = outcomes_result['modules']
        results['courseLearningOutcomes'] = outcomes_result['courseLearningOutcomes']
        results['bloomStatistics'] = outcomes_result['statistics']
        print(f"   ✓ Generated {len(outcomes_result['courseLearningOutcomes'])} course-level outcomes")
        
        # STEP 3: Validate Outcomes
        print("\n✅ Step 3: Validating outcomes...")
        validation = self.outcome_validator.validate_all_outcomes(
            outcomes_result['courseLearningOutcomes'],
            outcomes_result['modules']
        )
        print(f"   ✓ {validation['summary']['valid_outcomes']}/{validation['summary']['total_outcomes']} outcomes valid")
        
        # STEP 4: Generate Assessment Blueprint
        print("\n📋 Step 4: Generating assessment blueprint...")
        blueprint = self.assessment_generator.generate_blueprint(
            structured['course_type'],
            len(structured['modules']),
            duration,
            outcomes_result['courseLearningOutcomes'],
            outcomes_result['modules']
        )
        results['assessmentBlueprint'] = blueprint
        print(f"   ✓ Generated {len(blueprint['components'])} assessment components")
        
        # STEP 5: Analyze Assessment
        print("\n📊 Step 5: Analyzing assessment quality...")
        analysis = self.assessment_analyzer.generate_analysis_report(
            blueprint,
            outcomes_result['statistics'],
            outcomes_result['courseLearningOutcomes'],
            outcomes_result['modules']
        )
        results['assessmentAnalysis'] = analysis
        print(f"   ✓ Quality score: {analysis['quality_score']}/100")
        
        # STEP 6: Generate Questions
        print("\n📝 Step 6: Generating sample questions...")
        questions = self.question_generator.generate_all_questions(
            outcomes_result['modules'],
            questions_per_module=5
        )
        results['sampleQuestions'] = questions
        print(f"   ✓ Generated {len(questions)} questions")
        
        # STEP 7: Generate Alignment Matrix
        print("\n🔗 Step 7: Generating alignment matrix...")
        matrix = self.alignment_generator.generate_matrix(
            outcomes_result['modules'],
            outcomes_result['courseLearningOutcomes'],
            blueprint,
            questions
        )
        results['alignmentMatrix'] = matrix
        print(f"   ✓ Generated {len(matrix)} alignment entries")
        
        print(f"\n{'='*100}")
        print("✅ COURSE PROCESSING COMPLETE")
        print(f"{'='*100}\n")
        
        return results

def main():
    """Main function"""
    
    print("\n" + "="*100)
    print(" "*30 + "AI SYLLABUS EXPANDER & ASSESSMENT MAPPER")
    print(" "*40 + "Pure NLP Implementation")
    print("="*100 + "\n")
    
    # Initialize system
    system = SyllabusExpanderSystem()
    
    # Load sample courses
    try:
        with open('data/synthetic_courses.json', 'r') as f:
            courses = json.load(f)
    except FileNotFoundError:
        print("❌ Error: data/synthetic_courses.json not found.")
        print("Please run: python src/dataset_generator.py")
        sys.exit(1)
    
    # Process first 2 courses
    num_to_process = min(2, len(courses))
    print(f"Processing {num_to_process} sample courses...\n")
    
    for i, course in enumerate(courses[:num_to_process]):
        print(f"\n{'#'*100}")
        print(f"COURSE {i+1}/{num_to_process}")
        print(f"{'#'*100}")
        
        # Process course
        results = system.process_course(
            course['title'],
            course['description'],
            course['scope'],
            course['duration']
        )
        
        # Export results
        base_filename = f"output/course_{i+1}"
        system.exporter.export_to_json(results, f"{base_filename}.json")
        system.exporter.export_to_csv(results, f"{base_filename}_alignment.csv")
        
        report = system.exporter.generate_text_report(results)
        with open(f"{base_filename}_report.txt", 'w') as f:
            f.write(report)
        
        print(f"\n✅ COMPLETED: {course['title']}\n")
    
    print(f"\n{'='*100}")
    print("✅ ALL PROCESSING COMPLETE!")
    print("="*100)
    print("\nGenerated Files in output/ folder:")
    print("   • course_X.json")
    print("   • course_X_alignment.csv")
    print("   • course_X_report.txt")
    print("\n" + "="*100 + "\n")

if __name__ == "__main__":
    main()