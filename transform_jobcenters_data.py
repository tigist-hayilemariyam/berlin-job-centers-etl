import pandas as pd
import geopandas as gpd
import osmnx as ox
import hashlib
import os

# --- 1. CONFIGURATION ---
PLACE_NAME = "Berlin, Germany"
OSM_TAGS = {"office": "employment_agency"}
LOR_PATH = "lor_ortsteile.geojson" 
OUTPUT_PATH = "output/jobcenters_berlin_final.csv"

# --- 2. EXTRACTION ---
print("Fetching data from OSM...")
gdf_raw = ox.features_from_place(PLACE_NAME, OSM_TAGS)
gdf_raw = gdf_raw.to_crs(epsg=4326)

# Safety check: Remove rows without geometry before processing
gdf_raw = gdf_raw.dropna(subset=['geometry']).copy()

# --- 3. COORDINATE PREP & STABLE ID ---
print("Generating coordinates and stable IDs...")
# Extracting Lat/Lon from centroids
gdf_raw['latitude'] = gdf_raw.geometry.centroid.y
gdf_raw['longitude'] = gdf_raw.geometry.centroid.x

# Deterministic ID generation using hashlib
gdf_raw['id'] = gdf_raw.apply(
    lambda row: int(hashlib.sha256(f"{row.get('name', 'Unknown')}_{row['latitude']}_{row['longitude']}".encode()).hexdigest(), 16) % (10**10), 
    axis=1
)

# --- 4. LOR SPATIAL JOIN ---
if os.path.exists(LOR_PATH):
    print("LOR file found. Loading and joining...")
    lor_gdf = gpd.read_file(LOR_PATH).to_crs(epsg=4326)
    
    # Mapping coordinates into LOR boundaries
    gdf_mapped = gpd.sjoin(gdf_raw, lor_gdf, how='left', predicate='within')
else:
    print(f"Error: {LOR_PATH} not found at {os.getcwd()}")
    gdf_mapped = gdf_raw.copy()

# --- 5. DISTRICT & NEIGHBORHOOD CLEANUP ---
rename_dict = {
    'name': 'center_name',
    'BEZIRK': 'district',
    'OTEIL': 'neighborhood',
    'spatial_name': 'neighborhood_id'
}
gdf_mapped = gdf_mapped.rename(columns=rename_dict)

# Map the official 8-digit District IDs
district_mapping = {
    'Mitte': '11001001', 'Friedrichshain-Kreuzberg': '11002002',
    'Pankow': '11003003', 'Charlottenburg-Wilmersdorf': '11004004',
    'Spandau': '11005005', 'Steglitz-Zehlendorf': '11006006',
    'Tempelhof-Schöneberg': '11007007', 'Neukölln': '11008008',
    'Treptow-Köpenick': '11009009', 'Marzahn-Hellersdorf': '11010010',
    'Lichtenberg': '11011011', 'Reinickendorf': '11012012'
}
gdf_mapped['district_id'] = gdf_mapped['district'].map(district_mapping)

# --- 6. GEOMETRY TO WKT (NEW STEP) ---
print("Formatting geometry for SQL...")
# Convert the geometry objects into Well-Known Text (WKT) strings
gdf_mapped['geometry'] = gdf_mapped['geometry'].apply(
    lambda x: x.wkt if x is not None else None
)

# --- 7. FINAL EXPORT (UPDATED) ---

# We define the exact order of columns to match the database requirements
final_cols = [
    'id', 
    'district_id', 
    'center_name', 
    'address',        # Added
    'postal_code',    # Added
    'latitude', 
    'longitude', 
    'geometry', 
    'neighborhood', 
    'district', 
    'neighborhood_id'
]

# Create the final dataframe, ensuring we only grab columns that actually exist
df_final = gdf_mapped[[c for c in final_cols if c in gdf_mapped.columns]].copy()

# Add the audit tag
df_final['data_source'] = 'OSM_LOR'

# Save the clean CSV for the SQL \COPY command
os.makedirs("output", exist_ok=True)
df_final.to_csv(OUTPUT_PATH, index=False)

print(f"Success! CSV saved with Address and Postal Code at: {OUTPUT_PATH}")