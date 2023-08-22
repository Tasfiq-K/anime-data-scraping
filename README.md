# Multilabel Task Classifier from Paper Abstract 
</br>

<h1 align='center' style=color:#fe5e21;><strong>From Paper With Tasks</strong></h1>

A text classification model from data collection, model training, and deployment. <br/>
The model can classify **260** different types of paper tasks <br/>The keys of `json_files/task_types_encoded.json` shows the paper tasks
<br/>

 <h2 style=color:#fe5e21;>Data Collection</h2>

Data was collected from [paperswithcode](https://www.paperswithcode.com)

Data was collected from the categoreis below:
1. [*Computer Vision*](https://paperswithcode.com/methods/area/computer-vision)
    * Convolutional Neural Networks
    * Generative Models
    * Image Model Blocks
    * Object Detections Models
    * Image Feature Extractors
<br/><br/>

2. [*Natural Language Processing*](https://paperswithcode.com/methods/area/natural-language-processing)
    * Language Models
    * Transformers
    * Word Embeddings
    * Attention Patterns
    * Sentence Embeddings
<br/><br/>

3. [*Reinforcement Learning*](https://paperswithcode.com/methods/area/reinforcement-learning)
    * Policy Gradient Methods
    * Off-Policy TD Control
    * Reinforcement Learning Frameworks
    * Q-Learning Networks
    * Value Function Estimation
<br/><br/>

4. [*Audio*](https://paperswithcode.com/methods/area/audio)
    * Generative Audio Models
    * Audio Model Blocks
    * Text-to-Speech Models
    * Speech Separations Models
    * Speech Recognition
<br/><br/>

5. [*Sequential*](https://paperswithcode.com/methods/area/sequential)
    * Recurrent Neural Networks
    * Sequence to Sequence Models
    * Time Series Analysis
    * Temporal Convolutions
    * Bidirectional Recurrent Neural Networks
<br/><br/>

6. [*Graphs*](https://paperswithcode.com/methods/area/graphs)
    * Graph Models
    * Graph Embeddings
    * Graph Representation Learning
    * Graph Data Augmentation
<br/><br/>

The scripts I've used to scrape the data can be found in the [`scrapers`](https://github.com/Tasfiq-K/from-paper-with-tasks/tree/main/scrapers) directory. 

In total, I scraped **34k+** paper abstracts and other informations.

<h2 style=color:#fe5e21;>Data Processing</h2>

Initially there were *640* different genres in the dataset. After some analysis, I found out *499* of them are rare (probably custom genres by users). So, I removed those genres and then I have *141* genres. After that, I removed the description without any genres resulting in *6,104* samples.

## Model Training

Finetuned a `distilrobera-base` model from HuggingFace Transformers using Fastai and Blurr. The model training notebook can be viewed [here](https://github.com/msi1427/MultiLabel-Book-Genre-Classifier/blob/main/notebooks/multilabel_text_classification.ipynb)

## Model Compression and ONNX Inference

The trained model has a memory of 300+MB. I compressed this model using ONNX quantization and brought it under 80MB. 

## Model Deployment

The compressed model is deployed to HuggingFace Spaces Gradio App. The implementation can be found in `deployment` folder or [here](https://huggingface.co/spaces/msideadman/multilabel-book-genre-classifier) 

<img src = "deployment/gradio_app.PNG" width="800" height="400">

## Web Deployment
Deployed a Flask App built to take descprition and show the genres as output. Check `flask ` branch. The website is live [here](https://multilabel-book-genre-classifier.onrender.com) 

<img src = "deployment/flask_app_home.PNG" width="800" height="400">
<img src = "deployment/flask_app_results.PNG" width="800" height="200">