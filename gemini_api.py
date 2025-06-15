import os
import google.generativeai as genai
from typing import List, Dict, Optional
import time
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiAPI:
    def __init__(self):
        # Load environment variables
        load_dotenv(override=True)
        
        # Debug: Print all environment variables (excluding sensitive values)
        logger.info("Checking environment variables...")
        env_vars = {k: v for k, v in os.environ.items() if 'KEY' not in k}
        logger.info(f"Available environment variables: {list(env_vars.keys())}")
        
        # Get API key with detailed error handling
        api_key = os.getenv("GEMINI_API_KEY")
        logger.info(f"GEMINI_API_KEY found: {'Yes' if api_key else 'No'}")
        
        if not api_key:
            # Try alternative environment variable names
            alternative_keys = ["GOOGLE_API_KEY", "GEMINI_KEY", "GOOGLE_GEMINI_API_KEY"]
            for key in alternative_keys:
                api_key = os.getenv(key)
                if api_key:
                    logger.info(f"Found API key in {key}")
                    break
        
        if not api_key:
            # Provide more detailed error message
            error_msg = """
            GEMINI_API_KEY not found. Please ensure:
            1. You have created a .env file in the project root
            2. The .env file contains: GEMINI_API_KEY=your_actual_key_here
            3. There are no spaces around the = sign
            4. The API key is valid and active
            5. The .env file is properly formatted (no quotes around values)
            
            You can get a Gemini API key from:
            https://makersuite.google.com/app/apikey
            """
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Successfully initialized Gemini API")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini API: {str(e)}")
            raise
        
    def generate_summary(self, content: str, max_retries: int = 3) -> str:
        """Generate a summary using Gemini Pro with retry logic."""
        prompt = """You are a helpful research assistant. Given the following content, 
        generate a concise bullet-point summary. Highlight important stats, findings, and ideas. 
        Format clearly with markdown bullet points.
        
        Content:
        {content}
        """
        
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt.format(content=content))
                return response.text
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise Exception(f"Failed to generate summary after {max_retries} attempts: {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff
    
    def extract_key_points(self, content: str) -> List[str]:
        """Extract key points from content using Gemini Pro."""
        prompt = """Extract the 5 most important key points from the following content.
        Format each point as a separate bullet point.
        
        Content:
        {content}
        """
        
        try:
            response = self.model.generate_content(prompt.format(content=content))
            return [point.strip() for point in response.text.split('\n') if point.strip()]
        except Exception as e:
            logger.error(f"Failed to extract key points: {str(e)}")
            raise Exception(f"Failed to extract key points: {str(e)}")
    
    def analyze_domain(self, content: str, domain: str) -> Dict[str, str]:
        """Analyze content from a specific domain (academic, news, tech, etc.)."""
        prompt = """Analyze the following content from a {domain} perspective.
        Provide:
        1. Main findings
        2. Methodology (if applicable)
        3. Key implications
        4. Limitations (if any)
        
        Content:
        {content}
        """
        
        try:
            response = self.model.generate_content(prompt.format(domain=domain, content=content))
            return {
                "analysis": response.text,
                "domain": domain
            }
        except Exception as e:
            logger.error(f"Failed to analyze domain: {str(e)}")
            raise Exception(f"Failed to analyze domain: {str(e)}") 