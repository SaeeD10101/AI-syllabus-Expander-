# knowledge_base.py

# Bloom's Taxonomy Verb Templates
BLOOM_TAXONOMY = {
    "Remember": {
        "verbs": ["define", "identify", "list", "name", "recall", "recognize", "state", "describe", "label", "match", "select"],
        "question_templates": [
            "What is the definition of {concept}?",
            "Identify the main components of {concept}.",
            "List the key features of {concept}.",
            "Which of the following best describes {concept}?"
        ],
        "outcome_templates": [
            "Students will be able to define {concept}",
            "Students will be able to identify key {concept}",
            "Students will be able to list the main {concept}",
            "Students will be able to recall fundamental {concept}"
        ]
    },
    "Understand": {
        "verbs": ["classify", "describe", "discuss", "explain", "interpret", "summarize", "compare", "illustrate", "paraphrase"],
        "question_templates": [
            "Explain the relationship between {concept1} and {concept2}.",
            "Describe how {concept} works.",
            "Summarize the main principles of {concept}.",
            "Compare {concept1} with {concept2}."
        ],
        "outcome_templates": [
            "Students will be able to explain {concept}",
            "Students will be able to describe the principles of {concept}",
            "Students will be able to summarize {concept}",
            "Students will be able to interpret {concept}"
        ]
    },
    "Apply": {
        "verbs": ["apply", "demonstrate", "implement", "solve", "use", "execute", "operate", "calculate", "practice"],
        "question_templates": [
            "Apply {concept} to solve {problem}.",
            "Demonstrate how to use {concept} in {context}.",
            "Implement {concept} to achieve {goal}.",
            "Use {concept} to calculate {target}."
        ],
        "outcome_templates": [
            "Students will be able to apply {concept} to {context}",
            "Students will be able to implement {concept}",
            "Students will be able to use {concept} to solve problems",
            "Students will be able to demonstrate {concept}"
        ]
    },
    "Analyze": {
        "verbs": ["analyze", "compare", "contrast", "differentiate", "examine", "investigate", "categorize", "distinguish"],
        "question_templates": [
            "Analyze the factors that influence {concept}.",
            "Compare and contrast {concept1} with {concept2}.",
            "Examine the relationship between {concept1} and {concept2}.",
            "Differentiate between {concept1} and {concept2}."
        ],
        "outcome_templates": [
            "Students will be able to analyze {concept}",
            "Students will be able to compare different {concept}",
            "Students will be able to examine the components of {concept}",
            "Students will be able to differentiate between {concept}"
        ]
    },
    "Evaluate": {
        "verbs": ["assess", "critique", "evaluate", "judge", "justify", "validate", "argue", "defend", "support"],
        "question_templates": [
            "Evaluate the effectiveness of {concept} in {context}.",
            "Critique the approach used in {concept}.",
            "Justify the use of {concept} over {alternative}.",
            "Assess the advantages and disadvantages of {concept}."
        ],
        "outcome_templates": [
            "Students will be able to evaluate {concept}",
            "Students will be able to critique {concept}",
            "Students will be able to justify decisions about {concept}",
            "Students will be able to assess {concept}"
        ]
    },
    "Create": {
        "verbs": ["create", "design", "develop", "construct", "formulate", "propose", "plan", "produce", "generate"],
        "question_templates": [
            "Design a {concept} that addresses {problem}.",
            "Create a plan to implement {concept}.",
            "Develop a solution using {concept}.",
            "Propose a new approach to {concept}."
        ],
        "outcome_templates": [
            "Students will be able to design {concept}",
            "Students will be able to create {concept}",
            "Students will be able to develop solutions using {concept}",
            "Students will be able to construct {concept}"
        ]
    }
}

# Assessment Type Templates
ASSESSMENT_TYPES = {
    "Pre-Test": {
        "typical_weight": 5,
        "weight_range": (0, 10),
        "description": "Diagnostic assessment to gauge prior knowledge",
        "suitable_bloom": ["Remember", "Understand"],
        "format": "Multiple choice, True/False"
    },
    "Quizzes": {
        "typical_weight": 20,
        "weight_range": (15, 30),
        "description": "Regular assessments of module comprehension",
        "suitable_bloom": ["Remember", "Understand", "Apply"],
        "format": "Mixed: MCQ, short answer"
    },
    "Midterm Exam": {
        "typical_weight": 20,
        "weight_range": (15, 25),
        "description": "Comprehensive exam covering first half of course",
        "suitable_bloom": ["Understand", "Apply", "Analyze"],
        "format": "Mixed format"
    },
    "Labs/Assignments": {
        "typical_weight": 25,
        "weight_range": (20, 35),
        "description": "Hands-on practical exercises",
        "suitable_bloom": ["Apply", "Analyze"],
        "format": "Practical work, problem sets"
    },
    "Project": {
        "typical_weight": 20,
        "weight_range": (15, 30),
        "description": "Comprehensive project synthesizing course concepts",
        "suitable_bloom": ["Analyze", "Evaluate", "Create"],
        "format": "Project deliverable + documentation"
    },
    "Final Exam": {
        "typical_weight": 10,
        "weight_range": (10, 30),
        "description": "Comprehensive final assessment",
        "suitable_bloom": ["All levels"],
        "format": "Comprehensive exam"
    }
}

# Domain-specific keyword patterns
DOMAIN_INDICATORS = {
    "technical": ["algorithm", "programming", "code", "software", "system", "data", "network", "database"],
    "theoretical": ["theory", "concept", "principle", "framework", "model", "analysis"],
    "practical": ["application", "implementation", "practice", "exercise", "lab", "project", "hands-on"],
    "analytical": ["analyze", "examine", "investigate", "evaluate", "assess", "compare"]
}