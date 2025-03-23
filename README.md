# ShowShuffle - Movie Recommendation System  

Welcome to **ShowShuffle**, a movie recommendation system that helps users discover movies based on popularity and personalized preferences. This Streamlit-based web application offers an intuitive and engaging way to find movies that suit your taste.  

---

## 🔥 Features  

### 📌 **Personalized Recommendations**  
- Get movie suggestions based on your viewing history and preferences using **collaborative filtering**.  
- Our machine learning model predicts movies you might like based on similar users' ratings.  

### 🎬 **Popular Movie Recommendations**  
- Discover trending and highly-rated movies through **popularity-based recommendations**.  

### 🎭 **Browse by Categories**  
- Explore movies categorized by genres such as **Action, Sci-Fi, Horror, Romance, Comedy, Thriller, and more**.  

### 🖼️ **Movie Cards with Posters**  
- View movie recommendations in an aesthetically pleasing **card layout** with posters fetched dynamically from TMDB API.  

### ⚡ **Fast and Interactive UI**  
- User-friendly navigation with **Streamlit’s interactive widgets** like sliders, expanders, and sidebar menus.  

---

## 🚀 How It Works  

### 1️⃣ **Home Page**  
- Introduction to the recommendation system.  
- Explanation of how recommendations are generated.  

### 2️⃣ **Categories Page**  
- Movies grouped into different genres for easy browsing.  

### 3️⃣ **Movies Page**  
- Choose between **Popularity-based** or **Personalized** recommendations.  
- Enter your **user ID** to get personalized recommendations.  

---

## 🔧 Installation and Setup  

### 🛠️ Prerequisites  
Ensure you have Python installed and the required libraries.  

### 📦 Install Dependencies  
```bash
pip install streamlit pandas numpy scikit-learn requests streamlit-card streamlit-option-menu
```  

### ▶️ Run the Application  
```bash
streamlit run app.py
```  

---

## 📂 Project Structure  

```
/ShowShuffle
│── app.py                 # Main application script
│── archive.zip            # MovieLens dataset (extracted automatically)
│── README.md              # Documentation
│── requirements.txt       # Dependencies
```

---

## 🗂️ Data Used  

This application uses the **MovieLens 100K dataset**, which contains:  
- **User Ratings**: Users rate movies on a scale of 1 to 5.  
- **Movie Information**: Movie titles, genres, release dates.  

---

## 🧠 Recommendation Algorithms  

1️⃣ **Popularity-Based Recommendation**  
   - Suggests movies with the highest average ratings from all users.  

2️⃣ **Collaborative Filtering (User-Based KNN)**  
   - Finds similar users based on rating patterns.  
   - Suggests movies liked by users with similar preferences.  

---

## 🎨 UI Components  

- **Sidebar Navigation** – Choose between Home, Categories, and Movies.  
- **Movie Cards** – Displays movie recommendations beautifully with posters.  
- **Sliders & Inputs** – Customize recommendations easily.  

---

## 🔑 API Usage  

### TMDB API for Movie Posters  
- Fetches high-quality movie posters dynamically.  
- Uses **TMDB API** to search for movie posters.  

---

## 📬 Contact  

If you have any questions, feedback, or suggestions, feel free to reach out:  
📧 **Email**: tejaswimahadev9@gmail.com  

Happy Watching! 🎥🍿
