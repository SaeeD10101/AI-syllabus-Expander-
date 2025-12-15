# AI Syllabus Expander & Assessment Mapper

An intelligent tool that transforms course specifications into comprehensive, structured syllabi with aligned assessments and learning outcomes.

---

## 📋 Project Overview

This application uses Natural Language Processing (NLP) to automatically generate complete course syllabi from minimal input. It creates structured topic outlines, learning outcomes aligned with Bloom's Taxonomy, assessment blueprints, sample questions, and comprehensive alignment matrices.

### Key Features

✅ **Automated Topic Extraction** - Extracts 4-8 main topics from course descriptions  
✅ **Learning Outcomes Generation** - Creates measurable outcomes at course and topic levels  
✅ **Assessment Blueprint** - Recommends assessment types with appropriate weights  
✅ **Question Generation** - Produces MCQs, short answer, and case study questions  
✅ **Alignment Matrix** - Maps topics → outcomes → assessments → questions  
✅ **Multiple Export Formats** - JSON, CSV, and TXT reports for easy editing

---

## 🎯 Purpose

Designed for educators and instructional designers who need to:
- Quickly develop comprehensive course syllabi
- Ensure alignment between topics, outcomes, and assessments
- Generate sample assessment items across Bloom's taxonomy levels
- Save time on initial syllabus drafting and planning

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   Web Interface (HTML/JS)                        │
│  - index.html: User input form                                   │
│  - app.js: Frontend logic & API calls                           │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP POST/GET
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Flask Backend API (app.py)                          │
│  - /api/health: Health check endpoint                           │
│  - /api/process: Main processing endpoint                       │
│  - Orchestrates all processing modules                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Processing Pipeline                           │
│                                                                  │
│  1. Knowledge Base → Provides domain knowledge & templates      │
│  2. Dataset Generator → Creates synthetic training data         │
│  3. Topic Extractor → Extracts main topics (NLP)               │
│  4. Module Structurer → Organizes topics into modules          │
│  5. Outcome Generator → Creates learning outcomes              │
│  6. Outcome Validator → Validates Bloom's alignment            │
│  7. Assessment Generator → Designs assessment blueprint         │
│  8. Assessment Analyzer → Analyzes assessment distribution      │
│  9. Question Generator → Creates sample questions              │
│  10. Alignment Matrix → Maps all components together           │
│  11. Export Utils → Generates output files                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Output Generation                             │
│  - JSON: Complete structured data                               │
│  - CSV: Alignment matrix                                        │
│  - TXT: Formatted report                                        │
│  Files saved to: output/ directory                              │
└─────────────────────────────────────────────────────────────────┘

Alternative: CLI Mode (main_system.py)
└── Direct command-line interface bypassing web layer
```

---

## 🛠️ Technology Stack

### Frontend
- **HTML5** - Web interface structure
- **JavaScript (Vanilla)** - Frontend logic and interactivity
- **CSS3** - Styling and responsive design
- **Fetch API** - Asynchronous API communication

### Backend
- **Python 3.8+** - Core programming language
- **Flask** - Web framework for API
- **Flask-CORS** - Cross-origin resource sharing

### NLP & Data Processing
- **spaCy** - Natural language processing
- **scikit-learn** - TF-IDF and clustering algorithms
- **pandas** - Data manipulation
- **NLTK** - Text preprocessing

### Export Libraries
- **python-docx** - Word document generation (optional)
- **openpyxl** - Excel file handling (optional)

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Backend Setup


# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

### No Separate Frontend Setup Required
The web interface is pure HTML/CSS/JavaScript - no build step needed!

---

## 🚀 Running the Application

### Option 1: Web Interface

```bash
# Start Flask backend server
python app.py

# Server runs on http://localhost:5000
# Open web/index.html in your browser
# Or navigate to http://localhost:5000 if Flask serves the frontend
```

### Option 2: Command Line Interface

```bash
# Run CLI version directly
python main_system.py

