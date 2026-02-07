/*
  # Create Core Tables for Lugar Portugal

  1. New Tables
    - `imoveis` - Property listings scraped from Idealista, SAPO, etc.
      - `id` (uuid, primary key)
      - `titulo` (text) - Property title
      - `link` (text, unique) - Direct link to original listing
      - `endereco` (text) - Street address
      - `cidade` (text) - City name
      - `freguesia` (text) - Parish/neighborhood
      - `tipologia` (text) - T0, T1, T2, T3, T4, T5+, moradia, quarto
      - `preco` (numeric) - Monthly rent in EUR
      - `area_m2` (numeric) - Area in square meters
      - `imagem_url` (text) - Photo URL
      - `lat` (float) - Latitude
      - `lon` (float) - Longitude
      - `location` (geography point) - PostGIS geography for distance queries
      - `mobiliado` (boolean) - Furnished or not
      - `fonte` (text) - Source site (idealista, sapo, olx)
      - `descricao` (text) - Description text
      - `criado_em` (timestamptz) - Created timestamp

    - `demandas` - On-demand search requests from users
      - `id` (uuid, primary key)
      - `termo` (text) - Search term
      - `lat_centro` (float) - Center latitude
      - `lon_centro` (float) - Center longitude
      - `raio_km` (float) - Search radius in km
      - `status` (text) - pendente, processando, concluido
      - `criado_em` (timestamptz)

    - `alertas_fundador` - Founder member email signups
      - `id` (uuid, primary key)
      - `email` (text, unique) - Email address
      - `criado_em` (timestamptz)

  2. Security
    - RLS enabled on all tables
    - Public read access for imoveis (anon SELECT)
    - Public insert for demandas (anon INSERT) and alertas_fundador (anon INSERT)
    - No update/delete for anon users

  3. Indexes
    - GiST index on imoveis.location for spatial queries
    - Index on imoveis.cidade for city filtering
    - Index on imoveis.tipologia for type filtering
*/

CREATE TABLE IF NOT EXISTS imoveis (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  titulo text NOT NULL DEFAULT '',
  link text UNIQUE NOT NULL,
  endereco text DEFAULT '',
  cidade text DEFAULT '',
  freguesia text DEFAULT '',
  tipologia text DEFAULT '',
  preco numeric DEFAULT 0,
  area_m2 numeric DEFAULT 0,
  imagem_url text DEFAULT '',
  lat float DEFAULT 0,
  lon float DEFAULT 0,
  location extensions.geography(Point, 4326),
  mobiliado boolean DEFAULT false,
  fonte text DEFAULT '',
  descricao text DEFAULT '',
  criado_em timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS demandas (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  termo text NOT NULL DEFAULT '',
  lat_centro float DEFAULT 0,
  lon_centro float DEFAULT 0,
  raio_km float DEFAULT 2,
  status text DEFAULT 'pendente',
  criado_em timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS alertas_fundador (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email text UNIQUE NOT NULL,
  criado_em timestamptz DEFAULT now()
);

ALTER TABLE imoveis ENABLE ROW LEVEL SECURITY;
ALTER TABLE demandas ENABLE ROW LEVEL SECURITY;
ALTER TABLE alertas_fundador ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can read properties"
  ON imoveis FOR SELECT
  TO anon
  USING (lat != 0 AND lon != 0);

CREATE POLICY "Anyone can create search demands"
  ON demandas FOR INSERT
  TO anon
  WITH CHECK (termo != '' AND lat_centro != 0 AND lon_centro != 0);

CREATE POLICY "Anyone can read demands"
  ON demandas FOR SELECT
  TO anon
  USING (true);

CREATE POLICY "Anyone can sign up as founder"
  ON alertas_fundador FOR INSERT
  TO anon
  WITH CHECK (email != '');

CREATE POLICY "Anyone can read founder count"
  ON alertas_fundador FOR SELECT
  TO anon
  USING (true);

CREATE INDEX IF NOT EXISTS idx_imoveis_location ON imoveis USING GIST (location);
CREATE INDEX IF NOT EXISTS idx_imoveis_cidade ON imoveis (cidade);
CREATE INDEX IF NOT EXISTS idx_imoveis_tipologia ON imoveis (tipologia);
CREATE INDEX IF NOT EXISTS idx_imoveis_preco ON imoveis (preco);
