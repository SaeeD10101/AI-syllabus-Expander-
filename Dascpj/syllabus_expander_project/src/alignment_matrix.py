# src/alignment_matrix.py

class AlignmentMatrixGenerator:
    """Generate alignment matrix linking topics, LOs, assessments, and questions"""
    
    def __init__(self):
        pass
    
    def generate_matrix(self, modules, course_outcomes, blueprint, questions):
        """Generate complete alignment matrix"""
        
        matrix = []
        
        for module in modules:
            if 'learningOutcomes' not in module:
                continue
            
            for lo_idx, outcome in enumerate(module['learningOutcomes']):
                relevant_assessments = self.find_relevant_assessments(
                    outcome['bloomLevel'],
                    blueprint
                )
                
                relevant_questions = self.find_relevant_questions(
                    module['id'],
                    outcome['bloomLevel'],
                    questions
                )
                
                row = {
                    'moduleId': module['id'],
                    'module': module['title'],
                    'learningOutcome': outcome['outcome'],
                    'learningOutcomeId': f"M{module['id']}-LO{lo_idx+1}",
                    'bloomLevel': outcome['bloomLevel'],
                    'assessmentTypes': relevant_assessments,
                    'questionIds': relevant_questions[:5],
                    'coverage': self.calculate_coverage(relevant_questions)
                }
                
                matrix.append(row)
        
        return matrix
    
    def find_relevant_assessments(self, bloom_level, blueprint):
        """Find assessments that target this Bloom level"""
        relevant = []
        for component in blueprint['components']:
            if bloom_level in component['bloomLevels']:
                relevant.append(component['type'])
        return relevant
    
    def find_relevant_questions(self, module_id, bloom_level, questions):
        """Find questions for this module and Bloom level"""
        relevant = []
        for question in questions:
            if (question.get('moduleId') == module_id and 
                question.get('bloomLevel') == bloom_level):
                relevant.append(question['id'])
        return relevant
    
    def calculate_coverage(self, question_ids):
        """Calculate coverage level"""
        num_questions = len(question_ids)
        if num_questions >= 5:
            return 'High'
        elif num_questions >= 3:
            return 'Medium'
        elif num_questions >= 1:
            return 'Low'
        else:
            return 'None'
    
    def generate_gap_analysis(self, matrix):
        """Identify gaps in alignment"""
        gaps = []
        for row in matrix:
            if row['coverage'] == 'None':
                gaps.append({
                    'module': row['module'],
                    'outcome': row['learningOutcome'],
                    'issue': 'No questions mapped to this outcome'
                })
        return gaps