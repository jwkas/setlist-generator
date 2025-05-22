import { Song } from './song.model';

export interface Setlist {
  id?: number;
  name: string;
  date?: string;
  venue?: string;
  total_duration?: number;
  songs?: Song[];
  created_at?: string;
  updated_at?: string;
}
