/*
  # Create batch upsert and demanda management functions

  1. New Functions
    - `upsert_imoveis_batch` - Accepts a JSON array of properties and upserts them all
    - `get_demandas_pendentes` - Returns pending search demands
    - `atualizar_demanda_status` - Updates demand status

  2. Security
    - All functions run as SECURITY DEFINER to bypass RLS
    - Used by the motor_busca scraper
*/

CREATE OR REPLACE FUNCTION public.upsert_imoveis_batch(p_imoveis jsonb)
RETURNS int
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_imovel jsonb;
  v_inserted int := 0;
  v_location geography(Point, 4326);
BEGIN
  FOR v_imovel IN SELECT * FROM jsonb_array_elements(p_imoveis)
  LOOP
    v_location := NULL;
    IF (v_imovel->>'lat')::float <> 0 AND (v_imovel->>'lon')::float <> 0 THEN
      v_location := ST_SetSRID(ST_MakePoint((v_imovel->>'lon')::float, (v_imovel->>'lat')::float), 4326)::geography;
    END IF;

    INSERT INTO imoveis (titulo, link, endereco, cidade, freguesia, tipologia, preco, area_m2, imagem_url, lat, lon, location, mobiliado, fonte, descricao)
    VALUES (
      COALESCE(v_imovel->>'titulo', ''),
      v_imovel->>'link',
      COALESCE(v_imovel->>'endereco', ''),
      COALESCE(v_imovel->>'cidade', ''),
      COALESCE(v_imovel->>'freguesia', ''),
      COALESCE(v_imovel->>'tipologia', ''),
      COALESCE((v_imovel->>'preco')::numeric, 0),
      COALESCE((v_imovel->>'area_m2')::numeric, 0),
      COALESCE(v_imovel->>'imagem_url', ''),
      COALESCE((v_imovel->>'lat')::float, 0),
      COALESCE((v_imovel->>'lon')::float, 0),
      v_location,
      COALESCE((v_imovel->>'mobiliado')::boolean, false),
      COALESCE(v_imovel->>'fonte', ''),
      COALESCE(v_imovel->>'descricao', '')
    )
    ON CONFLICT (link) DO UPDATE SET
      preco = EXCLUDED.preco,
      imagem_url = EXCLUDED.imagem_url,
      descricao = EXCLUDED.descricao,
      mobiliado = EXCLUDED.mobiliado;

    IF NOT FOUND OR xmax = 0 THEN
      v_inserted := v_inserted + 1;
    END IF;
  END LOOP;

  RETURN v_inserted;
END;
$$;

CREATE OR REPLACE FUNCTION public.get_demandas_pendentes_rpc()
RETURNS SETOF demandas
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  RETURN QUERY
    SELECT * FROM demandas
    WHERE status = 'pendente'
    ORDER BY criado_em ASC
    LIMIT 10;
END;
$$;

CREATE OR REPLACE FUNCTION public.atualizar_demanda_status(p_id uuid, p_status text)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  UPDATE demandas SET status = p_status WHERE id = p_id;
END;
$$;
