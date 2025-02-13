-- Create table for storing user data
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR PRIMARY KEY,
    age INTEGER,
    gender VARCHAR(20),
    location VARCHAR(100),
    last_active TIMESTAMP,
    session_duration INTEGER, -- in minutes
    preferred_category VARCHAR(50)
);

-- Create table for storing product data
CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR PRIMARY KEY,
    category VARCHAR(50),
    title VARCHAR(255),
    description TEXT,
    price NUMERIC(10, 2),
    image_url TEXT,
    brand VARCHAR(100)
);

-- Create table for storing user-product interactions
CREATE TABLE IF NOT EXISTS interactions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR REFERENCES users(user_id),
    product_id VARCHAR REFERENCES products(product_id),
    clicks INTEGER,
    cart_additions INTEGER,
    purchases INTEGER,
    time_spent INTEGER,       -- in seconds
    ratings NUMERIC(2,1),
    reviews TEXT,
    search_queries VARCHAR(255),
    purchase_frequency VARCHAR(50),
    last_purchase_date TIMESTAMP,
    abandoned_cart BOOLEAN,
    wishlist_additions INTEGER,
    view_count INTEGER
);
