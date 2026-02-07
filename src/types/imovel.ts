export interface Imovel {
  id: string;
  titulo: string;
  link: string;
  endereco: string;
  cidade: string;
  freguesia: string;
  tipologia: string;
  preco: number;
  area_m2: number;
  imagem_url: string;
  lat: number;
  lon: number;
  mobiliado: boolean;
  fonte: string;
  descricao: string;
  criado_em: string;
  dist_metros?: number;
}

export interface SearchFilters {
  tipologias: string[];
  precoMin: number;
  precoMax: number;
  areaMin: number;
  areaMax: number;
  mobiliado: 'todos' | 'sim' | 'nao';
}

export interface SearchState {
  query: string;
  lat: number;
  lon: number;
  raioMetros: number;
  isSearching: boolean;
  hasSearched: boolean;
}
