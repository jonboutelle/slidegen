"""
Main script that connects all components of the presentation generator
"""
import json
import os
from llm_generator import LLMGenerator
from image_generator import ImageGenerator
from slidegen import PresentationGenerator

def main():
    try:
        # Example prompt (we'll make this a command line arg later)
        prompt = """Create a detailed 10-15 slide presentation about the impact of drones on warfare. Write it in the voice of Carl Von Clausewitz. Structure it as follows:

1. Introduction (1-2 slides)
2. Historical Context and Evolution (2-3 slides)
3. Current Capabilities and Impact (3-4 slides)
4. Strategic Implications (2-3 slides)
5. Future Considerations (1-2 slides)
6. Conclusion (1 slide)

Make each slide detailed with 100-150 words of text. The pictures should be in the style of dramatic oil paintings, focusing on the technological and strategic aspects of drone warfare."""
        
        print("\n1. Generating presentation content from prompt...")
        llm = LLMGenerator()
        content = llm.generate_presentation(prompt)
        print("Content generated:")
        print(json.dumps(content, indent=2))
        
        print("\n2. Generating images for slides...")
        image_gen = ImageGenerator()
        
        # Process each slide that has an image prompt
        for i, slide in enumerate(content['slides']):
            if 'image_prompt' in slide:
                print(f"\nProcessing image {i+1}...")
                image_path = image_gen.generate_image(slide['image_prompt'])
                print(f"Image saved to: {image_path}")
                # Update the slide with the generated image path
                slide['image'] = image_path
        
        print("\nFinal content structure:")
        print(json.dumps(content, indent=2))
        
        print("\n3. Generating PowerPoint presentation...")
        if not os.path.exists("template.pptx"):
            raise FileNotFoundError("template.pptx not found in current directory")
            
        pptx_gen = PresentationGenerator("template.pptx")
        
        # Save the content to a temporary JSON file
        temp_json = "temp_presentation.json"
        print(f"\nSaving content to {temp_json}...")
        with open(temp_json, 'w') as f:
            json.dump(content, f, indent=2)
        
        if not os.path.exists(temp_json):
            raise FileNotFoundError(f"Failed to create {temp_json}")
            
        # Generate the presentation from the JSON file
        output_path = "output.pptx"
        print(f"\nGenerating {output_path}...")
        pptx_gen.generate_from_json(temp_json, output_path)
        
        if not os.path.exists(output_path):
            raise FileNotFoundError(f"Failed to create {output_path}")
            
        print(f"\nPresentation generated successfully: {output_path}")
        print(f"File size: {os.path.getsize(output_path)} bytes")
        
        # Clean up temporary file
        os.remove(temp_json)
        print("Temporary files cleaned up")
        
    except Exception as e:
        print(f"\nError during execution:")
        import traceback
        print(traceback.format_exc())
        raise

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {str(e)}")
