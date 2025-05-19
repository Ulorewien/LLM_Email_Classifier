# Configuration and imports
import os
import yaml
import json
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
from datetime import datetime
import logging
from huggingface_hub.hf_api import HfFolder
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TextGenerationPipeline
from utils import email_data_validation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
hf_token = os.getenv("HF_TOKEN")
HfFolder.save_token(hf_token)

# Set the quantization configuration for LLaMA
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype="float16"
)

# Load the config and the prompts
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

with open("prompts.json", "r") as f:
    prompts = json.load(f)
    
email_classification_prompt = prompts["email_classification"][config["email_prompt"]]
response_generation_prompt = prompts["reponse_generation"][config["generation_prompt"]]

# Sample email dataset
sample_emails = [
    {
        "id": "001",
        "from": "angry.customer@example.com",
        "subject": "Broken product received",
        "body": "I received my order #12345 yesterday but it arrived completely damaged. This is unacceptable and I demand a refund immediately. This is the worst customer service I've experienced.",
        "timestamp": "2024-03-15T10:30:00Z"
    },
    {
        "id": "002",
        "from": "curious.shopper@example.com",
        "subject": "Question about product specifications",
        "body": "Hi, I'm interested in buying your premium package but I couldn't find information about whether it's compatible with Mac OS. Could you please clarify this? Thanks!",
        "timestamp": "2024-03-15T11:45:00Z"
    },
    {
        "id": "003",
        "from": "happy.user@example.com",
        "subject": "Amazing customer support",
        "body": "I just wanted to say thank you for the excellent support I received from Sarah on your team. She went above and beyond to help resolve my issue. Keep up the great work!",
        "timestamp": "2024-03-15T13:15:00Z"
    },
    {
        "id": "004",
        "from": "tech.user@example.com",
        "subject": "Need help with installation",
        "body": "I've been trying to install the software for the past hour but keep getting error code 5123. I've already tried restarting my computer and clearing the cache. Please help!",
        "timestamp": "2024-03-15T14:20:00Z"
    },
    {
        "id": "005",
        "from": "business.client@example.com",
        "subject": "Partnership opportunity",
        "body": "Our company is interested in exploring potential partnership opportunities with your organization. Would it be possible to schedule a call next week to discuss this further?",
        "timestamp": "2024-03-15T15:00:00Z"
    }
]


class EmailProcessor:
    def __init__(self):
        """Initialize the email processor with LLM API key."""
        
        model_name = config["llm_model"]
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config)
        self.pipeline = TextGenerationPipeline(model=self.model, tokenizer=self.tokenizer)

        # Define valid categories
        self.valid_categories = {
            "complaint", "inquiry", "feedback",
            "support_request", "other"
        }

    def classify_email(self, email: Dict) -> Optional[str]:
        """
        Classify an email using LLM.
        Returns the classification category or None if classification fails.
        """
        
        system_prompt = email_classification_prompt
        user_prompt = f"Subject: {email['subject']}, Body: {email['body']}"
        
        prompt = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
        
        try:
            response = self.pipeline(prompt, max_new_tokens=20)[0]["generated_text"]
            predicted_category = response[-1]["content"]
            
            if predicted_category in self.valid_categories:
                return predicted_category
            
            return "other"
        
        except Exception as e:
            logger.error(f"Classification failed for email {email['id']}: {e}")
            return None

    def generate_response(self, email: Dict, classification: str) -> Optional[str]:
        """
        Generate an automated response based on email classification.
        """
        
        system_prompt = response_generation_prompt
        
        user_prompt = f"Subject: {email['subject']}, Body: {email['body']}, Category: {classification}"
        
        prompt = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
        
        try:
            response = self.pipeline(prompt, max_new_tokens=200)[0]["generated_text"]
            generated_response = response[-1]["content"]
            print(generated_response)
            return generated_response
        
        except Exception as e:
            logger.error(f"Response generation failed for email {email['id']}: {e}")
            return None


