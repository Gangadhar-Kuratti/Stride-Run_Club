-- STRIDE RUN CLUB Database Schema
-- MySQL 8.0 Database Setup

-- Create database
CREATE DATABASE IF NOT EXISTS stride_run_club;
USE stride_run_club;

-- Runs table
CREATE TABLE IF NOT EXISTS runs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    distance DECIMAL(5,2) NOT NULL,
    starting_point VARCHAR(200) NOT NULL,
    pace VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Members table
CREATE TABLE IF NOT EXISTS members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    experience VARCHAR(50),
    preferred_distance VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Registrations table
CREATE TABLE IF NOT EXISTS registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    run_id INT NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,
    FOREIGN KEY (run_id) REFERENCES runs(id) ON DELETE CASCADE,
    UNIQUE KEY unique_registration (member_id, run_id)
);

-- Insert sample upcoming runs
INSERT INTO runs (title, date, time, distance, starting_point, pace, description) VALUES
('Sunday Morning Run', '2026-08-30', '06:00:00', 5.0, 'City Park Main Gate', 'Beginner Friendly', 'A relaxed 5K run perfect for beginners and experienced runners alike. We stick together and no one gets left behind.'),
('Saturday Long Run', '2026-09-04', '06:00:00', 10.0, 'City Park Main Gate', 'Intermediate', 'Our weekly long run. Ideal for those training for longer distances. Hydration support provided.'),
('Tuesday Tempo Run', '2026-08-25', '06:30:00', 5.0, 'Riverside Path', 'Intermediate', 'Faster-paced 5K run with intervals. Great for improving speed and fitness.'),
('Thursday Easy Run', '2026-08-27', '06:00:00', 4.0, 'City Park Main Gate', 'Beginner Friendly', 'Easy conversational pace run. Perfect for recovery and building base fitness.'),
('Wednesday Track Session', '2026-08-26', '06:00:00', 6.0, 'City Track', 'All Levels', 'Structured track workout with options for all abilities. Intervals and drills included.');
