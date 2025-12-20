from flask import Flask, render_template, request, jsonify, send_file
import sys
import os
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import modules with error handling
try:
    from src.topic_extractor import TopicExtractor, check_model_available
    from src.module_structurer import ModuleStructurer
    from src.outcome_generator import OutcomeGenerator
    from src.outcome_validator import OutcomeValidator
    from src.assessment_generator import AssessmentGenerator
    from src.question_generator import QuestionGenerator
    from src.alignment_matrix import AlignmentMatrix
    from src.export_utils import ExportUtils
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all required modules are in the src/ directory")
    sys.exit(1)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Global components - initialize with error handling
topic_extractor = None
module_structurer = None
outcome_generator = None
outcome_validator = None
assessment_generator = None
question_generator = None
alignment_matrix = None
export_utils = None

def initialize_components():
    """Initialize all system components with error handling"""
    global topic_extractor, module_structurer, outcome_generator
    global outcome_validator, assessment_generator, question_generator
    global alignment_matrix, export_utils
    
    try:
        print("Initializing components...")
        
        # Check if spaCy model is available
        spacy_available = check_model_available()
        if not spacy_available:
            print("Warning: spaCy model not available. Using basic text processing.")
        
        # Initialize components
        topic_extractor = TopicExtractor(skip_spacy=not spacy_available)
        module_structurer = ModuleStructurer()
        outcome_generator = OutcomeGenerator()
        outcome_validator = OutcomeValidator()
        assessment_generator = AssessmentGenerator()
        question_generator = QuestionGenerator()
        alignment_matrix = AlignmentMatrix()
        export_utils = ExportUtils()
        
        print("All components initialized successfully!")
        return True
        
    except Exception as e:
        print(f"Component initialization error: {e}")
        # Create minimal fallback versions
        topic_extractor = TopicExtractor(skip_spacy=True)
        module_structurer = ModuleStructurer()
        outcome_generator = OutcomeGenerator()
        outcome_validator = OutcomeValidator()
        assessment_generator = AssessmentGenerator()
        return False

# Initialize on startup
initialize_components()


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/api/generate-syllabus', methods=['POST'])
def generate_syllabus():
    """
    Main endpoint to generate complete syllabus
    
    Expected JSON input:
    {
        "course_title": "Introduction to Machine Learning",
        "course_description": "This course covers...",
        "course_scope": "Undergraduate level...",
        "duration": "15 weeks",
        "num_modules": 4,
        "outcomes_per_topic": 2
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract parameters
        course_title = data.get('course_title', '')
        course_description = data.get('course_description', '')
        course_scope = data.get('course_scope', '')
        duration = data.get('duration', '15 weeks')
        num_modules = int(data.get('num_modules', 4))
        outcomes_per_topic = int(data.get('outcomes_per_topic', 2))
        
        # Validate input
        if not course_title or not course_description:
            return jsonify({'error': 'Course title and description are required'}), 400
        
        print(f"Processing: {course_title}")
        
        # Step 1: Extract topics
        print("Step 1: Extracting topics...")
        topics = topic_extractor.extract_topics(
            course_description=course_description,
            course_title=course_title,
            num_topics=num_modules * 2  # 2 topics per module
        )
        
        if not topics:
            return jsonify({'error': 'Failed to extract topics from description'}), 400
        
        # Step 2: Structure modules
        print("Step 2: Structuring modules...")
        module_structure = module_structurer.create_module_structure(
            topics=topics,
            course_description=course_description,
            course_title=course_title,
            num_modules=num_modules
        )
        
        # Step 3: Generate learning outcomes
        print("Step 3: Generating learning outcomes...")
        module_structure = outcome_generator.generate_outcomes_for_all_modules(
            module_structure,
            outcomes_per_topic=outcomes_per_topic
        )
        
        # Step 4: Validate outcomes
        print("Step 4: Validating outcomes...")
        validation_results = outcome_validator.validate_all_outcomes(module_structure)
        
        # Step 5: Generate assessment blueprint
        print("Step 5: Generating assessments...")
        assessments = assessment_generator.recommend_assessments(module_structure)
        assessment_alignment = assessment_generator.align_assessments_to_outcomes(
            module_structure,
            assessments
        )
        
        # Step 6: Generate sample questions
        print("Step 6: Generating sample questions...")
        questions = question_generator.generate_questions_for_all_modules(
            module_structure,
            questions_per_topic=3
        )
        
        # Step 7: Create alignment matrix
        print("Step 7: Creating alignment matrix...")
        alignment = alignment_matrix.create_alignment_matrix(
            module_structure,
            assessments,
            questions
        )
        
        # Prepare response
        response = {
            'success': True,
            'course_info': {
                'title': course_title,
                'description': course_description,
                'scope': course_scope,
                'duration': duration,
                'generated_at': datetime.now().isoformat()
            },
            'topics': topics,
            'module_structure': module_structure,
            'validation': validation_results,
            'assessments': assessments,
            'assessment_alignment': assessment_alignment,
            'questions': questions,
            'alignment_matrix': alignment
        }
        
        print("Syllabus generation completed successfully!")
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error generating syllabus: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/extract-topics', methods=['POST'])
def extract_topics():
    """Extract topics only"""
    try:
        data = request.get_json()
        course_description = data.get('course_description', '')
        course_title = data.get('course_title', '')
        num_topics = int(data.get('num_topics', 6))
        
        if not course_description:
            return jsonify({'error': 'Course description is required'}), 400
        
        topics = topic_extractor.extract_topics(
            course_description=course_description,
            course_title=course_title,
            num_topics=num_topics
        )
        
        return jsonify({
            'success': True,
            'topics': topics
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/validate-outcomes', methods=['POST'])
def validate_outcomes():
    """Validate learning outcomes"""
    try:
        data = request.get_json()
        module_structure = data.get('module_structure')
        
        if not module_structure:
            return jsonify({'error': 'Module structure is required'}), 400
        
        validation_results = outcome_validator.validate_all_outcomes(module_structure)
        
        return jsonify({
            'success': True,
            'validation': validation_results
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/word', methods=['POST'])
def export_word():
    """Export syllabus to Word document"""
    try:
        data = request.get_json()
        
        # Generate Word document
        file_path = export_utils.export_to_word(data)
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name='syllabus.docx',
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/excel', methods=['POST'])
def export_excel():
    """Export alignment matrix to Excel"""
    try:
        data = request.get_json()
        
        # Generate Excel file
        file_path = export_utils.export_to_excel(data)
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name='alignment_matrix.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/json', methods=['POST'])
def export_json():
    """Export complete syllabus data as JSON"""
    try:
        data = request.get_json()
        
        # Create JSON file
        file_path = export_utils.export_to_json(data)
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name='syllabus.json',
            mimetype='application/json'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'components': {
            'topic_extractor': topic_extractor is not None,
            'module_structurer': module_structurer is not None,
            'outcome_generator': outcome_generator is not None,
            'spacy_available': check_model_available()
        },
        'timestamp': datetime.now().isoformat()
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


# For development
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"Starting Flask app on port {port}")
    print(f"Debug mode: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
