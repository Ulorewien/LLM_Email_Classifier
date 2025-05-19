# LLM-Powered Email Classification and Response System

This project demonstrates a complete pipeline for **classifying and responding to emails using Large Language Models (LLMs)**. The system automates customer support workflows by analyzing incoming emails, classifying them into categories, and generating appropriate responses.

---

## Features

- Email classification using LLaMA 3.2 3B (quantized)
- Prompt-driven response generation
- Input validation and error handling
- Modular design for easy extensibility
- Custom YAML and JSON configuration for prompts and models
- End-to-end demonstration on sample email dataset

---

## Project Structure

```
.
├── .env                          # Hugging Face token (excluded from version control)
├── config.yaml                   # YAML config for model and prompt settings
├── email_classifier_template.py  # Base Python script (template)
├── llm_email_classifier.ipynb    # Colab notebook version of the pipeline
├── prompts.json                  # Prompt templates for classification & response generation
├── requirements.txt              # Required Python dependencies
├── utils.py                      # Utility functions for validation, etc.
```
---

## Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/Ulorewien/LLM_Email_Classifier.git
cd LLM_Email_Classifier
```

2. **Set up your Python environment**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Add your Hugging Face API token**
Create a .env file in the project root:
```ini
HF_TOKEN=your_huggingface_token_here
```

---

## Sample Outputs
**Complaint**
"We apologize... We have created an urgent ticket... Expect a refund within 48 hours..."

**Inquiry**
"Our premium package is compatible with Mac OS... Please find the specifications here..."

**Feedback**
"Thank you for your kind words... We're thrilled to hear about your positive experience..."

**Support Request**
"We've created a support ticket... Please update the software and try reinstalling..."

**Other (Partnership)**
"We're excited to explore a partnership... How about a call on Wednesday at 2 PM EST?"