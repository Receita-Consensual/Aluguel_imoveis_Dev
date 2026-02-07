/*
  # Enable PostGIS Extension

  Enables the PostGIS extension for geographic/spatial queries.
  This is required for distance-based property searches (radius search).
*/

CREATE EXTENSION IF NOT EXISTS postgis SCHEMA extensions;
