import io
import openai
from PyPDF2 import PdfReader

class ResumeExtractionAgent:
    """
    This agent is responsible for extracting relevant information (skills) from the user's resume.
    We dynamically extract skills by calling Azure OpenAI (GPT) for a more robust method.
    """

    def __init__(self, deployment_name=None):
        """
        :param deployment_name: Name of your Azure GPT-4 (or other model) deployment.
        """
        self.deployment_name = deployment_name or "gpt-4o"  # fallback

    def extract_skills(self, resume_bytes: bytes) -> list:
        """
        Extracts relevant skills by parsing the PDF and calling Azure GPT.
        Returns a list of extracted skills (strings).
        """
        # 1. Parse PDF content
        resume_text = self._parse_pdf(resume_bytes)

        # 2. Dynamically extract skills using GPT
        extracted_skills = self._extract_skills_from_gpt(resume_text)
        return extracted_skills

    def _parse_pdf(self, resume_bytes: bytes) -> str:
        """
        Reads PDF bytes and returns the text content.
        """
        pdf_reader = PdfReader(io.BytesIO(resume_bytes))
        text_content = []
        for page in pdf_reader.pages:
            text_content.append(page.extract_text() or "")
        return "\n".join(text_content)

    def _extract_skills_from_gpt(self, resume_text: str) -> list:
        """
        Makes a call to Azure GPT to identify relevant skills.
        Returns a list of unique skills.
        """
        try:
            # Adjust system/user messages to your liking.
            response = openai.ChatCompletion.create(
                engine=self.deployment_name,  # Your Azure GPT-4 deployment name
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful assistant that extracts professional and technical skills from text. "
                            "Return only a bullet-point list of the unique skills mentioned, with no additional commentary."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Here is some resume text:\n\n{resume_text}\n\n"
                            "Extract a list of relevant technical and professional skills from the above text."
                        )
                    }
                ],
                temperature=0.0,
                max_tokens=300
            )
            raw_output = response["choices"][0]["message"]["content"]
            # Example GPT output might be:
            # "- Python\n- Machine Learning\n- SQL\n- Cloud Computing\n- ..."

            # Parse each line, stripping away bullet points and whitespace
            lines = raw_output.strip().split("\n")
            skills = []
            for line in lines:
                cleaned_line = line.strip("-•* \t").strip()
                if cleaned_line:
                    skills.append(cleaned_line)

            # Remove duplicates (optionally convert to lowercase)
            unique_skills = list(set(skills))
            return unique_skills

        except Exception as e:
            print(f"OpenAI GPT skill extraction error: {e}")
            return []
