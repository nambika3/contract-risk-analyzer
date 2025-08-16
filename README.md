# Contract Risk Analyzer

Contract Risk Analyzer is a Streamlit-based web application that uses AI to identify potential risks in legal contracts. It supports PDF and DOCX uploads and provides detailed risk assessments across legal, security, privacy, and liability domains.

## Features

- Upload and analyze contracts in `.pdf` or `.docx` formats.
- Detect and categorize risks:
  - Legal risks
  - Security vulnerabilities
  - Privacy and data protection issues
  - Liability clauses
  - Unfair terms
  - Missing protections
- Redacts basic Personally Identifiable Information (PII) before analysis.
- Utilizes OpenRouter and Anthropic Claude for language model processing.
- User-friendly Streamlit interface with privacy consent built in.

## How It Works

1. Upload a contract file.
2. The file is read and split into smaller text chunks.
3. Basic PII (names, emails, phone numbers, etc.) is redacted.
4. Each chunk is sent to Claude via OpenRouter API for analysis.
5. Results are displayed section by section in a structured format.

## Requirements

- Python 3.8+
- pip
- API key from [OpenRouter.ai](https://openrouter.ai/)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/contract-risk-analyzer.git
   cd contrac
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
   
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
5. Add your API key in a `.env` file:
   ```bash
   pip install -r requirements.txt
   ```
   
7. Run the app:
   ```bash
   streamlit run app.py
   ```

## Privacy Notice

- No documents are stored on disk.
- Only extracted text (after redacting PII) is sent to the external API.
- Users must explicitly consent before analysis begins.
- Do not upload contracts containing passwords, trade secrets, or sensitive PII.

## File Structure

```bash
contract-risk-analyzer/
├── app.py                # Main Streamlit app
├── requirements.txt      # Python dependencies
├── .gitignore            # Git ignore file
├── .env                  # API key (excluded from Git)
└── README.md             # Project documentation
```

## License

This project is open source and available under the MIT License.

## Author
Ambika Narayanan


