import os
import re
import json
import argparse

def convert_markdown_to_json(markdown_text):
    questions = []
    # Split questions while ignoring code blocks
    question_blocks = re.split(r'\n\d+\. ', markdown_text)[1:]
    
    for block in question_blocks:
        try:
            # Extract question text (handle multi-line questions)
            question_part = re.split(r'\n\s*-', block, 1)[0]
            question_text = re.sub(r'<.*?>', '', question_part)  # Remove HTML tags
            question_text = re.sub(r'\n+', ' ', question_text).strip()

            # Extract options
            options_section = re.search(r'-\s.*?(?=\n\s*<details)', block, re.DOTALL)
            if not options_section:
                continue
                
            options = []
            option_lines = re.findall(r'-\s+([A-E]\.\s*.*?)(?=\n\s*-|\Z)', options_section.group(0), re.DOTALL)
            for line in option_lines:
                option_text = re.split(r'\.\s+', line, 1)[-1].replace('\n', ' ').strip()
                options.append(option_text)

            # Extract correct answer(s)
            answer_match = re.search(r'Correct [Aa]nswer[^:\n]*:\s*([A-Z, ]+)(?:\n|$)', block)
            if answer_match:
                raw_answers = answer_match.group(1).replace(' ', '').replace(',', '')
                answers = list(raw_answers)
                answer_indices = [ord(ans.upper()) - ord('A') for ans in answers if ans in 'ABCDE']
                
                # Validate answer indices
                valid_answers = [idx for idx in answer_indices if 0 <= idx < len(options)]
                if not valid_answers:
                    continue  # Skip invalid answers
                    
                answer = valid_answers if len(valid_answers) > 1 else valid_answers[0]
            else:
                continue  # Skip questions without valid answer

            questions.append({
                "question": question_text,
                "options": options,
                "answer": answer
            })
        except Exception as e:
            print(f"Error processing block: {block[:200]}...")
            print(f"Error details: {str(e)}")
    
    return questions

# ... (le reste du code reste identique) ...

def process_file(input_file, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_dir, f"{base_name}.json")
    
    # Read markdown file
    with open(input_file, 'r', encoding='utf-8') as file:
        markdown_text = file.read()
    
    # Convert to JSON
    exam_json = convert_markdown_to_json(markdown_text)
    
    # Only write JSON if questions were found
    if exam_json:
        # Write to JSON file
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(exam_json, json_file, indent=4, ensure_ascii=False)
        
        print(f"Converted {input_file} to {output_file}")
    else:
        print(f"No questions found in {input_file}. Skipping JSON conversion.")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert Markdown exam files to JSON')
    parser.add_argument('-f', '--file', help='Specific markdown file to convert')
    parser.add_argument('-d', '--directory', help='Directory containing markdown files to convert')
    parser.add_argument('-o', '--output', default='quiz-json', help='Output directory for JSON files')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate arguments
    if not (args.file or args.directory):
        parser.error('Either -f/--file or -d/--directory must be specified')
    
    # Process single file
    if args.file:
        if not os.path.isfile(args.file):
            print(f"Error: File {args.file} does not exist")
            return
        process_file(args.file, args.output)
    
    # Process directory
    if args.directory:
        if not os.path.isdir(args.directory):
            print(f"Error: Directory {args.directory} does not exist")
            return
        
        # Find all markdown files
        markdown_files = [
            os.path.join(args.directory, f) 
            for f in os.listdir(args.directory) 
            if f.endswith('.md')
        ]
        
        # Convert each markdown file
        for file in markdown_files:
            process_file(file, args.output)

if __name__ == '__main__':
    main()
