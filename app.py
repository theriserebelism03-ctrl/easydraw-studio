import os
import streamlit as st
import matplotlib.pyplot as plt
import winsound
from pyaxidraw import axidraw

st.set_page_config(page_title="EasyDraw Controller", page_icon="🖊️", layout="centered")

st.title("🖊️ EasyDraw V3 Mobile Dashboard")

OUTPUT_DIR = "./generated_pages"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- 1. INPUT TEXT & FORMULAS ---
st.header("1. Enter Document Content")
input_text = st.text_area("Paste English Text and LaTeX Formulas Here:", height=200, 
                          value="Line 1: Sample English Text\nMath Equation: \\int_0^\\infty x^2 e^{-x} dx = 2\nLine 3: Plotter execution ready")

if st.button("📄 Generate Vector SVG Pages"):
    lines = [line.strip() for line in input_text.strip().split("\n") if line.strip()]
    lines_per_page = 15
    pages = [lines[i:i + lines_per_page] for i in range(0, len(lines), lines_per_page)]

    for page_idx, page_lines in enumerate(pages, start=1):
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis('off')
        
        y_pos = 0.95
        for line in page_lines:
            ax.text(0.05, y_pos, line, fontsize=14, verticalalignment='top')
            y_pos -= 0.05

        svg_filename = os.path.join(OUTPUT_DIR, f"page_{page_idx:02d}.svg")
        plt.savefig(svg_filename, format="svg", bbox_inches='tight')
        plt.close()

    st.success(f"Successfully generated {len(pages)} vector page(s)!")

# --- 2. PLOTTER REMOTE CONTROLLER ---
st.header("2. Plotter Control Loop")

svg_files = sorted([f for f in os.listdir(OUTPUT_DIR) if f.endswith('.svg')])

if "current_page_idx" not in st.session_state:
    st.session_state.current_page_idx = 0

if len(svg_files) > 0:
    current_idx = st.session_state.current_page_idx
    if current_idx < len(svg_files):
        current_file = svg_files[current_idx]
        st.info(f"Target file: **{current_file}** (Page {current_idx + 1} of {len(svg_files)})")

        if st.button("▶️ Start Plotting Current Page", type="primary"):
            svg_path = os.path.join(OUTPUT_DIR, current_file)
            st.write(f"🖊️ Plotting `{current_file}`...")
            
            # Execute AxiDraw plotting
            ad = axidraw.AxiDraw()
            ad.plot_setup(svg_path)
            ad.options.speed_pendown = 25
            ad.options.speed_penup = 60
            ad.options.pen_pos_down = 30
            ad.options.pen_pos_up = 60
            ad.plot_run()

            # Completion Chime
            winsound.Beep(1200, 300)
            winsound.Beep(1200, 300)
            winsound.Beep(1200, 300)
            
            st.success(f"🔔 Finished plotting Page {current_idx + 1}!")
            st.session_state.current_page_idx += 1
            st.rerun()

    else:
        st.balloons()
        st.success("🎉 All pages in queue completed!")
        if st.button("🔄 Reset Queue"):
            st.session_state.current_page_idx = 0
            st.rerun()
else:
    st.warning("No generated pages found. Add text above and click 'Generate Vector SVG Pages'.")