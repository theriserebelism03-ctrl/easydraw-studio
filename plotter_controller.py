import os
import time
import winsound
from pyaxidraw import axidraw

def ring_completion_chime(page_num, total_pages):
    print("\n" + "="*50)
    print(f"🔔 PAGE {page_num} OF {total_pages} FINISHED WRITING!")
    print("="*50)
    
    for _ in range(3):
        winsound.Beep(1200, 400)
        time.sleep(0.1)

def run_plot_job(svg_filepath):
    ad = axidraw.AxiDraw()
    ad.plot_setup(svg_filepath)
    
    # Speed and height settings
    ad.options.speed_pendown = 25
    ad.options.speed_penup = 60
    ad.options.pen_pos_down = 30
    ad.options.pen_pos_up = 60
    
    print(f"\n🖊️ Writing file: {os.path.basename(svg_filepath)}...")
    ad.plot_run()

def start_automated_session(pages_folder="./generated_pages"):
    svg_files = sorted(
        [os.path.join(pages_folder, f) for f in os.listdir(pages_folder) if f.endswith('.svg')]
    )
    total_pages = len(svg_files)
    
    if total_pages == 0:
        print("❌ No SVG pages found! Run page_builder.py first.")
        return

    print(f"📁 Loaded {total_pages} pages for EasyDraw V3.")
    
    for index, svg_path in enumerate(svg_files):
        current_page = index + 1
        
        run_plot_job(svg_path)
        ring_completion_chime(current_page, total_pages)
        
        if current_page < total_pages:
            print(f"\n⏸️ PAUSED: Swap paper for Page {current_page + 1}.")
            input("👉 Place fresh paper on EasyDraw and press [ENTER] to continue...")
        else:
            print("\n🎉 ALL PAGES COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    start_automated_session()