# Follow the prompts to enter course information
```

---

## 💻 Usage

### Web Interface

### Step 1: Input Course Information
Open the web interface and enter:
- **Course Title** (e.g., "Introduction to Data Science")
- **Course Description** (detailed text about course content)
- **Scope** (target audience, prerequisites, level)
- **Duration** (total hours or credit hours)

### Step 2: Generate Syllabus
Click "Generate Syllabus" button to process your input through the NLP pipeline.

### Step 3: Review Results
The interface displays:
1. **Topics Outline** - Structured modules with estimated hours
2. **Learning Outcomes** - Course and topic-level objectives with Bloom's levels
3. **Assessment Blueprint** - Recommended assessment mix with weights
4. **Sample Questions** - MCQs, short answer, and case studies
5. **Alignment Matrix** - Complete mapping of all components

### Step 4: Export
Download your syllabus in multiple formats:
- **JSON** - Complete structured data
- **CSV** - Alignment matrix for spreadsheets
- **TXT** - Formatted text report

All files are saved to the `output/` directory.

### Command Line Interface

```bash
python main_system.py
```

Follow the interactive prompts to enter course details and generate syllabus directly via terminal.

---

## 📊 Project Structure

```
syllabus_expander_project/
│
├── requirements.txt              # Python dependencies
├── main_system.py                # CLI version (command-line interface)
├── app.py                        # Flask web backend API ⭐
│
├── src/                          # Core Processing Modules
│   ├── knowledge_base.py         # Domain knowledge & templates
│   ├── dataset_generator.py     # Synthetic training data creation
│   ├── topic_extractor.py       # NLP-based topic extraction
│   ├── module_structurer.py     # Topic organization into modules
│   ├── outcome_generator.py     # Learning outcomes creation
│   ├── outcome_validator.py     # Bloom's taxonomy validation
│   ├── assessment_generator.py  # Assessment blueprint design
│   ├── assessment_analyzer.py   # Assessment distribution analysis
│   ├── question_generator.py    # Sample question creation
│   ├── alignment_matrix.py      # Component mapping system
│   └── export_utils.py          # Export functionality (JSON/CSV/TXT)
│
├── web/                          # Web Interface ⭐
│   ├── index.html               # User input form & results display
│   └── app.js                   # Frontend JavaScript & API calls
│
├── data/                         # Data Storage
│   └── synthetic_courses.json   # Generated synthetic course data
│
└── output/                       # Generated Results
    └── (syllabus files created here)
```

### Module Descriptions

#### Core Backend Modules (src/)
- **knowledge_base.py**: Stores domain-specific knowledge, Bloom's verbs, question templates
- **dataset_generator.py**: Creates synthetic course data for testing and training
- **topic_extractor.py**: Uses NLP (TF-IDF, spaCy) to extract main topics from descriptions
- **module_structurer.py**: Organizes extracted topics into logical course modules
- **outcome_generator.py**: Generates measurable learning outcomes aligned to Bloom's taxonomy
- **outcome_validator.py**: Validates that outcomes meet pedagogical standards
- **assessment_generator.py**: Creates assessment blueprint with types and weights
- **assessment_analyzer.py**: Analyzes assessment distribution and balance
- **question_generator.py**: Generates MCQs, short answer, and case study questions
- **alignment_matrix.py**: Builds comprehensive alignment matrix linking all components
- **export_utils.py**: Handles export to multiple file formats

#### Web Layer (web/)
- **index.html**: Complete web interface with forms and results display
- **app.js**: Frontend logic, API communication, dynamic content rendering

#### API Layer
- **app.py**: Flask server with RESTful endpoints, CORS support, request handling
- **main_system.py**: Alternative CLI interface for direct command-line usage
```

---

## 🔧 API Endpoints

### Health Check
```
GET /api/health
Response: {"status": "healthy", "timestamp": "..."}
```

### Process Course
```
POST /api/process
Body: {
  "title": "Course title",
  "description": "Course description",
  "scope": "Course scope",
  "duration": "Credit hours"
}
Response: {
  "topics": [...],
  "outcomes": {...},
  "assessments": [...],
  "questions": [...],
  "matrix": [...]
}
```

---

## 📈 Example Output

### Input
```
Title: Introduction to Machine Learning
Description: This course covers fundamental concepts in machine learning 
including supervised and unsupervised learning, neural networks, and 
model evaluation techniques.
```

### Generated Output
- **8 Topics** including "Supervised Learning", "Neural Networks", etc.
- **5 Course-level outcomes** across Bloom's levels
- **Assessment mix**: 10% pre-test, 20% quizzes, 25% midterm, 25% projects, 20% final
- **24 Questions**: 15 MCQs, 6 short answer, 3 case studies
- **Complete alignment matrix** with 40+ mappings

---
### Backend & NLP
- Flask API development
- NLP processing pipeline
- Topic extraction algorithms
- Learning outcomes generation

### Question Generation & Data
- Question template system
- Alignment matrix builder
- Export format handlers
- Data validation and QA

---

## 🔮 Future Enhancements

- [ ] Word and Excel export with formatting
- [ ] Multilingual support
- [ ] Custom Bloom's taxonomy configuration
- [ ] Question difficulty calibration
- [ ] Course template library
- [ ] User authentication and saved syllabi
- [ ] Advanced topic modeling (LDA, BERT)
- [ ] Integration with LMS platforms

---

