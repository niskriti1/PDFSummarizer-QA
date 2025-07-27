import os
from llama_parse import LlamaParse
from dotenv import load_dotenv
load_dotenv()

def parse_s3_pdf_to_markdown_table(
    pdf_path: str,
    output_dir: str = "output"
):
    try:
        # Extract the PDF filename from the path
        pdf_filename = pdf_path.split("/")[-1]
        
        print(f"Processing PDF: {pdf_filename}")
        
        parser = LlamaParse(
                        api_key=os.getenv("LLAMA_API_KEY"),
                        result_type="markdown",
                        auto_mode=True,
                        auto_mode_trigger_on_table_in_page=True,
                        auto_mode_trigger_on_image_in_page=True,
                        skip_diagonal_text=True,
                        disable_ocr=False,
                        disable_image_extraction=False,
                        do_not_cache=True,
                        verbose=True,
                    ).load_data(pdf_path)
        markdown_text = "\n".join(doc.text for doc in parser)

        # Create markdowns directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Save markdown text to file
        markdown_filename = f"{pdf_filename.split('.')[0]}.md"
        markdown_file_path = os.path.join(output_dir, markdown_filename)
        
        with open(markdown_file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)

        print(f"Markdown saved to: {markdown_file_path}")
        print(markdown_text)
        return markdown_text
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

# Example usage
if __name__ == "__main__":
  
    parse_s3_pdf_to_markdown_table("./Resume.pdf")