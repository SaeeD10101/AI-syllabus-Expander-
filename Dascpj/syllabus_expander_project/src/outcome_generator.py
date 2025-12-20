import random

# Fixed import - use relative import
from .knowledge_base import BLOOM_TAXONOMY

class OutcomeGenerator:
    """Generate learning outcomes aligned with Bloom's Taxonomy"""
    
    def __init__(self):
        self.bloom_taxonomy = BLOOM_TAXONOMY
    
    def generate_outcomes_for_topic(self, topic, num_outcomes=3, bloom_levels=None):
        """
        Generate learning outcomes for a specific topic
        
        Args:
            topic (str): Topic name
            num_outcomes (int): Number of outcomes to generate
            bloom_levels (list): Specific Bloom's levels to use (optional)
            
        Returns:
            list: List of learning outcome dictionaries
        """
        if bloom_levels is None:
            # Default distribution across Bloom's levels
            bloom_levels = ['remember', 'understand', 'apply']
        
        outcomes = []
        for i in range(num_outcomes):
            level = bloom_levels[i % len(bloom_levels)]
            outcome = self.create_outcome(topic, level)
            outcomes.append(outcome)
        
        return outcomes
    
    def create_outcome(self, topic, bloom_level):
        """
        Create a single learning outcome
        
        Args:
            topic (str): Topic name
            bloom_level (str): Bloom's taxonomy level
            
        Returns:
            dict: Learning outcome with level and description
        """
        level_data = self.bloom_taxonomy.get(bloom_level, self.bloom_taxonomy['understand'])
        
        # Select random verb from the level
        verb = random.choice(level_data['verbs'])
        
        # Generate outcome statement
        outcome_text = f"{verb.capitalize()} {topic.lower()}"
        
        return {
            'bloom_level': bloom_level.capitalize(),
            'outcome': outcome_text,
            'verb': verb,
            'topic': topic
        }
    
    def generate_outcomes_for_module(self, module_data, outcomes_per_topic=2):
        """
        Generate learning outcomes for an entire module
        
        Args:
            module_data (dict): Module dictionary with topics
            outcomes_per_topic (int): Number of outcomes per topic
            
        Returns:
            dict: Module data with added learning outcomes
        """
        module_outcomes = []
        
        topics = module_data.get('topics', [])
        
        # Distribute Bloom's levels across topics
        bloom_sequence = ['remember', 'understand', 'apply', 'analyze', 'evaluate', 'create']
        
        for i, topic in enumerate(topics):
            # Assign Bloom's levels progressively
            base_level = bloom_sequence[min(i, len(bloom_sequence) - 1)]
            next_level = bloom_sequence[min(i + 1, len(bloom_sequence) - 1)]
            
            topic_outcomes = self.generate_outcomes_for_topic(
                topic,
                num_outcomes=outcomes_per_topic,
                bloom_levels=[base_level, next_level]
            )
            
            module_outcomes.extend(topic_outcomes)
        
        # Add outcomes to module data
        module_data['learning_outcomes'] = module_outcomes
        
        return module_data
    
    def generate_outcomes_for_all_modules(self, module_structure, outcomes_per_topic=2):
        """
        Generate learning outcomes for all modules in the structure
        
        Args:
            module_structure (dict): Complete module structure
            outcomes_per_topic (int): Number of outcomes per topic
            
        Returns:
            dict: Updated module structure with learning outcomes
        """
        modules = module_structure.get('modules', [])
        
        for module in modules:
            self.generate_outcomes_for_module(module, outcomes_per_topic)
        
        return module_structure
    
    def format_outcomes(self, module_structure):
        """
        Format learning outcomes into readable text
        
        Args:
            module_structure (dict): Module structure with outcomes
            
        Returns:
            str: Formatted outcomes text
        """
        output = "LEARNING OUTCOMES\n"
        output += "=" * 50 + "\n\n"
        
        for module in module_structure.get('modules', []):
            output += f"{module['module_name']}\n"
            output += "-" * len(module['module_name']) + "\n\n"
            
            outcomes = module.get('learning_outcomes', [])
            for i, outcome in enumerate(outcomes, 1):
                output += f"{i}. [{outcome['bloom_level']}] {outcome['outcome']}\n"
            
            output += "\n"
        
        return output
    
    def get_bloom_distribution(self, module_structure):
        """
        Analyze the distribution of Bloom's taxonomy levels
        
        Args:
            module_structure (dict): Module structure with outcomes
            
        Returns:
            dict: Count of outcomes per Bloom's level
        """
        distribution = {level: 0 for level in self.bloom_taxonomy.keys()}
        
        for module in module_structure.get('modules', []):
            for outcome in module.get('learning_outcomes', []):
                level = outcome['bloom_level'].lower()
                distribution[level] = distribution.get(level, 0) + 1
        
        return distribution
    
    def validate_outcome_coverage(self, module_structure, min_outcomes_per_module=3):
        """
        Validate that each module has sufficient learning outcomes
        
        Args:
            module_structure (dict): Module structure with outcomes
            min_outcomes_per_module (int): Minimum outcomes required
            
        Returns:
            dict: Validation results
        """
        validation = {
            'valid': True,
            'issues': [],
            'total_outcomes': 0
        }
        
        for module in module_structure.get('modules', []):
            num_outcomes = len(module.get('learning_outcomes', []))
            validation['total_outcomes'] += num_outcomes
            
            if num_outcomes < min_outcomes_per_module:
                validation['valid'] = False
                validation['issues'].append(
                    f"{module['module_name']} has only {num_outcomes} outcomes "
                    f"(minimum: {min_outcomes_per_module})"
                )
        
        return validation
    
    def enhance_outcome_specificity(self, outcome_dict, context=""):
        """
        Make learning outcomes more specific and measurable
        
        Args:
            outcome_dict (dict): Basic outcome dictionary
            context (str): Additional context for specificity
            
        Returns:
            dict: Enhanced outcome with more detail
        """
        verb = outcome_dict['verb']
        topic = outcome_dict['topic']
        bloom_level = outcome_dict['bloom_level']
        
        # Add measurement criteria based on Bloom's level
        criteria_templates = {
            'remember': f"with 80% accuracy",
            'understand': f"by explaining key concepts",
            'apply': f"in real-world scenarios",
            'analyze': f"by comparing and contrasting different approaches",
            'evaluate': f"using established criteria",
            'create': f"demonstrating originality and innovation"
        }
        
        criteria = criteria_templates.get(bloom_level.lower(), "")
        
        enhanced_outcome = f"{verb.capitalize()} {topic.lower()} {criteria}"
        
        outcome_dict['outcome'] = enhanced_outcome
        outcome_dict['measurable'] = True
        
        return outcome_dict


# Standalone function
def generate_learning_outcomes(module_structure, outcomes_per_topic=2):
    """
    Convenience function to generate outcomes without instantiating the class
    
    Args:
        module_structure (dict): Module structure
        outcomes_per_topic (int): Number of outcomes per topic
        
    Returns:
        dict: Updated module structure with outcomes
    """
    generator = OutcomeGenerator()
    return generator.generate_outcomes_for_all_modules(module_structure, outcomes_per_topic)


# Example usage
if __name__ == "__main__":
    # Sample module structure
    sample_modules = {
        'course_domain': 'computer_science',
        'total_modules': 2,
        'modules': [
            {
                'module_number': 1,
                'module_name': 'Module 1: Introduction to Machine Learning',
                'topics': ['Supervised Learning', 'Unsupervised Learning']
            },
            {
                'module_number': 2,
                'module_name': 'Module 2: Deep Learning',
                'topics': ['Neural Networks', 'Convolutional Networks']
            }
        ]
    }
    
    generator = OutcomeGenerator()
    updated_structure = generator.generate_outcomes_for_all_modules(sample_modules)
    
    print(generator.format_outcomes(updated_structure))
    print("\nBloom's Distribution:")
    print(generator.get_bloom_distribution(updated_structure))
