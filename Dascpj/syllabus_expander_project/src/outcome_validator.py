# outcome_validator.py

import re
from .knowledge_base import BLOOM_TAXONOMY

class OutcomeValidator:
    """Validate learning outcomes for measurability and quality"""
    
    def __init__(self):
        # Collect all Bloom verbs
        self.bloom_verbs = {}
        for level, data in BLOOM_TAXONOMY.items():
            self.bloom_verbs[level] = [v.lower() for v in data['verbs']]
        
        # All verbs combined
        self.all_bloom_verbs = []
        for verbs in self.bloom_verbs.values():
            self.all_bloom_verbs.extend(verbs)
        
        # Non-measurable verbs to avoid
        self.vague_verbs = ['know', 'understand', 'learn', 'appreciate', 
                           'be aware of', 'become familiar with', 'gain knowledge']
    
    def validate_outcome(self, outcome_text):
        """Validate a single learning outcome"""
        issues = []
        warnings = []
        
        outcome_lower = outcome_text.lower()
        
        # Check 1: Starts with "Students will be able to"
        if not outcome_lower.startswith('students will be able to'):
            issues.append("Outcome should start with 'Students will be able to'")
        
        # Check 2: Contains a Bloom verb
        has_bloom_verb = any(verb in outcome_lower for verb in self.all_bloom_verbs)
        if not has_bloom_verb:
            issues.append("Outcome does not contain a measurable Bloom's taxonomy verb")
        
        # Check 3: Avoid vague verbs
        has_vague_verb = any(verb in outcome_lower for verb in self.vague_verbs)
        if has_vague_verb:
            warnings.append("Outcome contains vague, non-measurable verbs")
        
        # Check 4: Reasonable length (10-150 characters)
        if len(outcome_text) < 10:
            issues.append("Outcome is too short")
        elif len(outcome_text) > 150:
            warnings.append("Outcome is quite long; consider simplifying")
        
        # Check 5: Has a clear object (noun after verb)
        words = outcome_text.split()
        if len(words) < 6:
            warnings.append("Outcome may lack sufficient detail")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'outcome': outcome_text
        }
    
    def validate_all_outcomes(self, course_outcomes, modules):
        """Validate all learning outcomes in the course"""
        
        results = {
            'course_outcomes': [],
            'module_outcomes': [],
            'summary': {
                'total_outcomes': 0,
                'valid_outcomes': 0,
                'outcomes_with_issues': 0,
                'outcomes_with_warnings': 0
            }
        }
        
        # Validate course outcomes
        for outcome in course_outcomes:
            validation = self.validate_outcome(outcome['outcome'])
            validation['id'] = outcome['id']
            validation['bloomLevel'] = outcome['bloomLevel']
            results['course_outcomes'].append(validation)
            
            results['summary']['total_outcomes'] += 1
            if validation['valid']:
                results['summary']['valid_outcomes'] += 1
            if validation['issues']:
                results['summary']['outcomes_with_issues'] += 1
            if validation['warnings']:
                results['summary']['outcomes_with_warnings'] += 1
        
        # Validate module outcomes
        for module in modules:
            if 'learningOutcomes' in module:
                for outcome in module['learningOutcomes']:
                    validation = self.validate_outcome(outcome['outcome'])
                    validation['moduleId'] = module['id']
                    validation['moduleTitle'] = module['title']
                    validation['bloomLevel'] = outcome['bloomLevel']
                    results['module_outcomes'].append(validation)
                    
                    results['summary']['total_outcomes'] += 1
                    if validation['valid']:
                        results['summary']['valid_outcomes'] += 1
                    if validation['issues']:
                        results['summary']['outcomes_with_issues'] += 1
                    if validation['warnings']:
                        results['summary']['outcomes_with_warnings'] += 1
        
        return results
    
    def check_bloom_balance(self, statistics):
        """Check if Bloom's taxonomy distribution is balanced"""
        
        recommendations = []
        
        # Check module-level distribution
        module_pct = statistics['module_level']['percentages']
        
        # Too much at Remember level
        if module_pct.get('Remember', 0) > 30:
            recommendations.append("Consider reducing 'Remember' level outcomes (currently > 30%)")
        
        # Too little at Apply level
        if module_pct.get('Apply', 0) < 15:
            recommendations.append("Consider adding more 'Apply' level outcomes (currently < 15%)")
        
        # No higher-order thinking
        higher_order = module_pct.get('Analyze', 0) + module_pct.get('Evaluate', 0) + module_pct.get('Create', 0)
        if higher_order < 20:
            recommendations.append("Consider adding more higher-order outcomes (Analyze/Evaluate/Create)")
        
        return {
            'balanced': len(recommendations) == 0,
            'recommendations': recommendations
        }


# Test validator
if __name__ == "__main__":
    import json
    from topic_extractor import TopicExtractor
    from module_structurer import ModuleStructurer
    from outcome_generator import LearningOutcomeGenerator
    
    # Load and process sample course
    with open('synthetic_courses.json', 'r') as f:
        courses = json.load(f)
    
    sample_course = courses[0]
    
    # Generate complete structure
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
    result = outcome_gen.generate_complete_outcomes(
        structured['modules'],
        sample_course['title'],
        structured['course_type']
    )
    
    # Validate outcomes
    validator = OutcomeValidator()
    validation_results = validator.validate_all_outcomes(
        result['courseLearningOutcomes'],
        result['modules']
    )
    
    # Check balance
    balance_check = validator.check_bloom_balance(result['statistics'])
    
    # Display validation results
    print("=" * 80)
    print("LEARNING OUTCOME VALIDATION REPORT")
    print("=" * 80)
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total Outcomes: {validation_results['summary']['total_outcomes']}")
    print(f"   Valid Outcomes: {validation_results['summary']['valid_outcomes']}")
    print(f"   With Issues: {validation_results['summary']['outcomes_with_issues']}")
    print(f"   With Warnings: {validation_results['summary']['outcomes_with_warnings']}")
    
    print(f"\n✓ Validation Success Rate: {validation_results['summary']['valid_outcomes'] / validation_results['summary']['total_outcomes'] * 100:.1f}%")
    
    if not balance_check['balanced']:
        print(f"\n⚠️  BLOOM'S TAXONOMY BALANCE RECOMMENDATIONS:")
        for rec in balance_check['recommendations']:
            print(f"   • {rec}")
    else:
        print(f"\n✅ Bloom's taxonomy distribution is well-balanced!")
    
    # Show any issues
    print(f"\n" + "=" * 80)
    print("DETAILED VALIDATION RESULTS:")
    print("=" * 80)
    
    if validation_results['summary']['outcomes_with_issues'] > 0:
        print("\n❌ OUTCOMES WITH ISSUES:")
        for outcome in validation_results['course_outcomes'] + validation_results['module_outcomes']:
            if outcome['issues']:
                print(f"\n   Outcome: {outcome['outcome']}")
                for issue in outcome['issues']:
                    print(f"      ❌ {issue}")
    
    if validation_results['summary']['outcomes_with_warnings'] > 0:
        print("\n⚠️  OUTCOMES WITH WARNINGS:")
        for outcome in validation_results['course_outcomes'] + validation_results['module_outcomes']:
            if outcome['warnings']:
                print(f"\n   Outcome: {outcome['outcome']}")
                for warning in outcome['warnings']:
                    print(f"      ⚠️  {warning}")
    

    print("\n" + "=" * 80)
