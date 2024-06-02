# Idea Guy API - Empowering Developers with Random Project Ideas

![Idea Guy Logo](https://github.com/Masayaelvin/The_Idea_guy/blob/main/the_idea/static/images/nick-fewings-j8OIk-G8wpw-unsplash%20(1).jpg)

## Overview
The **Idea Guy** API is a  tool designed to provide software engineers and developers with random project ideas across various domains. Whether you're a seasoned developer looking for a new challenge or a novice eager to embark on your coding journey, Idea Guy is here to inspire creativity and innovation.

## Features
- **Random Project Ideas**: Access a vast database of project ideas covering a wide range of topics, including web development, mobile apps, machine learning, and more.
- **Filtered Ideas by Tags/Categories**: Explore project ideas tailored to your interests by filtering based on specific tags or categories.
- **Account creation and Access for Adding Ideas**: Authorized users, such as administrators, can contribute to the Idea Guy database by adding new project ideas.
- **Detailed Project Information**: Retrieve comprehensive details about each project idea, including a title, description, associated tags, and difficulty level.

## Technologies Used to develop
- **Backend Framework**: Flask (Python)
- **Database**: Mysql
- **Authentication**: flask
- **API Documentation**: FastAPI-Swagger_ui
- **Frontend**: HTML, CSS, JavaScript

## Getting Started
### Prerequisites
- Python 3.8+
- MySQL
- Flask
- Virtual environment (venv)

### Installation
1. **Clone the repository:**
    ```bash
    git clone https://github.com/Masayaelvin/The_Idea_guy-api.git
    cd The_Idea_guy/api
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**
    - Create a MySQL database.
    - Configure the database URI in your environment variables or `config.py`.

5. **Run the application:**
    ```bash
    uvicorn api.vi.app:app --reload
    ```
5. **Run the GUI application:**
     ```bash
    python app.py 
    ```

## Usage
### Endpoints
- **Get Random Idea**: `/api/random_idea`
- **Filter Ideas by Tags**: `/api/ideas?tag=web&difficulty=beginner`
- **Add New Idea** (Users only): `/api/add_idea`

### Example API Call
```bash
curl -X GET http://localhost:8000/random_project
```

## API Endpoints

### `/random_project`
- **Method:** GET
- **Description:** Returns a random project from the database. If no projects are found, it raises a 404 error.

### `/users`
- **Method:** GET
- **Description:** Retrieves and returns a list of all users in the database, including their ID, username, email, and timestamps for creation and updates.

### `/projects`
- **Method:** GET
- **Description:** Retrieves and returns a list of all projects in the database, including project details such as ID, title, difficulty level, description, category ID, user ID, and timestamps for creation and updates.

### `/user_projects`
- **Method:** GET
- **Description:** Returns a list of all users along with the projects they have created. Each user's information includes their ID, username, email, and a list of their projects with project details.

### `/categories`
- **Method:** GET
- **Description:** Retrieves and returns a list of all categories along with the projects within each category. Each category's information includes its ID, name, and a list of projects with project details.

### `/filter/{difficulty}`
- **Method:** GET
- **Description:** Filters and returns projects based on the specified difficulty level. If no projects are found for the given difficulty, it raises a 404 error.

### `/category/{category}`
- **Method:** GET
- **Description:** Retrieves and returns projects within a specified category. If the category is not found, it raises a 404 error. Each category's information includes its ID, name, and a list of projects with project details.

### `/`
- **Method:** GET
- **Description:** A root endpoint that returns a welcome message.

Additionally, the application includes CORS middleware to handle cross-origin requests, allowing the frontend to interact with the API. The database session is managed with a dependency injection pattern to ensure proper session handling.

## Future Enhancements
- **User Profiles**: Enable users to create profiles, save favorite ideas, and track their coding journey.
- **Collaboration Features**: Facilitate collaboration between developers by allowing them to share ideas, join projects, and collaborate on innovative solutions.
- **Integration with Development Tools**: Seamlessly integrate Idea Guy with popular development platforms and tools to streamline the project implementation process.


## About the Developer
**masayaelvin@gmail.com** - A passionate backend developer dedicated to empowering the developer community with innovative tools and resources.

Connect with me on [LinkedIn](https://www.linkedin.com/in/elvin-masaya/) or follow me on [GitHub](https://github.com/Masayaelvin).

---

*Inspire. Create. Innovate with Idea Guy.*
