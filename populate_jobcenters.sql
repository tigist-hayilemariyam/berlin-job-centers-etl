-- STEP 1: CREATE TABLE (ALIGNED WITH PYTHON OUTPUT)
-- This defines the table structure for the Jobcenter data layer.

CREATE TABLE IF NOT EXISTS berlin_data.jobcenters (
    id VARCHAR(20) PRIMARY KEY,          -- 10-digit stable ID
    district_id VARCHAR(20) NOT NULL,    -- Official 8-digit code
    center_name VARCHAR(200) NOT NULL,   -- Updated from 'name' to 'center_name'
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    geometry TEXT NOT NULL,  -- Renamed from geometry_wkt to geometry 
    address TEXT,                -- Added From your Nominatim enrichment
    postal_code VARCHAR(10),
    neighborhood VARCHAR(100),
    district VARCHAR(100),
    neighborhood_id VARCHAR(50),         -- LOR spatial_name code
    
    -- Metadata and Enrichment
    data_source VARCHAR(50) NOT NULL,

    -- Foreign Key Constraint (Linking to Districts table)
    CONSTRAINT district_id_fk 
      FOREIGN KEY (district_id)
      REFERENCES berlin_data.districts(district_id) 
      ON DELETE RESTRICT ON UPDATE CASCADE
);

-- STEP 2: DATA POPULATION
/*
\COPY berlin_data.jobcenters (
    id, 
    district_id, 
    center_name, 
    address,        
    postal_code,    
    latitude, 
    longitude, 
    geometry, 
    neighborhood, 
    district, 
    neighborhood_id, 
    data_source
) 
FROM '../../output/jobcenters_berlin_final.csv' 
DELIMITER ',' 
CSV HEADER;
*/


