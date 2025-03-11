import gradio as gr
import mne
import joblib
import pandas
import sys
import mainpre
import tempfile
import os

model=joblib.load("/home/admincit/Desktop/ibrains_dataset/ADHD_project/model.joblib")

# Define the processing function
def process_file(file, state):
    temp_file_path = os.path.join("/tmp", file.name)
    file.save(temp_file_path)
    if file.name.endswith(".vhdr"):
        raw = mne.io.read_raw_brainvision(temp_file_pate, preload=True)
    elif file.name.endswith(".edf"):
        raw = mne.io.read_raw_edf(temp_file_path, preload=True)
    else:
        return print({"error": "Unsupported file type. Please upload a .vhdr or .edf file."}), 400

    # Preprocess and predict
    df = [mainpre.preprocess(raw)]
    if state == "Eyes Closed":
        df = df.assign(ECEO=1)
    else:
        df = df.assign(ECEO=0)

        # Prediction
    pred = model.predict(df)[0]
    result = "Patient Diagnosed with ADHD" if pred == 1 else "Patient is Healthy"
    # Simulate processing (replace with actual logic)
    return result

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# EEG File Upload")
    
    with gr.Row():
        file_input = gr.File(label="Upload EEG File", file_types=[".vhdr", ".edf"])
        state_input = gr.Dropdown(
            choices=["Eyes Open", "Eyes Closed"], 
            label="Select State", 
            value="Eyes Open"
        )
    
    output = gr.Textbox(label="Output", interactive=False)
    submit_btn = gr.Button("Submit")
    
    # Link the submit button to the function
    submit_btn.click(process_file, inputs=[file_input, state_input], outputs=output)

# Launch the app
demo.launch(share=True)
