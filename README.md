# Flask Chat Application Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Getting Started](#getting-started)
4. [Usage](#usage)
5. [Code Explanation](#code-explanation)
   - [main.py](#mainpy)
   - [utils.py](#utilspy)
   - [templates](#templates)
     - [base.html](#basehtml)
     - [home.html](#homehtml)
     - [room.html](#roomhtml)
   - [Static](#static)
     - [styles.css](#stylescss)
6. [Running Tests](#running-tests)
7. [Contributing](#contributing)
8. [License](#license)

## Introduction

The Flask Chat Application is a real-time chat platform that allows users to join chat rooms, exchange text messages, and share files. The application is built using Flask, Flask-SocketIO, and Socket.IO for the server and real-time communication capabilities.

## Project Structure

The project is organized into the following directory structure:

```
Flask-Chat-Application/
|-- Static/
|--  |--  styles/
|--  |--  |--  styles.css
|--  templates/
|--  |--  base.html
|--  |--  home.html
|--  |--  room.html
|--  uploads/
|--  main.py
|--  utils.py
```

- **Static:** Contains static assets, such as CSS files.
- **Templates:** Holds HTML templates for rendering pages.
- **Uploads:** Stores uploaded files.
- **main.py:** The main application script.
- **utils.py:** Utility functions for generating room codes.
- **templates:** Directory for HTML templates.
- **Static/styles/styles.css:** CSS file for styling the application.

## Getting Started

Follow these steps to run the Flask Chat Application locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/kardam00/Flask-Chat-Application.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Flask-Chat-Application-main/Flask-Chat-Application-main
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python main.py
   ```

   The application will be accessible at [http://localhost:5000](http://localhost:5000).

## Usage

### Chat Application Workflow:

1. Open the application in your browser.
2. Enter your name and choose to either create a new room or join an existing room.
3. If creating a new room, a unique room code will be generated.
4. If joining an existing room, enter the room code provided by the host.
5. Once inside a room, you can exchange messages in real-time.
6. To upload a file, use the file input and click the "Send" button.
7. You can leave the chat room at any time by clicking the "Leave the Chat" link.

## Code Explanation

### main.py

`main.py` is the main script that runs the Flask application and handles Socket.IO events.

- **Key Functions:**
  - `home`: Renders the home page and handles room creation/joining.
  - `room`: Renders the chat room page.
  - Socket.IO event handlers (`handle_connect`, `handle_message`, `handle_file_upload`, `handle_disconnect`).

### utils.py

`utils.py` contains a utility function for generating unique room codes.

- **Function:**
  - `generate_room_code`: Generates a unique room code based on existing codes.

### templates

#### base.html

`base.html` serves as the base template for other HTML pages.

- **Content:**
  - HTML structure with common elements (head, body).
  - Links to static files (CSS).
  - Includes a div with the id "root" where page-specific content is injected.

#### home.html

`home.html` is the template for the home page where users enter their name and room details.

- **Content:**
  - Form for entering name, creating or joining a room.
  - Error message display if applicable.

#### room.html

`room.html` is the template for the chat room page.

- **Content:**
  - Displays room information, messages, and file uploads.
  - Includes a script for Socket.IO events handling.

### Static

#### styles.css

`styles.css` is the stylesheet for styling the application.

- **Key Styles:**
  - Defines the layout, colors, and styles for various elements.
  - Includes styles for different types of messages (self, peer).
  - Responsive design for different screen sizes.

