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

## Tech Stack

- **Model**: [meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama)
- **Transformer Library**: `transformers`
- **Quantization**: 4-bit (NF4) with `bitsandbytes`
- **Configuration**: `yaml`, `json`, `.env`
- **Email Logic**: Python, `pandas`, `logging`
- **Runtime**: Google Colab (due to GPU constraints)

---

## Project Structure

```
.
├── config.yaml              # Model and prompt configuration
├── prompts.json             # Prompt templates for classification & generation
├── main.py                  # Main script for processing emails
├── utils.py                 # Input validation and helper functions
├── .env                     # Hugging Face token (excluded from version control)
├── README.md                # Project documentation
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

