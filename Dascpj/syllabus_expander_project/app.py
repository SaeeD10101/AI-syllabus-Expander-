from flask import Flask, render_template, request, jsonify, send_file
import sys
import os
import json
from datetime import datetime
import traceback

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import modules
from src.topic_extractor import TopicExtractor
from src.module_structurer import ModuleStructurer
from src.outcome_generator import OutcomeGenerator
from src.outcome_validator import OutcomeValidator
from src.assessment_generator import AssessmentGenerator

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ai-syllabus-generator-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Initialize components
print("Initializing AI Syllabus Generator components...")
topic_extractor = TopicExtractor()
module_structurer = ModuleStructurer()
outcome_generator = OutcomeGenerator()
outcome_validator = OutcomeValidator()
assessment_generator = AssessmentGenerator()
print("All components initialized successfully!")


@app.route('/')
def index():
    """Main page - return API information"""
    return jsonify({
        'status': 'running',
        'message': '🎓 AI Syllabus Generator API is live!',
        'version': '1.0.0',
        'endpoints': {
            'generate_syllabus': {
                'path': '/api/generate-syllabus',
                'method': 'POST',
                'description': 'Generate complete syllabus from course description'
            },
            'extract_topics': {
                'path': '/api/extract-topics',
                'method': 'POST',
                'description': 'Extract topics from course description'
            },
            'validate_outcomes': {
                'path': '/api/validate-outcomes',
                'method': 'POST',
                'description': 'Validate learning outcomes'
            },
            'export_text': {
                'path': '/api/export/text',
                'method': 'POST',
                'description': 'Export syllabus as plain text'
            },
            'export_json': {
                'path': '/api/export/json',
                'method': 'POST',
                'description': 'Export syllabus as JSON'
            },
            'health': {
                'path': '/api/health',
                'method': 'GET',
                'description': 'Check system health'
            }
        },
        'example_request': {
            'url': '/api/generate-syllabus',
            'method': 'POST',
            'body': {
                'course_title': 'Introduction to Machine Learning',
                'course_description': 'This course covers supervised learning, unsupervised learning, and neural networks.',
                'num_modules': 4,
                'outcomes_per_topic': 2
            }
        }
    })


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
        course_title = data.get('course_title', '').strip()
        course_description = data.get('course_description', '').strip()
        course_scope = data.get('course_scope', '').strip()
        duration = data.get('duration', '15 weeks').strip()
        num_modules = int(data.get('num_modules', 4))
        outcomes_per_topic = int(data.get('outcomes_per_topic', 2))
        
        # Validate input
        if not course_title or not course_description:
            return jsonify({
                'error': 'Course title and description are required'
            }), 400
        
        if num_modules < 2 or num_modules > 10:
            return jsonify({
                'error': 'Number of modules must be between 2 and 10'
            }), 400
        
        print(f"\n{'='*60}")
        print(f"Processing: {course_title}")
        print(f"{'='*60}")
        
        # Step 1: Extract topics
        print("Step 1/6: Extracting topics...")
        topics = topic_extractor.extract_topics(
            course_description=course_description,
            course_title=course_title,
            num_topics=num_modules * 2  # 2 topics per module
        )
        
        if not topics:
            return jsonify({
                'error': 'Failed to extract topics. Please provide a more detailed course description.'
            }), 400
        
        print(f"  ✓ Extracted {len(topics)} topics")
        
        # Step 2: Structure modules
        print("Step 2/6: Structuring modules...")
        module_structure = module_structurer.create_module_structure(
            topics=topics,
            course_description=course_description,
            course_title=course_title,
            num_modules=num_modules
        )
        print(f"  ✓ Created {module_structure['total_modules']} modules")
        
        # Step 3: Generate learning outcomes
        print("Step 3/6: Generating learning outcomes...")
        module_structure = outcome_generator.generate_outcomes_for_all_modules(
            module_structure,
            outcomes_per_topic=outcomes_per_topic
        )
        
        total_outcomes = sum(
            len(m.get('learning_outcomes', [])) 
            for m in module_structure['modules']
        )
        print(f"  ✓ Generated {total_outcomes} learning outcomes")
        
        # Step 4: Validate outcomes
        print("Step 4/6: Validating outcomes...")
        validation_results = outcome_validator.validate_all_outcomes(module_structure)
        print(f"  ✓ Validation complete: {validation_results['valid_outcomes']}/{validation_results['total_outcomes']} valid")
        
        # Step 5: Generate assessment blueprint
        print("Step 5/6: Generating assessment blueprint...")
        assessments = assessment_generator.recommend_assessments(module_structure)
        print(f"  ✓ Created assessment plan with {len(assessments['assessments'])} components")
        
        # Step 6: Align assessments to outcomes
        print("Step 6/6: Creating assessment alignment...")
        assessment_alignment = assessment_generator.align_assessments_to_outcomes(
            module_structure,
            assessments
        )
        print(f"  ✓ Alignment matrix created")
        
        print(f"\n{'='*60}")
        print("✅ Syllabus generation completed successfully!")
        print(f"{'='*60}\n")
        
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
            'assessment_alignment': assessment_alignment
        }
        
        return jsonify(response), 200
        
    except ValueError as e:
        print(f"❌ Validation error: {e}")
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400
        
    except Exception as e:
        print(f"❌ Error generating syllabus: {e}")
        traceback.print_exc()
        return jsonify({
            'error': 'An error occurred while generating the syllabus',
            'details': str(e)
        }), 500