class EmailAutomationSystem:
    def __init__(self, processor: EmailProcessor):
        """Initialize the automation system with an EmailProcessor."""
        self.processor = processor
        self.response_handlers = {
            "complaint": self._handle_complaint,
            "inquiry": self._handle_inquiry,
            "feedback": self._handle_feedback,
            "support_request": self._handle_support_request,
            "other": self._handle_other
        }

    def process_email(self, email: Dict) -> Dict:
        """
        Process a single email through the complete pipeline.
        Returns a dictionary with the processing results.
        """
        
        try:
            classification = self.processor.classify_email(email)
            
            if not classification:
                raise ValueError(f"Failed to classify email {email['id']}")
            
            handler = self.response_handlers.get(classification, self._handle_other)
            
            response = self.processor.generate_response(email, classification)
            if not response:
                raise ValueError(f"Failed to generate response for email {email['id']}")
            
            if classification == "complaint":
                send_complaint_response(email["from"], response)
            else:
                send_standard_response(email["from"], response)
            
            handler(email)
            
            results = {
                "id": email["id"],
                "email_id": email["from"], 
                "success": True, 
                "classification": classification, 
                "response_sent": response
            }
        
        except Exception as e:
            results = {
                "id": email["id"],
                "email_id": email["from"], 
                "success": False, 
                "classification": None, 
                "response_sent": None
            }
        
        return results

    def _handle_complaint(self, email: Dict):
        """
        Handle complaint emails.
        """
        create_urgent_ticket(email["from"], "complaint", email["body"])

    def _handle_inquiry(self, email: Dict):
        """
        Handle inquiry emails.
        """
        create_support_ticket(email["from"], email["body"])

    def _handle_feedback(self, email: Dict):
        """
        Handle feedback emails.
        """
        log_customer_feedback(email["from"], email["body"])

    def _handle_support_request(self, email: Dict):
        """
        Handle support request emails.
        """
        create_support_ticket(email["from"], email["body"])

    def _handle_other(self, email: Dict):
        """
        Handle other category emails.
        """
        logger.info(f"Handled email {email['id']}")

# Mock service functions
def send_complaint_response(email_id: str, response: str):
    """Mock function to simulate sending a response to a complaint"""
    logger.info(f"Sending complaint response for email {email_id}")
    # In real implementation: integrate with email service


def send_standard_response(email_id: str, response: str):
    """Mock function to simulate sending a standard response"""
    logger.info(f"Sending standard response for email {email_id}")
    # In real implementation: integrate with email service


def create_urgent_ticket(email_id: str, category: str, context: str):
    """Mock function to simulate creating an urgent ticket"""
    logger.info(f"Creating urgent ticket for email {email_id}")
    # In real implementation: integrate with ticket system


def create_support_ticket(email_id: str, context: str):
    """Mock function to simulate creating a support ticket"""
    logger.info(f"Creating support ticket for email {email_id}")
    # In real implementation: integrate with ticket system


def log_customer_feedback(email_id: str, feedback: str):
    """Mock function to simulate logging customer feedback"""
    logger.info(f"Logging feedback for email {email_id}")
    # In real implementation: integrate with feedback system


def run_demonstration():
    """Run a demonstration of the complete system."""
    # Initialize the system
    processor = EmailProcessor()
    automation_system = EmailAutomationSystem(processor)

    # Process all sample emails
    results = []
    for email in sample_emails:
        logger.info(f"\nValidating input data for email {email['id']}...")
        if not email_data_validation(email):
            raise ValueError("Given data has some missing fields!")
        logger.info(f"\nProcessing email {email['id']}...")
        result = automation_system.process_email(email)
        results.append(result)

    # Create a summary DataFrame
    df = pd.DataFrame(results)
    print("\nProcessing Summary:")
    print(df[["id", "email_id", "success", "classification", "response_sent"]])

    return df


# Example usage:
if __name__ == "__main__":
    results_df = run_demonstration()
