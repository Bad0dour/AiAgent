import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
import os
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI

def main():

    parser = argparse.ArgumentParser(description="ChatBot")
    
    parser.add_argument("user_prompt", type=str,                  help="User Prompt")
    parser.add_argument("-v", "--verbose",   action="store_true", help="Enable verbose output")
    
    args = parser.parse_args() 
    usr_prompt = args.user_prompt


    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("API Key could not be loaded.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": usr_prompt},
    ]

    def generate_content(client: OpenAI, messages: list, verbose: bool) -> None:
        for i in range(20):
            response = client.chat.completions.create(
                model="openrouter/free",
                messages=messages,
                tools=available_functions,
            )
            
            if not response.usage:
                raise RuntimeError("API response appears to be malformed")
    
            message = response.choices[0].message
            messages.append(message)
        
            if verbose:
                print(f"\nSystem prompt:{system_prompt}")
                print(f"User prompt:\n{usr_prompt}\n")
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")
            
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    result_message = call_function(tool_call, verbose)
                    if result_message["content"] == "":
                        raise ValueError("Error: Content is empty")
                    if verbose:
                        print(f"-> {result_message['content']}")
                    messages.append(result_message)
            else:
                print(f"\nResponse:\n{message.content}\n\n\n")
                break
            if i == 19:
                print(f"Error: Reached maximum number of repeats. To hard of a prompt, or stuck in loop.")
                sys.exit(1)
    
    generate_content(client, messages, args.verbose)


if __name__ == "__main__":
    main()