@app.route('/api/extract-topics', methods=['POST'])
def extract_topics_endpoint():
    """Extract topics only"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        course_description = data.get('course_description', '').strip()
        course_title = data.get('course_title', '').strip()
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
            'topics': topics,
            'count': len(topics)
        }), 200
        
    except Exception as e:
        print(f"Error extracting topics: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/validate-outcomes', methods=['POST'])
def validate_outcomes_endpoint():
    """Validate learning outcomes"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        module_structure = data.get('module_structure')
        
        if not module_structure:
            return jsonify({'error': 'Module structure is required'}), 400
        
        validation_results = outcome_validator.validate_all_outcomes(module_structure)
        
        return jsonify({
            'success': True,
            'validation': validation_results
        }), 200
        
    except Exception as e:
        print(f"Error validating outcomes: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/text', methods=['POST'])
def export_text():
    """Export syllabus as plain text"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Generate text output
        course_info = data.get('course_info', {})
        module_structure = data.get('module_structure', {})
        assessments = data.get('assessments', {})
        
        text_output = f"""
{'='*70}
AI SYLLABUS GENERATOR - COURSE OUTLINE
{'='*70}

Course Title: {course_info.get('title', 'N/A')}
Duration: {course_info.get('duration', 'N/A')}
Generated: {course_info.get('generated_at', 'N/A')}

{'='*70}
COURSE DESCRIPTION
{'='*70}

{course_info.get('description', 'N/A')}

{'='*70}
MODULE STRUCTURE
{'='*70}

"""
        
        for module in module_structure.get('modules', []):
            text_output += f"\n{module.get('module_name', '')}\n"
            text_output += "-" * 70 + "\n\n"
            
            text_output += "Topics:\n"
            for topic in module.get('topics', []):
                text_output += f"  • {topic}\n"
            
            text_output += "\nLearning Outcomes:\n"
            for i, outcome in enumerate(module.get('learning_outcomes', []), 1):
                text_output += f"  {i}. [{outcome.get('bloom_level', '')}] {outcome.get('outcome', '')}\n"
            
            text_output += "\n"
        
        text_output += f"\n{'='*70}\n"
        text_output += "ASSESSMENT BLUEPRINT\n"
        text_output += f"{'='*70}\n\n"
        
        for assessment in assessments.get('assessments', []):
            text_output += f"• {assessment.get('type', '')}: {assessment.get('weight', 0)}%\n"
            text_output += f"  {assessment.get('description', '')}\n\n"
        
        return jsonify({
            'success': True,
            'content': text_output
        }), 200
        
    except Exception as e:
        print(f"Error exporting text: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/json', methods=['POST'])
def export_json():
    """Export complete syllabus data as JSON"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Return the data as formatted JSON
        return jsonify({
            'success': True,
            'data': data
        }), 200
        
    except Exception as e:
        print(f"Error exporting JSON: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test each component
        components_status = {
            'topic_extractor': topic_extractor is not None,
            'module_structurer': module_structurer is not None,
            'outcome_generator': outcome_generator is not None,
            'outcome_validator': outcome_validator is not None,
            'assessment_generator': assessment_generator is not None,
        }
        
        all_healthy = all(components_status.values())
        
        return jsonify({
            'status': 'healthy' if all_healthy else 'degraded',
            'components': components_status,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }), 200 if all_healthy else 503
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 503


@app.route('/api/status', methods=['GET'])
def status():
    """Simple status endpoint"""
    return jsonify({
        'status': 'running',
        'message': 'AI Syllabus Generator is operational',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Resource not found',
        'status': 404
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'error': 'Method not allowed',
        'status': 405
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'status': 500
    }), 500


# For local development and Render deployment
if __name__ == '__main__':
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get('PORT', 5000))
    
    # Get debug mode from environment
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"\n{'='*60}")
    print(f"🎓 AI Syllabus Generator")
    print(f"{'='*60}")
    print(f"Starting Flask app on port {port}")
    print(f"Debug mode: {debug}")
    print(f"{'='*60}\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
