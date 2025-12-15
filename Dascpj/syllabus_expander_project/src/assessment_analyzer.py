# assessment_analyzer.py

class AssessmentAnalyzer:
    """Analyze assessment blueprint for quality and alignment"""
    
    def __init__(self):
        pass
    
    def analyze_bloom_coverage(self, blueprint, outcomes_statistics):
        """Check if assessments cover all Bloom levels appropriately"""
        
        # Get all Bloom levels from assessments
        assessed_blooms = set()
        for component in blueprint['components']:
            assessed_blooms.update(component['bloomLevels'])
        
        # Get Bloom levels from learning outcomes
        outcome_blooms = set()
        module_stats = outcomes_statistics['module_level']['counts']
        for level, count in module_stats.items():
            if count > 0:
                outcome_blooms.add(level)
        
        # Check coverage
        uncovered = outcome_blooms - assessed_blooms
        
        return {
            'assessed_blooms': list(assessed_blooms),
            'outcome_blooms': list(outcome_blooms),
            'uncovered_blooms': list(uncovered),
            'coverage_percentage': (len(assessed_blooms) / max(len(outcome_blooms), 1)) * 100
        }
    
    def analyze_outcome_alignment(self, blueprint, course_outcomes, modules):
        """Check if all learning outcomes are assessed"""
        
        # Collect all linked outcomes from assessments
        assessed_outcomes = set()
        for component in blueprint['components']:
            assessed_outcomes.update(component['linkedLOs'])
            assessed_outcomes.update(component['linkedModuleLOs'])
        
        # Collect all learning outcomes
        all_outcomes = set()
        for outcome in course_outcomes:
            all_outcomes.add(outcome['id'])
        
        for module in modules:
            if 'learningOutcomes' in module:
                for idx in range(len(module['learningOutcomes'])):
                    all_outcomes.add(f"M{module['id']}-LO{idx+1}")
        
        # Calculate coverage
        unassessed = all_outcomes - assessed_outcomes
        
        return {
            'total_outcomes': len(all_outcomes),
            'assessed_outcomes': len(assessed_outcomes),
            'unassessed_outcomes': list(unassessed),
            'coverage_percentage': (len(assessed_outcomes) / max(len(all_outcomes), 1)) * 100
        }
    
    def analyze_weight_distribution(self, blueprint):
        """Analyze if weight distribution is appropriate"""
        
        issues = []
        warnings = []
        
        # Check if any single assessment is too heavy
        for component in blueprint['components']:
            if component['weight'] > 40:
                issues.append(f"{component['type']} has excessive weight ({component['weight']}%). Consider redistributing.")
            elif component['weight'] > 35:
                warnings.append(f"{component['type']} has high weight ({component['weight']}%). Ensure students have adequate preparation.")
        
        # Check if continuous assessment is adequate
        continuous_types = ['Quizzes', 'Labs/Assignments']
        continuous_weight = sum(c['weight'] for c in blueprint['components'] 
                               if any(t in c['type'] for t in continuous_types))
        
        if continuous_weight < 25:
            warnings.append(f"Low continuous assessment weight ({continuous_weight}%). Consider adding more formative assessments.")
        
        # Check if high-stakes assessments dominate
        high_stakes = ['Midterm Exam', 'Final Exam']
        high_stakes_weight = sum(c['weight'] for c in blueprint['components'] 
                                if c['type'] in high_stakes)
        
        if high_stakes_weight > 60:
            issues.append(f"High-stakes exams dominate ({high_stakes_weight}%). This may increase student anxiety.")
        
        return {
            'issues': issues,
            'warnings': warnings,
            'continuous_weight': continuous_weight,
            'high_stakes_weight': high_stakes_weight
        }
    
    def analyze_timing(self, blueprint):
        """Analyze assessment timing for student workload"""
        
        # Simple heuristic: check for reasonable distribution
        timings = [c['timing'] for c in blueprint['components']]
        
        warnings = []
        
        # Check if too many assessments in final week
        final_assessments = sum(1 for t in timings if 'Final' in t or 'Week {' in t)
        if final_assessments > 2:
            warnings.append("Multiple major assessments scheduled near end of course. Consider spreading workload.")
        
        return {
            'warnings': warnings,
            'assessment_count': len(blueprint['components'])
        }
    
    def generate_analysis_report(self, blueprint, outcomes_statistics, 
                                 course_outcomes, modules):
        """Generate complete analysis report"""
        
        bloom_analysis = self.analyze_bloom_coverage(blueprint, outcomes_statistics)
        alignment_analysis = self.analyze_outcome_alignment(blueprint, course_outcomes, modules)
        weight_analysis = self.analyze_weight_distribution(blueprint)
        timing_analysis = self.analyze_timing(blueprint)
        
        # Calculate overall quality score
        quality_score = 0
        max_score = 100
        
        # Bloom coverage (30 points)
        quality_score += (bloom_analysis['coverage_percentage'] / 100) * 30
        
        # Outcome alignment (30 points)
        quality_score += (alignment_analysis['coverage_percentage'] / 100) * 30
        
        # Weight distribution (20 points)
        if not weight_analysis['issues']:
            quality_score += 20
        elif not weight_analysis['warnings']:
            quality_score += 15
        else:
            quality_score += 10
        
        # Timing (20 points)
        if not timing_analysis['warnings']:
            quality_score += 20
        else:
            quality_score += 15
        
        return {
            'quality_score': round(quality_score, 1),
            'bloom_coverage': bloom_analysis,
            'outcome_alignment': alignment_analysis,
            'weight_distribution': weight_analysis,
            'timing': timing_analysis,
            'overall_grade': self.get_grade(quality_score)
        }
    
    def get_grade(self, score):
        """Convert quality score to grade"""
        if score >= 90:
            return 'Excellent'
        elif score >= 80:
            return 'Good'
        elif score >= 70:
            return 'Satisfactory'
        elif score >= 60:
            return 'Needs Improvement'
        else:
            return 'Poor'


