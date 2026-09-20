import os
import matplotlib.pyplot as plt

def convert_text_to_svg_pages(text_content, output_dir="./generated_pages"):
    os.makedirs(output_dir, exist_ok=True)
    lines = text_content.strip().split("\n")
    
    # Paginate 20 lines per page
    lines_per_page = 20
    pages = [lines[i:i + lines_per_page] for i in range(0, len(lines), lines_per_page)]

    for page_idx, page_lines in enumerate(pages, start=1):
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis('off')
        
        y_pos = 0.95
        for line in page_lines:
            ax.text(0.05, y_pos, line, fontsize=14, verticalalignment='top')
            y_pos -= 0.045

        svg_filename = os.path.join(output_dir, f"page_{page_idx:02d}.svg")
        plt.savefig(svg_filename, format="svg", bbox_inches='tight')
        plt.close()
        print(f"Generated vector page: {svg_filename}")

if __name__ == "__main__":
    sample_text = """Sample Page 1 for EasyDraw V3
Tamil Text: வணக்கம் (Hello)
Math Formula: \\int_{0}^{\\infty} x^2 e^{-x} dx = 2
EasyDraw V3 Batch Writing Automation line 1
EasyDraw V3 Batch Writing Automation line 2"""
    convert_text_to_svg_pages(sample_text)