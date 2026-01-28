# Berlin Job Center Geospatial Data Pipeline

## Project Overview
Developed during a Data Science internship, this project focuses on the automated extraction and geospatial analysis of Berlin employment agency data.
The goal was to transform raw OpenStreetMap (OSM) data into a high-integrity dataset for cloud-based analysis in AWS RDS.

## Key Technical Achievements
* **Data Sanitization**: Implemented Python logic within Jupyter Notebooks to standardize ID formats and handle missing values for 63 records.
* **Geospatial Analysis**: Utilized GeoPandas to perform spatial joins, mapping coordinates to official Berlin LOR boundaries.
* **Cloud Infrastructure**: Established secure data pipelines to AWS RDS via SSM tunneling.

## Tech Stack
* **Languages**: Python (Pandas, GeoPandas, SQLAlchemy)
* **Environment**: VS Code & Jupyter Notebooks
* **Cloud/DB**: AWS RDS, PostgreSQL/PostGIS
* **Tools**: DBeaver, Git, AWS CLI
* ** Tableau Dashboard : https://public.tableau.com/views/jobcenters_berlin/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link
