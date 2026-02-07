/*
  # Create upsert_imovel RPC function

  1. New Functions
    - `upsert_imovel` - SECURITY DEFINER function that allows the motor_busca
      to insert/update properties without needing the service role key.
      It receives all property fields and performs an upsert based on the link.

  2. Security
    - Function runs as the table owner (SECURITY DEFINER) to bypass RLS
    - Only performs insert/update operations on the imoveis table
*/

CREATE OR REPLACE FUNCTION public.upsert_imovel(
  p_titulo text,
  p_link text,
  p_endereco text DEFAULT '',
  p_cidade text DEFAULT '',
  p_freguesia text DEFAULT '',
  p_tipologia text DEFAULT '',
  p_preco numeric DEFAULT 0,
  p_area_m2 numeric DEFAULT 0,
  p_imagem_url text DEFAULT '',
  p_lat double precision DEFAULT 0,
  p_lon double precision DEFAULT 0,
  p_mobiliado boolean DEFAULT false,
  p_fonte text DEFAULT '',
  p_descricao text DEFAULT ''
)
RETURNS text
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_location geography(Point, 4326);
  v_result text;
BEGIN
  IF p_lat <> 0 AND p_lon <> 0 THEN
    v_location := ST_SetSRID(ST_MakePoint(p_lon, p_lat), 4326)::geography;
  END IF;

  INSERT INTO imoveis (titulo, link, endereco, cidade, freguesia, tipologia, preco, area_m2, imagem_url, lat, lon, location, mobiliado, fonte, descricao)
  VALUES (p_titulo, p_link, p_endereco, p_cidade, p_freguesia, p_tipologia, p_preco, p_area_m2, p_imagem_url, p_lat, p_lon, v_location, p_mobiliado, p_fonte, p_descricao)
  ON CONFLICT (link) DO UPDATE SET
    preco = EXCLUDED.preco,
    imagem_url = EXCLUDED.imagem_url,
    descricao = EXCLUDED.descricao,
    mobiliado = EXCLUDED.mobiliado
  RETURNING CASE WHEN xmax = 0 THEN 'inserted' ELSE 'updated' END INTO v_result;

  RETURN v_result;
END;
$$;
