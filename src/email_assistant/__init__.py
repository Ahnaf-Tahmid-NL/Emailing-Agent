import os
import streamlit as st

from dotenv import load_dotenv
from google import genai
from email_assistant.email import send_email

load_dotenv()  # Loads variables from .env
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def emailing_tool(email_content: str, email_address: str, email_subject: str):
    """Send an email via Gmail SMTP.
    Args:
        email_content (str): The content of the email.
        email_address (str): The recipient's email address.
        email_subject (str): The subject of the email.
    Returns:
        Nothing. The function sends an email and does not return any value.
    Raises:
        Exception: If sending the email fails.
    """
    try:
        send_email(email_content, email_address, email_subject)
        return "SUCCESS: Email was sent successfully."
    except Exception as e:
        return f"FAILED: Email could not be sent. Error: {e}"

def main():
    st.set_page_config(
        page_title="AI Email Assistant",
        page_icon="✉️",
        layout="centered"
    )

    st.title("AI Email Assistant")
    st.markdown("Write a professional email with the power of AI!")

    email_address = st.text_input(
        "Enter the receiver's email address",
        key="receive_email_address"
    ).strip()

    email_subject = st.text_input(
        "Enter the email subject (optional)",
        key="email_subject"
    ).strip()

    email_content = st.text_area(
        "Enter the email content",
        key="email_content"
    ).strip()

    send = st.button("Send Email")

    if send:
        if not email_content or not email_address:
            st.warning(
                "Please provide both the email content and "
                "the receiver's email address."
            )
            st.stop()

        subject_instruction = (
            f"Use this subject: {email_subject}"
            if email_subject
            else "Generate a suitable subject based on the email content."
        )

        prompt = f"""
        You are a professional email writer.

        Improve the user's email while preserving its original meaning.

        Focus on:
        1. Content clarity
        2. Professional tone
        3. Grammar
        4. Structure

        Original email:
        {email_content}

        Recipient email address:
        {email_address}

        Subject instruction:
        {subject_instruction}

        After improving the email, use the emailing tool to send it.

        IMPORTANT:
        - Send the email to the exact recipient email address provided.
        - Do not modify the recipient's email address.
        - Use the generated/improved email content.
        - Use the provided subject if one was given.
        - If no subject was provided, generate an appropriate subject.
        - Only report success after the email has actually been sent.
        """

        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=1000,
                    tools=[emailing_tool]
                ),
            )

            st.markdown(response.text)

        except Exception as e:
            st.error(f"An error occurred while sending the email: {e}")


if __name__ == "__main__":
    main()