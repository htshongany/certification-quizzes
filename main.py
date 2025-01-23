import os
import re
import json
import argparse

def convert_markdown_to_json(markdown_text):
   questions = []
   question_blocks = re.findall(r'(\d+\.\s.*?)(?=\n\d+\.|\Z)', markdown_text, re.DOTALL)
   
   for block in question_blocks:
       try:
           # Extract question text
           question_match = re.search(r'\d+\.\s(.*?)(?=\n\s*-)', block, re.DOTALL)
           question_text = question_match.group(1).strip() if question_match else ""
           
           # Extract options
           options = re.findall(r'\s*-\s+([A-E]\.\s*.*)', block)
           options = [option.split('. ', 1)[1] for option in options if '. ' in option]
           
           # Skip if no options found
           if not options:
               continue
           
           # Extract correct answer
           answer_match = re.search(r'Correct answer:\s*([A-E](?:,\s*[A-E])*)', block)
           if answer_match:
               answers = answer_match.group(1).split(',')
               answer_indices = [ord(ans.strip()) - ord('A') for ans in answers]
               
               # If only one answer, convert to single index
               answer = answer_indices[0] if len(answer_indices) == 1 else answer_indices
           else:
               answer = 0
           
           questions.append({
               "question": question_text,
               "options": options,
               "answer": answer
           })
       except Exception as e:
           print(f"Error processing block: {block}")
           print(f"Error details: {e}")
   
   return questions

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