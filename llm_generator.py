"""
Module for generating presentation content using OpenRouter.ai LLM models.
"""
import json
import requests
from typing import Dict, List, Optional

class LLMGenerator:
    """Handles generation of presentation content using various LLM models through OpenRouter.ai"""
    
    # Available models on OpenRouter.ai
    MODELS = {
        "gpt4": "openai/gpt-4",
        "claude3": "anthropic/claude-3-sonnet:beta"
    }
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize with config file containing API key"""
        with open(config_path, 'r') as f:
            config = json.load(f)
            self.api_key = config["openrouter_api_key"]
        
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_presentation(self, prompt: str, model: str = "claude3") -> Dict:
        """
        Generate a complete presentation from a prompt using specified model.
        
        Args:
            prompt: User's presentation prompt
            model: Model identifier (default: gpt4)
            
        Returns:
            Dict containing generated slides in our JSON format
        """
        if model not in self.MODELS:
            raise ValueError(f"Invalid model. Choose from: {', '.join(self.MODELS.keys())}")
            
        # Enhance prompt with our specific requirements
        enhanced_prompt = f"""
        Create a presentation based on this prompt: {prompt}
        
        Requirements:
        - Generate 100-150 words of text per slide
        - For each slide, try to generate an image prompt that captures the slide's essence
        - If you can't think of a good image prompt for a slide, skip it
        - Format the response as a JSON object with a 'slides' array
        - Each slide should have:
          - 'format': either 'CENTERED_TEXT_ONLY' or 'IMAGE_AND_TEXT_SIDE_BY_SIDE'
          - 'text': the slide text
          - 'image_prompt': (optional) prompt for generating an image
        
        Example format:
        {{
            "slides": [
                {{
                    "format": "CENTERED_TEXT_ONLY",
                    "text": "The Impact of Drones on Modern Warfare"
                }},
                {{
                    "format": "IMAGE_AND_TEXT_SIDE_BY_SIDE",
                    "text": "Drones have revolutionized reconnaissance...",
                    "image_prompt": "A military drone flying over a battlefield at sunset, painted in the style of a classical oil painting"
                }}
            ]
        }}
        """
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json={
                "model": self.MODELS[model],
                "messages": [{"role": "user", "content": enhanced_prompt}]
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.text}")
            
        try:
            raw_content = response.json()["choices"][0]["message"]["content"]
            print("\nRaw LLM response:")
            print(raw_content)
            
            # Extract just the JSON part (ignore any preamble text)
            import re
            json_match = re.search(r'({[\s\S]*})', raw_content)
            if not json_match:
                raise Exception("No JSON object found in response")
                
            content = json_match.group(1)
            
            # Clean up the JSON structure
            def clean_json(text):
                # Convert the text into a Python structure first
                slides = []
                current_slide = {}
                
                # Extract slide data using simpler patterns
                for line in text.split('\n'):
                    line = line.strip()
                    if '"format"' in line:
                        if current_slide:
                            slides.append(current_slide)
                        current_slide = {}
                        format_match = re.search(r'"format":\s*"([^"]*)"', line)
                        if format_match:
                            current_slide['format'] = format_match.group(1)
                    elif '"text"' in line:
                        text_match = re.search(r'"text":\s*"([^"]*)"', line)
                        if text_match:
                            current_slide['text'] = text_match.group(1)
                    elif '"image_prompt"' in line:
                        prompt_match = re.search(r'"image_prompt":\s*"([^"]*)"', line)
                        if prompt_match:
                            current_slide['image_prompt'] = prompt_match.group(1)
                
                if current_slide:
                    slides.append(current_slide)
                
                # Convert back to properly formatted JSON
                return json.dumps({"slides": slides})
            
            content = clean_json(content)
            
            try:
                parsed = json.loads(content)
                print("\nParsed JSON structure:")
                print(json.dumps(parsed, indent=2))
                return parsed
            except json.JSONDecodeError as e:
                print(f"\nJSON parsing error at position {e.pos}:")
                print(content[max(0, e.pos-50):min(len(content), e.pos+50)])
                print(" " * (min(50, e.pos)) + "^")
                raise
        except (KeyError, json.JSONDecodeError) as e:
            raise Exception(f"Failed to parse LLM response: {str(e)}")

    def compare_models(self, prompt: str) -> Dict[str, Dict]:
        """
        Generate presentations using all available models for comparison.
        
        Args:
            prompt: User's presentation prompt
            
        Returns:
            Dict mapping model names to their generated presentations
        """
        results = {}
        for model in self.MODELS:
            try:
                results[model] = self.generate_presentation(prompt, model)
            except Exception as e:
                results[model] = {"error": str(e)}
        return results

def main():
    """Example usage"""
    generator = LLMGenerator()
    
    # Example prompt
    prompt = "Create a 10-15 slide presentation about the impact of drones on warfare. Write it in the voice of Carl Von Clausewitz. The pictures should look like oil paintings."
    
    try:
        # Compare all available models
        results = generator.compare_models(prompt)
        for model, result in results.items():
            print(f"\nResults from {model}:")
            print(json.dumps(result, indent=2))
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
