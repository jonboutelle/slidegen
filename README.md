# Slidegen

A Python-based PowerPoint presentation generator that creates slides from JSON input files using predefined templates and formats.

## Features

- Generate PowerPoint presentations from JSON configuration
- Support for multiple slide formats:
  - Image and text side by side
  - Centered text only
- Template-based generation
- Customizable slide layouts

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
