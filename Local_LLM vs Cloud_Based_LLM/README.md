# Local vs Cloud LLM Performance Comparison: Mathematical Reasoning Evaluation

## Overview
This research project aims to evaluate and compare the performance capabilities of local LLMs (using TinyLlama) against cloud-based LLMs (using GPT-4). The focus is on assessing mathematical reasoning abilities as a benchmark for comparing model performance.

## Research Motivation
The growing interest in deploying local LLMs versus using cloud-based solutions necessitates a thorough understanding of their comparative performance. This research provides quantitative metrics for evaluating the trade-offs between these approaches.

## Research Evolution

### Phase 1: Semantic Similarity Approach
Initially, we attempted to evaluate models through semantic comparison:
- Implemented keyword-based evaluation
- Used semantic similarity metrics
- Found limitations in this approach as:
  - Bad answers containing expected keywords scored well
  - Semantic similarity didn't correlate with answer quality
  - Required extensive manual verification

### Phase 2: Transition to Structured Evaluation
To address the limitations of semantic comparison:
- Shifted to mathematics MCQs from MMLU dataset
- Selected questions across difficulty levels
- Implemented quantitative evaluation metrics
- Source: [MMLU Dataset](https://huggingface.co/datasets/cais/mmlu/)

### Phase 3: Comprehensive Evaluation Framework
Developed a structured evaluation system using:
- 60 questions (15 each from 4 difficulty levels)
- Multiple evaluation metrics
- Automated scoring system

## Evaluation Methodology

### Question Categories
- Elementary Mathematics
- High School Mathematics
- College Mathematics
- Abstract Algebra

### Evaluation Metrics

1. **Correctness** (40%)
   - Primary measure of answer accuracy
   - Binary scoring for MCQ responses

2. **Mathematical Reasoning** (25%)
   - Depth of mathematical understanding
   - Problem-solving approach assessment
   - Use of mathematical concepts

3. **Solution Completeness** (15%)
   - Step-by-step solution presence
   - Logical progression
   - Completeness of explanation

4. **Explanation Quality** (10%)
   - Clarity of presentation
   - Mathematical vocabulary usage
   - Coherence of explanation

5. **Coherence** (5%)
   - Solution structure
   - Logical flow
   - Presentation consistency

6. **Time Efficiency** (5%)
   - Response generation speed
   - Processing efficiency

## Implementation

### Key Components
- Azure OpenAI integration for GPT-4 access
- Local Ollama setup for TinyLlama deployment
- Custom evaluation pipeline for automated assessment
- Interactive dashboard for result visualization

### Performance Visualization
- Implemented comprehensive dashboards using Streamlit
- Multiple visualization types:
  - Radar charts for metric comparison
  - Bar charts for subject-wise performance
  - Detailed metric tables

## Results

### Overall Performance
- GPT-4 Average Score: 0.68
- TinyLlama Average Score: 0.18

### Subject-wise Performance
1. Abstract Algebra
   - GPT-4: 0.65
   - TinyLlama: 0.10

2. College Mathematics
   - GPT-4: 0.74
   - TinyLlama: 0.18

3. Elementary Mathematics
   - GPT-4: 0.59
   - TinyLlama: 0.19

4. High School Mathematics
   - GPT-4: 0.76
   - TinyLlama: 0.26

## Limitations and Future Work

### Current Limitations
- Evaluation limited to multiple-choice questions
- Fixed answer format constraints
- Limited to specific mathematical domains

### Future Research Directions
1. Expansion to subjective mathematical questions
2. Development of more sophisticated evaluation metrics
3. Integration of symbolic mathematics evaluation
4. Analysis of step-by-step solution quality
5. Investigation of mathematical reasoning patterns

## Setup and Usage

### Prerequisites
```
- Python 3.8+
- Azure OpenAI API access
- Ollama installation
- Required Python packages (requirements.txt)
```

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
1. Create a `.env` file with:
```
API_KEY=your_azure_openai_key
AZURE_ENDPOINT=your_azure_endpoint
DEPLOYMENT_NAME=your_deployment_name
API_VERSION=your_api_version
```

2. Install Ollama and download TinyLlama:
```bash
ollama pull tinyllama
```

### Running the Evaluation
```bash
python run.py
```

### Viewing Results
```bash
streamlit run ui_comparison.py
```

## License
MIT License

## Acknowledgments
- MMLU Dataset creators
- Azure OpenAI team
- Ollama community