# Azure OpenAI Chat Application

This Streamlit-based web application integrates with Azure OpenAI to provide a conversational interface. Users can enter their queries, and the app interacts with Azure OpenAI's API to generate responses.

---

## Features
- **Interactive Chat Interface**: Users can input queries via a text area.
- **Azure OpenAI Integration**: Leverages Azure OpenAI's `chat/completions` endpoint to process prompts and generate responses.
- **Customizable Design**: Includes a styled **Submit** button with hover effects using CSS.

---

## Prerequisites
1. **Azure OpenAI Account**: Set up an Azure OpenAI service instance.
2. **API Key**: Obtain your API key from the Azure portal.
3. **Endpoint Information**: Note your Azure OpenAI endpoint, deployment name, and API version.
4. **Python Environment**: Ensure Python 3.7+ is installed.

---

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dependencies
Install the required Python libraries:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root and add the following:
```
API_KEY=<your_azure_openai_api_key>
AZURE_ENDPOINT=<your_azure_openai_endpoint>
DEPLOYMENT_NAME=<your_deployment_name>
API_VERSION=<api_version>
```

### 4. Run the Application
Start the Streamlit server:
```bash
streamlit run app.py
```

---

## Usage
1. Open the application in your browser (default: `http://localhost:8501`).
2. Enter a query in the text area.
3. Click the **Submit** button to get a response from Azure OpenAI.

---

## Project Structure
```
.
├── app.py               # Main Streamlit application
├── .env                 # Environment variables file
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## Key Highlights in Code
- **Custom Button Styling**: 
  CSS styling ensures a visually appealing and interactive Submit button.
- **Error Handling**: 
  Displays detailed error messages in case of API failures, including the API URL.
- **Environment Variables**: 
  Sensitive data like API keys and endpoints are secured using `.env`.

---

## Example Output
1. **Input**: `"What is the capital of France?"`
2. **Output**: `"The capital of France is Paris."`

---

## Troubleshooting
1. **Invalid API Key or Endpoint**: Verify the details in your `.env` file.
2. **Network Errors**: Ensure the Azure OpenAI service is accessible from your machine.
3. **Streamlit Errors**: Check if all dependencies are installed correctly.

---

## Future Improvements
- Add user authentication for security.
- Support additional Azure OpenAI features like embeddings or completions.
- Implement chat history to store past conversations.

---

## License
This project is licensed under the [MIT License](LICENSE).

--- 

## Contributions
Contributions are welcome! Feel free to open issues or submit pull requests for improvements.
