# CAGEChat Frontend

Welcome to CAGEChat Frontend Repo!

Okay, you know... I got a really hard time trying to code this (even with Cursor, ChatGPT, Gemini, etc). I hate it, but it's necessary.

So, in order to increase the chance of sucess, I've decided to invest a good time doing a REACT frontend client. Please enjoy it, and have mercy of me.


## Overview

CAGEChat is a web application designed to assist with legal norm consultations. 
This frontend client is built with React and provide a way to users interact with the RAG System.


## Features

- **Chat Interface**: Communicate with an AI assistant specialized in legal norms
- **Question Collector**: Contribute to the project by submitting legal questions and answers
- **Conversation History**: Access previous chat sessions
- **Responsive Design**: Works on desktop and mobile devices

## Project Structure

The frontend is organized as follows:

- `src/`
  - `assets/`: Contains images and icons
  - `components/`: Reusable React components
  - `pages/`: Main application pages
  - `styles/`: CSS files for styling
  - `App.js`: Main application component
  - `index.js`: Entry point

## Key Components

- **ChatPage**: Main interface for interacting with the AI
- **QuestionCollector**: Interface for contributing legal questions and answers
- **Sidebar**: Navigation component for accessing different parts of the application
- **AboutSection**: Information about the project and its purpose

## API Integration

The frontend communicates with the backend through several API endpoints:

- `/chat_stream/`: Streaming endpoint for real-time chat responses
- `/add_question/`: Endpoint for submitting new questions to the database
- `/get_all_questions_from_user/`: Retrieves user-specific questions

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Clone the repository
2. Navigate to the frontend directory:
   ```
   cd frontend_react/client
   ```
3. Install dependencies:
   ```
   npm install
   ```
4. Start the development server:
   ```
   npm start
   ```

