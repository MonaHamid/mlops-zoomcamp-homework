# NYC Taxi Duration Predictor 🚕
This ML app predicts the average duration of NYC taxi rides from public monthly data.

 Batch predictions  
 Deployed on Hugging Face Spaces  
Built with Scikit-learn + Gradio  

<img width="850" alt="image" src="https://github.com/user-attachments/assets/ac599d4a-44f9-451c-8473-6cd00aff39f7" />

Deployed a batch prediction pipeline for NYC Taxi duration prediction using Prefect Cloud. The pipeline:

Loads preprocessed taxi trip data

 Loads a serialized model (model.bin) and vectorizer

 Generates duration predictions using scikit-learn

 Saves predictions to a file with timestamp

Uses Prefect Cloud with a managed work pool, custom requirements.txt, and GitHub integration

 Debugged and resolved cloud execution issues including:

Module import failures

Missing dependency installation

File sync errors (e.g., model.bin, batch.py)

 Final deployment runs successfully on Prefect Cloud with automated scheduling options enabled





<img width="959" alt="image" src="https://github.com/user-attachments/assets/ffa42ed7-5343-40d7-87e7-5c030856759b" />
