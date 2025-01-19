# Slidegen
This software generates full presentations in PPTX format from text prompts. 

1)COLLECT PRESENTATION PROMPT FROM USER
A user starts out with a prompt to generation a presentation. Like "make a 10 page presentation about the impact of drones on warfare. Write it in the voice of Carl Von Clausewitz. The pictures should look like oil paintings." could be prompt. 

2)GENERATE PRESENTATION TEXT AND IMAGE PROMPTS
We will send the prompt to an LLM, that will use the prompt to generate a JSON file that has 1)text for each slide, and 2)an image prompt for every slide.
We will append our instructions to the prompt. "Try to generate an image prompt for each slide. But if you can't come up with something good just don't include it. For the text please generate less than 50 words of text per slide."
TODO: DECIDE WHICH LLM TO USE (MAYBE TRY MULTIPLE IN PARALLEL TO START)
TODO: EXTERNALIZE CREDENTIALS TO A FILE THAT WE DO NOT CHECK INTO SOURCE CONTROL (WE'LL USE OPENROUTER.AI FOR LLM AND IMAGE MODEL ACCESS)

3)GENERATE IMAGES FROM IMAGE PROMPTS
We will send each image prompt to an image model and save the resulting image to file. We'll save the path of each image in the JSON, at the appropriate slide.
TODO: DECIDE WHICH IMAGE MODEL TO USE (MAYBE TRY MULTIPLE IN PARALLEL TO START)

4) GENERATE PPTX FROM IMAGES AND TEXT 
We will generate a PPTX file from the text and images in the JSON file, using the python-pptx libary and the template.pptx file. (THIS PART IS ALREADY DONE)


A Python-based PowerPoint presentation generator that creates slides from user prompts. JSON input files using predefined templates and formats.


## Requirements

- Python 3.x
- python-pptx

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd slidegen
```

2. Install dependencies:
```bash
pip install python-pptx
```

## Usage

1. Prepare your JSON configuration file (see example.json for format):
```json
{
  "slides": [
    {
      "format": "CENTERED_TEXT_ONLY",
      "text": "Your slide text here"
    },
    {
      "format": "IMAGE_AND_TEXT_SIDE_BY_SIDE",
      "text": "Your slide text here",
      "image": "path/to/image.jpg"
    }
  ]
}
```

2. Ensure you have a PowerPoint template file named `template.pptx` in your project directory.

3. Run the script:
```bash
python slidegen.py
```

The script will generate an `output.pptx` file based on your JSON configuration.

## Slide Formats

### CENTERED_TEXT_ONLY
- Uses slide layout 1 (Title Slide)
- Text is placed in the title placeholder
- Best for section headers or emphasis slides

### IMAGE_AND_TEXT_SIDE_BY_SIDE
- Uses slide layout 8 (Picture with Caption)
- Text is placed in the title placeholder
- Image is placed in the picture placeholder
- Best for slides with visual content and accompanying text

## Project Structure

- `slidegen.py`: Main script for presentation generation
- `template.pptx`: PowerPoint template file
- `example.json`: Example configuration file

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
