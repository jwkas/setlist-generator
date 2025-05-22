export interface Song {
  id?: number;
  title: string;
  artist: string;
  tempo?: number;
  tempo_category?: string;
  intensity?: string;
  lead_vocalist?: string;
  key?: string;
  is_minor?: boolean;
  is_original?: boolean;
  is_hit?: boolean;
  duration?: number;
  created_at?: string;
  updated_at?: string;
}
