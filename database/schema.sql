-- Create table for bins
CREATE TABLE bins (
    bin_id INT AUTO_INCREMENT,
    bin_name VARCHAR(255) NOT NULL,
    bin_type VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    PRIMARY KEY (bin_id)
);

-- Insert sample data into bins table
INSERT INTO bins (bin_name, bin_type, location) VALUES
('Bin 1', 'Recycling', 'Front Yard'),
('Bin 2', 'Organic Waste', 'Backyard'),
('Bin 3', 'Food Waste', 'Garage'),
('Bin 4', 'Plastic Waste', 'Side Walk'),
('Bin 5', 'Glass Waste', 'Street Corner');

-- Create table for alerts
CREATE TABLE alerts (
    alert_id INT AUTO_INCREMENT,
    bin_id INT NOT NULL,
    alert_type VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    PRIMARY KEY (alert_id),
    FOREIGN KEY (bin_id) REFERENCES bins(bin_id)
);

-- Insert sample data into alerts table
INSERT INTO alerts (bin_id, alert_type, description) VALUES
(1, 'Full', 'Bin 1 is full'),
(2, 'Low', 'Bin 2 has low organic waste'),
(3, 'High', 'Bin 3 has high food waste');

-- Create table for collections
CREATE TABLE collections (
    collection_id INT AUTO_INCREMENT,
    bin_id INT NOT NULL,
    collection_date DATE NOT NULL,
    PRIMARY KEY (collection_id),
    FOREIGN KEY (bin_id) REFERENCES bins(bin_id)
);

-- Insert sample data into collections table
INSERT INTO collections (bin_id, collection_date) VALUES
(1, '2023-03-01'),
(2, '2023-03-15'),
(3, '2023-04-01'),
(4, '2023-05-01'),
(5, '2023-06-01');
