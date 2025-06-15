# SageScope - Cross-domain Research Assistant

SageScope is an AI-powered research assistant that helps you gather and analyze information from multiple domains including academia, news, science, and history. It uses Gemini Pro for intelligent summarization and multiple search APIs for comprehensive research.

## Features

- 🔍 Multi-source search (Tavily, arXiv, Google Scholar, Wikipedia, PubMed)
- 📝 AI-powered content summarization using Gemini Pro
- 📊 Structured research reports with key points
- 💾 Save reports in Markdown format
- 🎯 Cross-domain research capabilities

## Setup

1. Clone the repository:
```bash
git clone https://github.com/aswego123/Sagescope_crossdomain_researchagent.git
cd sagescope
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Usage

Run the research assistant from the command line:

```bash
python main.py "your research query" [options]
```

### Options

- `--max-results`: Maximum number of results per source (default: 5)
- `--output`: Output format (choices: console, file, both; default: both)

### Examples

```bash
# Basic usage
python main.py "AI in Agriculture"

# With custom options
python main.py "Quantum Computing" --max-results 3 --output file
```

## Output

The research report includes:
- Source information
- AI-generated summaries
- Key points extracted from each source
- Links to original content

Reports are saved in the `reports` directory with timestamps.

## Project Structure

```
sagescope/
├── main.py           # CLI interface
├── gemini_api.py     # Gemini Pro API wrapper
├── web_search.py     # Multi-source search functionality
├── summarizer.py     # Content extraction and summarization
├── requirements.txt  # Project dependencies
└── reports/         # Generated research reports
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
