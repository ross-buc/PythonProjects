# Story Writing Prompt Application

This is a Python Flask application that prompts users with story ideas to help them overcome writer's block. The application provides a random writing prompt from a collection of pre-defined prompts. Once the user starts typing, they have 10 seconds to continue typing before the text field becomes disabled, encouraging them to write within a time constraint.

## Features

- Randomly generates writing prompts from a collection of pre-defined prompts.
- Starts a countdown timer when the user starts typing.
- Disables the text field after 10 seconds of inactivity.
- Allows users to save their written stories along with the corresponding prompt.

## Installation

1. Clone the repository:
2. pip install -r requirements.txt
3. Set up the database on your pc
4. Run the application
5. Access the application in your web browser at `http://localhost:5000`.

## Usage

- Upon accessing the application, you will be presented with a random writing prompt.
- Start typing your story in the provided text area.
- The countdown timer will start as soon as you start typing.
- You have 10 seconds to continue typing before the text field becomes disabled.
- If you type another word before the countdown ends, the timer will reset and allow you to continue typing.
- To save your story, click the "Save" button.
- You can view your saved stories by visiting the "/saved" route.
