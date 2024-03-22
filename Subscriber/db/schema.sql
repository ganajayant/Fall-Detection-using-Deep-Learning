CREATE TABLE Accidents (
    id INT AUTO_INCREMENT PRIMARY KEY, accelerometer_x FLOAT NOT NULL, accelerometer_y FLOAT NOT NULL, accelerometer_z FLOAT NOT NULL, gyroscope_x FLOAT NOT NULL, gyroscope_y FLOAT NOT NULL, gyroscope_z FLOAT NOT NULL, latitude FLOAT NOT NULL, longitude FLOAT NOT NULL, accident_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);