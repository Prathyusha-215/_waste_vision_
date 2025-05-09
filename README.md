# WasteVision - AI-Based Waste Management System ♻️  

## Overview 📜  
**WasteVision** is a deep learning-based image classification web app that helps users identify whether waste items are **Organic** or **Recyclable**. It leverages a Convolutional Neural Network (CNN) trained on a custom waste dataset and is built with **Streamlit** for quick deployment and ease of use.

Whether you're managing waste in smart cities, educational campaigns, or personal sustainability efforts, **WasteVision** offers an intuitive and interactive tool to support effective waste segregation.

---

## Features 🚀  
- **Image Upload:** Upload a waste item image directly via the interface. 🖼️  
- **Waste Type Prediction:** Instantly identify waste as **Recyclable** or **Organic** using a trained CNN model. 🧠  
- **Streamlit Interface:** Clean, minimal, and user-friendly UI built using Streamlit. 🖥️  
- **Live Web App:** Accessible without any local installation. 🌐  
- **Efficient & Lightweight:** Fast predictions using optimized Keras models. ⚡  

---

## Live Demo 🌍  
Try the app now: [WasteVision Streamlit App]([https://wastevision-jtboe6gjqeysbhtdghrk8f.streamlit.app//](https://wastevision-prathyusha215.streamlit.app/))

---

## Installation 🛠️  
To run **WasteVision** locally, follow these steps:

### 1. Clone the Repository:
```bash
git clone https://github.com/Prathyusha-215/waste_vision.git
cd waste_vision
```

### 2. Create a Virtual Environment (Optional but Recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

### 3. Install Required Libraries:
```bash
pip install -r requirements.txt
```

### 4. Run the App:
```bash
streamlit run waste.py
```

### 5. Open in Browser:
Visit [http://localhost:8501](http://localhost:8501) to use the application locally.

---

## Usage 🎮  
1. **Launch the App** locally or open the [Live Demo](https://wastevision-jtboe6gjqeysbhtdghrk8f.streamlit.app/).  
2. **Upload an Image** of waste (e.g., bottle, banana peel, etc.).  
3. Click on **"Predict Waste Type"** to see the model’s prediction.  
4. **View Output:** The app displays the uploaded image, predicted category, and corresponding emoji.  

---

## Technical Stack 💻  
- **Web App Framework:** Streamlit  
- **Deep Learning:** TensorFlow / Keras  
- **Image Processing:** Pillow  
- **Visualization:** Streamlit Widgets & Matplotlib  
- **Dataset:** Custom dataset for Organic & Recyclable waste  

---

## Project Structure 🗂️  
```plaintext
waste_vision/
├── waste.py                # Main Streamlit app script
├── waste_model.h5          # Pre-trained CNN model
├── waste1.jpg              # Sample image
├── streamlit_app.PNG       # App UI screenshot
├── requirements.txt        # Required Python packages
└── README.md               # Project documentation
```

---

## Contributing 🤝  
We welcome contributions! To contribute:

1. Fork the repository 🍴  
2. Create a new branch 🌿  
3. Make your changes 💻  
4. Submit a pull request 🔄  

---

## License 📜  
This project is licensed under the **MIT License**. See the [LICENSE](https://github.com/Prathyusha-215/waste_vision/blob/main/LICENSE) file for more details.

---

## Acknowledgments 🙏  
- TensorFlow/Keras for the model training framework  
- Streamlit for simplifying app deployment  
- Pillow for handling image uploads  

---

## Contact 📧  
**Developer:** Prathyusha Vanama  
- 📬 Email: prathyushavanama215@gmail.com  
- 🐙 GitHub: [Prathyusha-215](https://github.com/Prathyusha-215)  

---

> ♻️ *WasteVision – Smart Segregation Starts with You!* 🌱
