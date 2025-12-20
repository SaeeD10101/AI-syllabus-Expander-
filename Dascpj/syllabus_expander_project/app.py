# app.py - Flask Web Backend
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import json
sys.path.insert(0, 'src')
from topic_extractor import TopicExtractor
from module_structurer import ModuleStructurer
from outcome_generator import OutcomeGenerator
from assessment_generator import AssessmentBlueprintGenerator
from question_generator import QuestionGenerator
from alignment_matrix import AlignmentMatrixGenerator
from assessment_analyzer import AssessmentAnalyzer

app = Flask(__name__, static_folder='web', static_url_path='')
CORS(app)

# Initialize components
topic_extractor = TopicExtractor()
module_structurer = ModuleStructurer()
outcome_generator = LearningOutcomeGenerator()
assessment_generator = AssessmentBlueprintGenerator()
question_generator = QuestionGenerator()
alignment_generator = AlignmentMatrixGenerator()
assessment_analyzer = AssessmentAnalyzer()

@app.route('/')
def index():
    """Serve main page"""
    return send_from_directory('web', 'index.html')

@app.route('/api/process', methods=['POST'])
def process_course():
    """Process course specification and generate complete syllabus"""
    try:
        data = request.json
        
        title = data.get('title', '')
        description = data.get('description', '')
        scope = data.get('scope', '')
        duration = data.get('duration', '')
        
        if not all([title, description, scope, duration]):
            return jsonify({'error': 'All fields are required'}), 400
        
        print(f"\n Processing: {title}")
        
        # Step 1: Extract topics
        extraction = topic_extractor.extract_topics_and_modules(
            title, description, scope, duration
        )
        
        # Step 2: Structure modules
        structured = module_structurer.structure_complete_outline(
            extraction['modules'],
            extraction['extracted_keywords']
        )
        
        # Step 3: Generate outcomes
        outcomes_result = outcome_generator.generate_complete_outcomes(
            structured['modules'],
            title,
            structured['course_type']
        )
        
        # Step 4: Generate assessment blueprint
        blueprint = assessment_generator.generate_blueprint(
            structured['course_type'],
            len(structured['modules']),
            duration,
            outcomes_result['courseLearningOutcomes'],
            outcomes_result['modules']
        )
        
        # Step 5: Analyze assessment
        analysis = assessment_analyzer.generate_analysis_report(
            blueprint,
            outcomes_result['statistics'],
            outcomes_result['courseLearningOutcomes'],
            outcomes_result['modules']
        )
        
        # Step 6: Generate questions
        questions = question_generator.generate_all_questions(
            outcomes_result['modules'],
            questions_per_module=5
        )
        
        # Step 7: Generate alignment matrix
        matrix = alignment_generator.generate_matrix(
            outcomes_result['modules'],
            outcomes_result['courseLearningOutcomes'],
            blueprint,
            questions
        )
        
        # Prepare response
        response = {
            'metadata': {
                'courseTitle': title,
                'description': description,
                'duration': duration,
                'generated_date': __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            'courseType': structured['course_type'],
            'totalHours': structured['total_hours'],
            'modules': outcomes_result['modules'],
            'courseLearningOutcomes': outcomes_result['courseLearningOutcomes'],
            'assessmentBlueprint': blueprint,
            'assessmentAnalysis': analysis,
            'sampleQuestions': questions,
            'alignmentMatrix': matrix,
            'bloomStatistics': outcomes_result['statistics']
        }
        
        print(f"✅ Processing complete: {len(outcomes_result['modules'])} modules generated")
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Syllabus Expander API is running'}), 200

if __name__ == '__main__':
    print("\n" + "="*80)
    print(" "*20 + "🚀 AI Syllabus Expander - Web Server")
    print("="*80)
    print("\n✅ Server starting...")
    print("📍 URL: http://localhost:5000")
    print("📡 API: http://localhost:5000/api/health")
    print("\nPress Ctrl+C to stop\n")
    print("="*80 + "\n")
    

    app.run(debug=True, host='0.0.0.0', port=5000)



