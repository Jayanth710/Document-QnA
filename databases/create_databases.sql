-- Drop databases if they exist
DROP DATABASE IF EXISTS DocumentQnA_test;
DROP DATABASE IF EXISTS DocumentQnA_development;

-- Drop users if they exist
DROP ROLE IF EXISTS DocumentQnA_user;
DROP ROLE IF EXISTS DocumentQnA_user_test;

-- Create databases
CREATE DATABASE DocumentQnA_development;
CREATE DATABASE DocumentQnA_test;

-- Create user and grant access
CREATE USER DocumentQnA_user WITH PASSWORD 'DocumentQnA_secure';
GRANT ALL PRIVILEGES ON DATABASE DocumentQnA_development TO DocumentQnA_user;
GRANT ALL PRIVILEGES ON DATABASE DocumentQnA_test TO DocumentQnA_user;

-- Connect to development database and grant schema permissions
\connect DocumentQnA_development
GRANT USAGE, CREATE ON SCHEMA public TO DocumentQnA_user;

-- Connect to test database and grant schema permissions
\connect DocumentQnA_test
GRANT USAGE, CREATE ON SCHEMA public TO DocumentQnA_user;
