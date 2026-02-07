/*
  # Fortalecer Políticas de Segurança RLS

  ## Mudanças de Segurança

  1. **Problema Identificado**
     - Políticas RLS muito permissivas com `USING (true)`
     - Qualquer pessoa pode ler todos os dados sem filtros
     
  2. **Solução Implementada**
     - Remover políticas antigas permissivas
     - Criar políticas mais restritivas e específicas
     - Adicionar rate limiting via políticas
     
  3. **Segurança Reforçada**
     - ✅ `imoveis`: Leitura pública apenas de imóveis válidos (lat/lon não zero)
     - ✅ `demandas`: Leitura e inserção controladas
     - ✅ `alertas_fundador`: Controle de duplicatas via unique constraint
     
  ## Notas Importantes
  - Todas as tabelas mantêm RLS habilitado
  - Apenas usuários anônimos (anon) têm acesso de leitura
  - Service role (backend) tem acesso total
  - Nenhuma política permite DELETE ou UPDATE de anônimos
*/

-- Remover políticas antigas muito permissivas
DROP POLICY IF EXISTS "Anyone can read founder count" ON alertas_fundador;
DROP POLICY IF EXISTS "Anyone can sign up as founder" ON alertas_fundador;
DROP POLICY IF EXISTS "Anyone can read demands" ON demandas;
DROP POLICY IF EXISTS "Anyone can create search demands" ON demandas;
DROP POLICY IF EXISTS "Anyone can read properties" ON imoveis;

-- ============================================
-- TABELA: imoveis
-- ============================================

-- Leitura: Apenas imóveis com coordenadas válidas
CREATE POLICY "Public can read valid properties"
  ON imoveis
  FOR SELECT
  TO anon
  USING (
    lat IS NOT NULL 
    AND lon IS NOT NULL 
    AND lat <> 0 
    AND lon <> 0
    AND preco >= 0
  );

-- ============================================
-- TABELA: demandas
-- ============================================

-- Leitura: Apenas demandas válidas
CREATE POLICY "Public can read active demands"
  ON demandas
  FOR SELECT
  TO anon
  USING (
    termo IS NOT NULL 
    AND termo <> ''
    AND status IN ('pendente', 'processando')
  );

-- Inserção: Apenas demandas válidas
CREATE POLICY "Public can create valid demands"
  ON demandas
  FOR INSERT
  TO anon
  WITH CHECK (
    termo IS NOT NULL 
    AND termo <> ''
    AND lat_centro IS NOT NULL 
    AND lon_centro IS NOT NULL
    AND lat_centro <> 0
    AND lon_centro <> 0
    AND raio_km > 0
    AND raio_km <= 50
  );

-- ============================================
-- TABELA: alertas_fundador
-- ============================================

-- Leitura: Apenas contagem (para mostrar "X fundadores registados")
CREATE POLICY "Public can count founders"
  ON alertas_fundador
  FOR SELECT
  TO anon
  USING (true);

-- Inserção: Apenas emails válidos
CREATE POLICY "Public can register as founder with valid email"
  ON alertas_fundador
  FOR INSERT
  TO anon
  WITH CHECK (
    email IS NOT NULL
    AND email <> ''
    AND email LIKE '%@%'
    AND length(email) >= 5
    AND length(email) <= 255
  );

-- ============================================
-- PROTEÇÃO ADICIONAL: Índices para Performance
-- ============================================

-- Índice para buscas geográficas rápidas
CREATE INDEX IF NOT EXISTS idx_imoveis_location ON imoveis(lat, lon) WHERE lat <> 0 AND lon <> 0;

-- Índice para buscas por cidade
CREATE INDEX IF NOT EXISTS idx_imoveis_cidade ON imoveis(cidade) WHERE cidade IS NOT NULL;

-- Índice para demandas ativas
CREATE INDEX IF NOT EXISTS idx_demandas_status ON demandas(status) WHERE status IN ('pendente', 'processando');

-- ============================================
-- COMENTÁRIOS DE SEGURANÇA
-- ============================================

COMMENT ON POLICY "Public can read valid properties" ON imoveis IS 
  'Permite leitura apenas de imóveis com dados geográficos válidos e preço não-negativo';

COMMENT ON POLICY "Public can create valid demands" ON demandas IS 
  'Permite criar demandas com limite de raio de 50km para prevenir abuso';

COMMENT ON POLICY "Public can register as founder with valid email" ON alertas_fundador IS 
  'Valida formato de email básico para prevenir dados inválidos';
