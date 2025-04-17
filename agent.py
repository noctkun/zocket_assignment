import os
import autogen
from autogen import AssistantAgent, UserProxyAgent
import logging


def get_gemini_config(api_key: str):
    """Creates the configuration list for the Gemini LLM."""
    if not api_key:
        raise ValueError("Gemini API Key is required.")
    return [{
        "model": "gemini-1.5-pro",
        "api_key": api_key,
        "api_type": "google"
    }]

def summarize_with_agent(context: str, gemini_api_key: str) -> str:
    """
    Uses an AutoGen agent powered by Gemini to summarize the provided text.

    Args:
        context: The text content to be summarized.
        gemini_api_key: The API key for Google Gemini.

    Returns:
        The generated summary string or an error message.
    """
    if not context or not context.strip():
        return "Error: No content provided to summarize."
    print("--- Entering summarize_with_agent ---")
    try:
        config_list = get_gemini_config(gemini_api_key)

        assistant = AssistantAgent(
            name="SummarizerAgent",
            llm_config={"config_list": config_list},
            system_message=(
                "You are an expert AI assistant specialized in summarizing web content. "
                "Analyze the provided text, identify the key information and main points. "
                "Generate a concise and clear summary of the text. "
                "Your output should be *only* the summary paragraph itself, without any introductory phrases like 'Here is the summary:' or any other explanations. "
                "End your response with the word TERMINATE." 
            )
        )

        user_proxy = UserProxyAgent(
            name="UserProxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config=False,
            description="A proxy agent that provides the text and requests a summary."
        )

        prompt = f"Please summarize the following web page content:\n\n---\n{context}\n---\n\nProvide only the summary. End your response with TERMINATE"

        print(f"--- Initiating chat with prompt (first 100 chars): {prompt[:100]}... ---")
        chat_result = user_proxy.initiate_chat(
            assistant,
            message=prompt,
        )
        print("--- Chat finished ---")

        summary = None
        agent_error_message = None

        if hasattr(chat_result, 'error_message') and chat_result.error_message:
             agent_error_message = chat_result.error_message
             print(f"--- Agent chat reported an error: {agent_error_message} ---")
             if "unsupported operand type(s) for +: 'int' and 'NoneType'" in agent_error_message:
                 return f"Internal TypeError during agent chat (reported by AutoGen): {agent_error_message}."
             return f"Error during agent chat: {agent_error_message}"

        print("--- Debugging Full Chat History ---")
        if chat_result.chat_history:
            for i, msg in enumerate(chat_result.chat_history):
                role = msg.get('role', 'N/A')
                content_preview = str(msg.get('content', 'N/A'))[:150] # Longer preview
                print(f"  [{i}] Role: {role}, Content Preview: {content_preview}...")
        else:
            print("  Chat history is empty or None.")
        print("-----------------------------------")
        print(f"--- Attempting WORKAROUND: Extracting summary from LAST message with role 'user' ---")
        if chat_result.chat_history:
            for msg in reversed(chat_result.chat_history):
                if msg.get("role") == "user":
                    print(f"--- Found potential summary message (role='user'): {str(msg.get('content'))[:100]}... ---")
                    raw_content = msg.get("content")
                    if isinstance(raw_content, str):
                        if not raw_content.strip().startswith("Please summarize"):
                            summary = raw_content.replace("TERMINATE", "").strip()
                            if summary:
                                print("--- Successfully extracted non-empty summary (from 'user' role message). ---")
                                break 
                            else:
                                print("--- 'User' role message content was empty after cleaning 'TERMINATE'. Continuing search... ---")
                                summary = None 
                        else:
                             print("--- Skipping 'user' role message as it looks like the original prompt. ---")
                    else:
                        print(f"--- Warning: 'User' role message content is not a string: {raw_content}. Continuing search... ---")
                else:
                     print(f"--- Skipping message with role: {msg.get('role')} ---")

        if summary:
            print(f"--- FINAL Returning summary: {summary[:100]}... ---")
            return summary
        else:
            last_msg_content = chat_result.chat_history[-1].get('content', '[No Content]') if chat_result.chat_history else '[No History]'
            print(f"--- FINAL Failed to extract summary. Last message in history (preview): {str(last_msg_content)[:100]}... ---")
            if chat_result.chat_history and not any(msg.get('role') == 'user' and not str(msg.get('content')).strip().startswith("Please summarize") for msg in chat_result.chat_history):
                 return "Error: Chat finished, but couldn't find a message with role 'user' containing the expected summary (possible role assignment issue in AutoGen history)."
            return f"Error: Agent chat finished, but failed to extract a usable summary. Please check the terminal logs for chat history details."

    except TypeError as te:
         if "unsupported operand type(s) for +: 'int' and 'NoneType'" in str(te):
             error_msg = f"Internal TypeError during agent execution: {str(te)}."
             print(f"--- Caught TypeError: {error_msg} ---")
             return error_msg
         else:
              print(f"--- Caught unexpected TypeError: {str(te)} ---")
              return f"Unexpected TypeError: {str(te)}"
    except ValueError as ve:
         print(f"--- Caught ValueError: {str(ve)} ---")
         return f"Configuration Error: {str(ve)}"
    except AttributeError as ae:
         error_msg = f"Internal AttributeError during agent execution: {str(ae)}."
         print(f"--- Caught AttributeError: {error_msg} ---")
         return error_msg
    except Exception as e:
        error_msg = f"Unexpected error during agent execution: {str(e)} (Type: {type(e).__name__})"
        print(f"--- Caught general Exception: {error_msg} ---")
        if "api key" in str(e).lower() or "permission" in str(e).lower() or "authenticate" in str(e).lower():
            return "Error: Failed to authenticate with Gemini. Please check your API key and permissions."
        return error_msg