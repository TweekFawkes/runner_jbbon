# Import necessary libraries
import os
import argparse
import random # Added for randomization

# Define standard folder names relative to the script location
INPUT_FOLDER = "inputs"
OUTPUT_FOLDER = "outputs"

def process_text_file(input_filename, apply_uppercase=False, apply_reverse=False):
    """
    Reads a text file, optionally randomizes case and/or reverses text,
    and saves the result to the OUTPUT_FOLDER.

    Args:
        input_filename (str): The name of the input text file.
        apply_uppercase (bool): Whether to randomize character case.
        apply_reverse (bool): Whether to reverse the text.

    Returns:
        bool: True if the process completes successfully, False otherwise.
    """
    input_path = os.path.join(INPUT_FOLDER, input_filename)
    # Use a consistent output suffix
    output_filename = os.path.splitext(input_filename)[0] + "_processed.txt"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    try:
        # 1. Validate input path
        if not os.path.isfile(input_path):
            print(f"Error: Input file not found at '{input_path}'")
            return False

        print(f"Processing '{input_path}'...")

        # 2. Ensure output directory exists
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        # 3. Read the input text file
        with open(input_path, 'r', encoding='utf-8') as infile:
            processed_text = infile.read()

        actions_applied = []

        # 4. Apply Uppercase (if requested)
        if apply_uppercase:
            modified_text_upper = ""
            for char in processed_text:
                if 'a' <= char <= 'z' or 'A' <= char <= 'Z': # Only randomize letters
                    if random.choice([True, False]): # 50% chance to change case
                        modified_text_upper += char.upper()
                    else:
                        modified_text_upper += char.lower()
                else:
                    modified_text_upper += char # Keep non-letters as is
            processed_text = modified_text_upper # Update text for potential next step
            actions_applied.append("random uppercase")

        # 5. Apply Reverse (if requested)
        if apply_reverse:
            processed_text = processed_text[::-1] # Reverse the current text
            actions_applied.append("reverse")

        # 6. Check if any action was taken
        if not actions_applied:
            print(f"Warning: No processing options selected for '{input_filename}'. Output file will be a copy.")
            # processed_text is already the original text

        # 7. Write the modified text to the output file
        with open(output_path, 'w', encoding='utf-8') as outfile:
            outfile.write(processed_text)

        if actions_applied:
            print(f"Successfully applied [{', '.join(actions_applied)}] and saved to '{output_path}'")
        else:
            print(f"Copied original content to '{output_path}'")
        return True

    except Exception as e:
        print(f"An unexpected error occurred processing '{input_filename}': {e}")
        return False


# --- Command-Line Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=f"Reads a text file from './{INPUT_FOLDER}/', optionally randomizes character case and/or reverses text, and saves the result to './{OUTPUT_FOLDER}/'."
    )
    parser.add_argument(
        "-f", "--filename",
        required=True,
        help=f"Filename of the input text file (e.g., 'my_document.txt' for '{INPUT_FOLDER}/my_document.txt')."
    )
    parser.add_argument(
        "-u", "--uppercase",
        action="store_true", # Treat as a boolean flag
        help="Randomly change the case of alphabetic characters."
    )
    parser.add_argument(
        "-r", "--reverse",
        action="store_true", # Treat as a boolean flag
        help="Reverse the text content."
    )
    # Removed the quality argument

    args = parser.parse_args()

    # Call the text processing function with the arguments
    process_text_file(
        args.filename,
        apply_uppercase=args.uppercase,
        apply_reverse=args.reverse
    )

# Removed image conversion quality check and related code.