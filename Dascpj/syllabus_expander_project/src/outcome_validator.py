import re

# Fixed import
from .knowledge_base import BLOOM_TAXONOMY

class OutcomeValidator:
    """Validate learning outcomes for quality and alignment"""
    
    def __init__(self):
        self.bloom_taxonomy = BLOOM_TAXONOMY
        self.valid_verbs = self._extract_all_verbs()
    
    def _extract_all_verbs(self):
        """Extract all valid action verbs from Bloom's taxonomy"""
        all_verbs = []
        for level_data in self.bloom_taxonomy.values():
            all_verbs.extend(level_data['verbs'])
        return set(verb.lower() for verb in all_verbs)
    
    def validate_outcome(self, outcome_dict):
        """
        Validate a single learning outcome
        
        Args:
            outcome_dict (dict): Outcome dictionary with 'outcome' and 'bloom_level'
            
        Returns:
            dict: Validation results
        """
        validation = {
            'valid': True,
            'issues': [],
            'suggestions': []
        }
        
        outcome_text = outcome_dict.get('outcome', '').lower()
        bloom_level = outcome_dict.get('bloom_level', '').lower()
        
        # Check 1: Has action verb
        has_verb = any(verb in outcome_text for verb in self.valid_verbs)
        if not has_verb:
            validation['valid'] = False
            validation['issues'].append("No clear action verb found")
            validation['suggestions'].append("Start with an action verb from Bloom's Taxonomy")
        
        # Check 2: Bloom's level matches verb
        if bloom_level in self.bloom_taxonomy:
            level_verbs = [v.lower() for v in self.bloom_taxonomy[bloom_level]['verbs']]
            verb_matches = any(verb in outcome_text for verb in level_verbs)
            if not verb_matches:
                validation['valid'] = False
                validation['issues'].append(f"Verb doesn't match {bloom_level} level")
                validation['suggestions'].append(f"Use verbs like: {', '.join(level_verbs[:3])}")
        
        # Check 3: Measurable
        if not self._is_measurable(outcome_text):
            validation['suggestions'].append("Consider adding measurable criteria")
        
        # Check 4: Length check
        word_count = len(outcome_text.split())
        if word_count < 3:
            validation['valid'] = False
            validation['issues'].append("Outcome too short")
        elif word_count > 25:
            validation['suggestions'].append("Consider making outcome more concise")
        
        return validation
    
    def _is_measurable(self, outcome_text):
        """Check if outcome contains measurable elements"""
        measurable_indicators = [
            'accuracy', 'correctly', 'effectively', 'efficiently',
            'criteria', 'standard', 'demonstrate', 'produce',
            'create', 'analyze', 'evaluate', 'compare'
        ]
        return any(indicator in outcome_text.lower() for indicator in measurable_indicators)
    
    def validate_all_outcomes(self, module_structure):
        """
        Validate all outcomes in module structure
        
        Args:
            module_structure (dict): Complete module structure
            
        Returns:
            dict: Overall validation results
        """
        results = {
            'total_outcomes': 0,
            'valid_outcomes': 0,
            'invalid_outcomes': 0,
            'modules': []
        }
        
        for module in module_structure.get('modules', []):
            module_results = {
                'module_name': module.get('module_name', ''),
                'outcomes': []
            }
            
            for outcome in module.get('learning_outcomes', []):
                validation = self.validate_outcome(outcome)
                module_results['outcomes'].append({
                    'outcome': outcome.get('outcome', ''),
                    'validation': validation
                })
                
                results['total_outcomes'] += 1
                if validation['valid']:
                    results['valid_outcomes'] += 1
                else:
                    results['invalid_outcomes'] += 1
            
            results['modules'].append(module_results)
        
        return results
    
    def get_validation_report(self, validation_results):
        """
        Generate human-readable validation report
        
        Args:
            validation_results (dict): Results from validate_all_outcomes
            
        Returns:
            str: Formatted report
        """
        report = "LEARNING OUTCOMES VALIDATION REPORT\n"
        report += "=" * 50 + "\n\n"
        
        report += f"Total Outcomes: {validation_results['total_outcomes']}\n"
        report += f"Valid: {validation_results['valid_outcomes']}\n"
        report += f"Invalid: {validation_results['invalid_outcomes']}\n\n"
        
        for module_result in validation_results['modules']:
            report += f"\n{module_result['module_name']}\n"
            report += "-" * len(module_result['module_name']) + "\n\n"
            
            for outcome_result in module_result['outcomes']:
                validation = outcome_result['validation']
                status = "✓" if validation['valid'] else "✗"
                
                report += f"{status} {outcome_result['outcome']}\n"
                
                if validation['issues']:
                    report += "  Issues:\n"
                    for issue in validation['issues']:
                        report += f"    - {issue}\n"
                
                if validation['suggestions']:
                    report += "  Suggestions:\n"
                    for suggestion in validation['suggestions']:
                        report += f"    - {suggestion}\n"
                
                report += "\n"
        
        return report


# Standalone function
def validate_learning_outcomes(module_structure):
    """Convenience function to validate outcomes"""
    validator = OutcomeValidator()
    return validator.validate_all_outcomes(module_structure)


if __name__ == "__main__":
    # Test validation
    sample_outcome = {
        'outcome': 'Understand machine learning concepts',
        'bloom_level': 'understand'
    }
    
    validator = OutcomeValidator()
    result = validator.validate_outcome(sample_outcome)
    print(result)
