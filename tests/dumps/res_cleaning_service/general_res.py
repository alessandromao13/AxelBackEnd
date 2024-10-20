# import ast
# import re
#
#
# def manage_llm_response(llm_output):
#     # Step 1: Use regex to extract everything between the outermost brackets
#     match = re.search(r'\[.*\]', llm_output, re.DOTALL)
#
#     if not match:
#         raise ValueError("No valid array structure found in the LLM output.")
#
#     cleaned_array_str = match.group(0)
#
#     # Step 2: Attempt to clean and correct common mistakes in the structure
#     cleaned_array_str = correct_common_issues(cleaned_array_str)
#
#     # Step 3: Validate if the cleaned string is a valid Python list
#     try:
#         # Step 4: Convert cleaned single quotes to double quotes before parsing
#         cleaned_array_str = cleaned_array_str.replace("'", '"')
#         python_array = ast.literal_eval(cleaned_array_str)
#
#         if not isinstance(python_array, list):
#             raise ValueError("The corrected data is not a valid list.")
#
#         return python_array
#
#     except (SyntaxError, ValueError):
#         raise ValueError("The corrected content is still not a valid Python array.")
#
#
# def correct_common_issues(array_str):
#     # Common corrections:
#     # 1. Remove any trailing commas inside the list
#     array_str = re.sub(r',\s*]', ']', array_str)
#
#     # 2. Ensure there are commas between elements (e.g., missing commas between numbers or strings)
#     array_str = re.sub(r'(\w)(\s+)(\w)', r'\1, \3', array_str)  # Add comma between elements if missing
#
#     # 3. Replace any accidental single quotes inside double quotes or unescaped quotes
#     array_str = re.sub(r'“|”|\'', '"', array_str)  # Ensure consistent use of double quotes
#
#     # 4. Remove any non-printable characters that might break the array structure
#     array_str = re.sub(r'[^\x20-\x7E]+', '', array_str)
#
#     # 5. Ensure the brackets are balanced, correcting for extra or missing brackets
#     open_brackets = array_str.count('[')
#     close_brackets = array_str.count(']')
#
#     if open_brackets > close_brackets:
#         array_str += ']' * (open_brackets - close_brackets)  # Add missing closing brackets
#     elif close_brackets > open_brackets:
#         array_str = '[' * (close_brackets - open_brackets) + array_str  # Add missing opening brackets
#
#     # 6. Join words separated by commas within strings (e.g., 'Private, Space, Exploration, Company')
#     array_str = re.sub(r'"(.*?)"', lambda m: '"' + m.group(1).replace(",", "").replace("  ", " ") + '"', array_str)
#
#     return array_str
#
#
# def parse_valid_python_dict_or_array(response):
#     """
#     Check if the given response is a well-formatted Python dict or an array of dicts
#     after removing all text outside of the outermost braces or brackets and replacing
#     single quotes with double quotes. Filters out dicts with None values or empty keys.
#
#     Parameters:
#     response (str): The string representation of the response to check.
#
#     Returns:
#     dict, list, or None: The parsed dict or list of dicts if valid, None if invalid.
#     """
#     print("Original Response:", response)
#
#     # Step 1: Remove everything outside of the outermost brackets or braces
#     cleaned_response = re.sub(r'^[^\[{]*|[^\]}]*$', '', response)  # Keep only the text inside [] or {}
#     cleaned_response = cleaned_response.strip()
#     print("Cleaned Response (Braces removed):", cleaned_response)
#
#     # If nothing is left after cleaning, return None
#     if not cleaned_response:
#         return None
#
#     # Step 2: Replace single quotes with double quotes
#     cleaned_response = cleaned_response.replace("'", '"')
#     print("Cleaned Response (Quotes replaced):", cleaned_response)
#
#     # Step 3: Handle special case for double square brackets
#     if cleaned_response.startswith('[[') and cleaned_response.endswith(']]'):
#         cleaned_response = cleaned_response[1:-1]  # Remove the outer brackets
#         cleaned_response = f'[{cleaned_response}]'  # Wrap it back with a single bracket
#
#     # Step 4: Safely evaluate the string to a Python object
#     try:
#         # Attempt to evaluate the cleaned response string to a Python object
#         evaluated_response = ast.literal_eval(cleaned_response)
#         print("Evaluated Response (As Python object):", evaluated_response)
#
#         # Step 5: Filter out dicts with None values or empty keys/values
#         def is_valid_dict(d):
#             # Check if all keys and values are neither None nor empty
#             return isinstance(d, dict) and all(k and v for k, v in d.items())
#
#         if isinstance(evaluated_response, list):
#             # Remove dicts with None or empty keys/values
#             filtered_response = [d for d in evaluated_response if is_valid_dict(d)]
#             return filtered_response if filtered_response else None
#
#         elif isinstance(evaluated_response, dict):
#             # If it's a single dict, check for None or empty keys/values
#             if is_valid_dict(evaluated_response):
#                 return evaluated_response
#             else:
#                 return None
#
#         return None
#
#     # Catch SyntaxError or ValueError during evaluation of response
#     except (SyntaxError, ValueError) as e:
#         print(f"Failed to evaluate the response due to error: {e}")
#         return None