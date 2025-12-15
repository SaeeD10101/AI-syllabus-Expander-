# src/export_utils.py

import pandas as pd

class ExportUtilities:
    """Export utilities for CSV and reports"""
    
    def export_to_csv(self, results, filename):
        """Export alignment matrix to CSV"""
        df = pd.DataFrame(results['alignmentMatrix'])
        df_export = df[['module', 'learningOutcome', 'bloomLevel', 'assessmentTypes', 'questionIds', 'coverage']]
        df_export['assessmentTypes'] = df_export['assessmentTypes'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
        df_export['questionIds'] = df_export['questionIds'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
        df_export.to_csv(filename, index=False)
        print(f"📊 Exported to: {filename}")
    
    def export_to_json(self, results, filename):
        """Export to JSON"""
        import json
        with open(filename, 'w') as f:
            json.dump(results, indent=2, fp=f)
        print(f"📄 Exported to: {filename}")
    
    def generate_text_report(self, results):
        """Generate text report"""
        report = []
        report.append("="*80)
        report.append(f"SYLLABUS: {results['metadata']['courseTitle']}")
        report.append("="*80)
        report.append(f"\nModules: {len(results['modules'])}")
        report.append(f"Course LOs: {len(results['courseLearningOutcomes'])}")
        report.append(f"Questions: {len(results['sampleQuestions'])}")
        report.append(f"Quality Score: {results.get('assessmentAnalysis', {}).get('quality_score', 'N/A')}")
        return '\n'.join(report)