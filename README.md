# Getfeels - Sentiment Analysis Web Application
This repository contains code for a web application that performs sentiment analysis on comments from a YouTube channel using the BERT model. The application is built with JavaScript for the frontend and Python (Flask) for the backend.

## Features
- YouTube Channel Sentiment Analysis: Analyzes sentiment of comments from a specified YouTube channel.
- Visual Representation: Displays sentiment analysis results using a pie chart for a visually pleasing representation.
- Error Handling: Provides error handling for various scenarios, such as invalid channel name or no comments found.

## Technologies Used
- JavaScript: Frontend development for dynamic user interaction and visualization.
- Python (Flask): Backend development for API endpoints and sentiment analysis.
- BERT Model: Utilized for sentiment analysis on comments.
- HTML/CSS: Used for structuring and styling the web interface.

## Frontend
- Global Methods: Functions for smooth element deletion and opacity transitions.
- Chart Class: Creates a pie chart to visualize sentiment analysis results.
- Screen Class: Manages screen elements such as loading screens and error messages.
- Main Function: Initializes the application upon DOM being loaded.

## Backend (Python Flask)
The backend of the application is built with Python Flask, providing API endpoints for sentiment analysis and serving HTML templates. 
Here's an overview of the backend components:

- Flask Routes: Defines routes for the web application, including the home page and sentiment analysis endpoint.
- Sentiment Analysis: Performs sentiment analysis on YouTube comments using the BERT model.
- Error Handling: Handles errors such as invalid channel names or no comments found.

### File Structure
app.py: Main Flask application file containing routes and logic.
static/: Directory containing static assets (JavaScript, CSS).
templates/: HTML templates for rendering the frontend.
bert_main.py: Script for BERT-based sentiment analysis (from a saved and trained model).
bert_clf.py: Script for training and saving new models from scratch. This file would be executed if I want to improve the model in the future and deploy a better version with higher accuracy.
preprocessing.py: Script for preprocessing input data (text documents) that will later on be fed into the BERT model. 
utils.py: Utility functions used within the application such as getting a saved BERT model.
youtube_api.py: Module for fetching comments from the YouTube Data API.
