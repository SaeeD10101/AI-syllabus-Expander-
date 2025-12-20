import os
import re

def fix_imports_in_file(filepath):
    """Fix imports in a Python file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match: from module_name import ...
    # Where module_name doesn't start with a dot or 'src.'
    pattern = r'^from\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+import'
    
    # Files in src/ that need relative imports
    src_modules = [
        'knowledge_base', 'topic_extractor', 'module_structurer',
        'outcome_generator', 'outcome_validator', 'assessment_generator',
        'assessment_analyzer', 'question_generator', 'alignment_matrix',
        'export_utils', 'dataset_generator'
    ]
    
    lines = content.split('\n')
    updated_lines = []
    
    for line in lines:
        match = re.match(pattern, line)
        if match:
            module = match.group(1)
            if module in src_modules:
                # Convert to relative import
                line = re.sub(f'^from {module}', f'from .{module}', line)
        updated_lines.append(line)
    
    updated_content = '\n'.join(updated_lines)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Fixed: {filepath}")

# Fix all Python files in src/
src_dir = 'Dascpj/syllabus_expander_project/src'
for filename in os.listdir(src_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        filepath = os.path.join(src_dir, filename)
        fix_imports_in_file(filepath)

print("All imports fixed!")
