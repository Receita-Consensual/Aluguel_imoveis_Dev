/*
  # Create Spatial Query Functions

  1. Functions
    - `imoveis_no_raio(lat, lon, raio_metros)` - Returns properties within a radius, ordered by distance
    - `imoveis_na_viewport(min_lat, min_lon, max_lat, max_lon)` - Returns properties visible in map viewport

  These functions use PostGIS ST_DWithin and ST_Distance for efficient geographic queries.
  The GiST index on the location column ensures fast spatial lookups.
*/

CREATE OR REPLACE FUNCTION imoveis_no_raio(
  p_lat float,
  p_lon float,
  p_raio_metros float DEFAULT 2000
)
RETURNS TABLE (
  id uuid,
  titulo text,
  link text,
  endereco text,
  cidade text,
  freguesia text,
  tipologia text,
  preco numeric,
  area_m2 numeric,
  imagem_url text,
  lat float,
  lon float,
  mobiliado boolean,
  fonte text,
  descricao text,
  criado_em timestamptz,
  dist_metros float
)
LANGUAGE sql
STABLE
AS $$
  SELECT
    i.id, i.titulo, i.link, i.endereco, i.cidade, i.freguesia,
    i.tipologia, i.preco, i.area_m2, i.imagem_url, i.lat, i.lon,
    i.mobiliado, i.fonte, i.descricao, i.criado_em,
    extensions.ST_Distance(
      i.location,
      extensions.ST_SetSRID(extensions.ST_MakePoint(p_lon, p_lat), 4326)::extensions.geography
    ) AS dist_metros
  FROM imoveis i
  WHERE i.location IS NOT NULL
    AND extensions.ST_DWithin(
      i.location,
      extensions.ST_SetSRID(extensions.ST_MakePoint(p_lon, p_lat), 4326)::extensions.geography,
      p_raio_metros
    )
  ORDER BY dist_metros ASC;
$$;

CREATE OR REPLACE FUNCTION imoveis_na_viewport(
  p_min_lat float,
  p_min_lon float,
  p_max_lat float,
  p_max_lon float
)
RETURNS TABLE (
  id uuid,
  titulo text,
  link text,
  endereco text,
  cidade text,
  freguesia text,
  tipologia text,
  preco numeric,
  area_m2 numeric,
  imagem_url text,
  lat float,
  lon float,
  mobiliado boolean,
  fonte text,
  descricao text,
  criado_em timestamptz
)
LANGUAGE sql
STABLE
AS $$
  SELECT
    i.id, i.titulo, i.link, i.endereco, i.cidade, i.freguesia,
    i.tipologia, i.preco, i.area_m2, i.imagem_url, i.lat, i.lon,
    i.mobiliado, i.fonte, i.descricao, i.criado_em
  FROM imoveis i
  WHERE i.location IS NOT NULL
    AND i.location OPERATOR(extensions.&&) extensions.ST_SetSRID(
      extensions.ST_MakeBox2D(
        extensions.ST_Point(p_min_lon, p_min_lat),
        extensions.ST_Point(p_max_lon, p_max_lat)
      ),
      4326
    )
  LIMIT 200;
$$;