# Test the analyzer
if __name__ == "__main__":
    import json
    from topic_extractor import TopicExtractor
    from module_structurer import ModuleStructurer
    from outcome_generator import LearningOutcomeGenerator
    from assessment_generator import AssessmentBlueprintGenerator
    
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
    outcomes_result = outcome_gen.generate_complete_outcomes(
        structured['modules'],
        sample_course['title'],
        structured['course_type']
    )
    
    assessment_gen = AssessmentBlueprintGenerator()
    blueprint = assessment_gen.generate_blueprint(
        structured['course_type'],
        len(structured['modules']),
        sample_course['duration'],
        outcomes_result['courseLearningOutcomes'],
        outcomes_result['modules']
    )
    
    # Analyze blueprint
    analyzer = AssessmentAnalyzer()
    analysis = analyzer.generate_analysis_report(
        blueprint,
        outcomes_result['statistics'],
        outcomes_result['courseLearningOutcomes'],
        outcomes_result['modules']
    )
    
    # Display analysis
    print("=" * 90)
    print("ASSESSMENT BLUEPRINT ANALYSIS")
    print("=" * 90)
    
    print(f"\n📊 OVERALL QUALITY SCORE: {analysis['quality_score']}/100 - {analysis['overall_grade']}")
    
    print(f"\n🎯 BLOOM'S TAXONOMY COVERAGE:")
    print(f"   Coverage: {analysis['bloom_coverage']['coverage_percentage']:.1f}%")
    print(f"   Assessed Levels: {', '.join(analysis['bloom_coverage']['assessed_blooms'])}")
    if analysis['bloom_coverage']['uncovered_blooms']:
        print(f"   ⚠️  Uncovered Levels: {', '.join(analysis['bloom_coverage']['uncovered_blooms'])}")
    
    print(f"\n🔗 LEARNING OUTCOME ALIGNMENT:")
    print(f"   Total Outcomes: {analysis['outcome_alignment']['total_outcomes']}")
    print(f"   Assessed Outcomes: {analysis['outcome_alignment']['assessed_outcomes']}")
    print(f"   Coverage: {analysis['outcome_alignment']['coverage_percentage']:.1f}%")
    if analysis['outcome_alignment']['unassessed_outcomes']:
        print(f"   ⚠️  Unassessed: {', '.join(analysis['outcome_alignment']['unassessed_outcomes'][:5])}")
    
    print(f"\n⚖️  WEIGHT DISTRIBUTION:")
    print(f"   Continuous Assessment: {analysis['weight_distribution']['continuous_weight']}%")
    print(f"   High-Stakes Exams: {analysis['weight_distribution']['high_stakes_weight']}%")
    
    if analysis['weight_distribution']['issues']:
        print(f"\n   ❌ Issues:")
        for issue in analysis['weight_distribution']['issues']:
            print(f"      • {issue}")
    
    if analysis['weight_distribution']['warnings']:
        print(f"\n   ⚠️  Warnings:")
        for warning in analysis['weight_distribution']['warnings']:
            print(f"      • {warning}")
    
    print(f"\n⏰ TIMING ANALYSIS:")
    print(f"   Total Assessments: {analysis['timing']['assessment_count']}")
    if analysis['timing']['warnings']:
        for warning in analysis['timing']['warnings']:
            print(f"   ⚠️  {warning}")
    
    print("\n" + "=" * 90)