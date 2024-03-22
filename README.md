# Fall Detection System

Fall Detection System is a project that aims to detect falls in real-time using a accelerometer and gryoscope sensor. The system is able to detect falls in real-time and send an alert to a caregiver. The system is implemented using a Raspberry Pi, an accelerometer and gyroscope sensor, it uses a deep learning model to detect falls and the communcation between the wearable device and the server is done using MQTT protocol.
## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Introduction
The Fall Detection System is designed to provide an automated solution for detecting falls and notifying caregivers promptly. It utilizes sensors to capture data from the wearer's movements, specifically an accelerometer and gyroscope sensor. By analyzing the motion patterns, the system can identify if a fall has occurred. When a fall is detected, an alert message is sent to a designated caregiver, ensuring that help can be provided quickly.
## Features
The Fall Detection System offers the following features:

1. Real-time fall detection: The system continuously monitors the wearer's movements and can detect falls in real-time.
2. Alert notification: When a fall is detected, an alert message is sent to a designated caregiver, providing immediate notification.
3. Wearable device integration: The system can be integrated with a wearable device, such as a wristband or pendant, to ensure continuous monitoring.
4. Raspberry Pi implementation: The system is implemented using a Raspberry Pi, a small and affordable computer, making it accessible and easy to set up.
5. Deep learning model: The fall detection algorithm utilizes a deep learning model, which has been trained on a large dataset to accurately identify fall patterns.
6. MQTT communication: The system employs the MQTT (Message Queuing Telemetry Transport) protocol for efficient and reliable communication between the wearable device and the server.
7. User-friendly interface: The system features a user-friendly interface that allows to analyze the data.

## Installation
Clone the repository & Change the directory
```bash
git clone git@github.com:ganajayant/Fall-Detection-using-Deep-Learning.git
```

### Subscriber & Server Installation

1. Install the required packages by creating a virtual environment

    Change the directory to the server folder
    ```bash
    cd Fall-Detection-using-Deep-Learning/Subscriber
    ```

    For Macos and Linux
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

    For Windows
    ```bash
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```
2. Intialize the database

    make sure virtual environment is activated

    For Macos and Linux
    ```bash
    source venv/bin/activate
    python Subscriber.py
    ```

    For Windows
    ```bash
    venv\Scripts\activate
    python Subscriber.py
    ```

### React App Installation

1. Install the required packages

    Change the directory to the server folder
    ```bash
    cd Fall-Detection-using-Deep-Learning/client
    ```

    Install the required packages
    ```bash
    npm install
    ```

### Raspberry Pi Installation

1. Clone the repository & Change the directory in the Raspberry Pi

    ```bash
    git clone git@github.com:ganajayant/Fall-Detection-using-Deep-Learning.git
    cd Fall-Detection-using-Deep-Learning/Publisher
    ```

2. Create a virtual environment and install the required packages

    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
## Usage

### Subscriber & Server Usage

1. Create .env file in the Subscriber folder and add the following variables

    ```bash
    EMAIL="<email>"
    PASSWORD="<password>"
    PORT=<"port">
    CLOUDAMQP_URL="<cloudamqp_url>"
    ```

2. Run the subscriber script

        make sure virtual environment is activated

        For Macos and Linux
        ```bash
        source venv/bin/activate
        python Subscriber.py
        ```

        For Windows
        ```bash
        venv\Scripts\activate
        python Subscriber.py
        ```

3. Run the server script

        open another terminal
        make sure virtual environment is activated

        For Macos and Linux
        ```bash
        source venv/bin/activate
        python server.py
        ```

        For Windows
        ```bash
        venv\Scripts\activate
        python server.py
        ```


### React App Usage

1. Create .env file in the client folder and add the following variables

    ```bash
    REACT_APP_URL="<server_url>"
    ```
2. Run the react app

    ```bash
    npm start
    ```
3. Open the browser and go to the following url

    ```bash
    http://localhost:3000
    ```
### Raspberry Pi Usage
1. Run the publisher script

    make sure virtual environment is activated

    ```bash
    source venv/bin/activate
    python Publisher.py
    ```


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
