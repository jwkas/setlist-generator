import { Component, OnInit } from '@angular/core';
import { Song } from '../../models/song.model';
import { SongService } from '../../services/song.service';

@Component({
  selector: 'app-song-list',
  templateUrl: './song-list.component.html',
  styleUrls: ['./song-list.component.scss']
})
export class SongListComponent implements OnInit {
  songs: Song[] = [];
  loading = true;
  error = '';

  constructor(private songService: SongService) { }

  ngOnInit(): void {
    this.loadSongs();
  }

  loadSongs(): void {
    this.loading = true;
    this.songService.getSongs().subscribe({
      next: (data) => {
        this.songs = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load songs. Please try again later.';
        this.loading = false;
        console.error('Error loading songs:', err);
      }
    });
  }

  deleteSong(id: number): void {
    if (confirm('Are you sure you want to delete this song?')) {
      this.songService.deleteSong(id).subscribe({
        next: () => {
          this.songs = this.songs.filter(song => song.id !== id);
        },
        error: (err) => {
          this.error = 'Failed to delete song. Please try again later.';
          console.error('Error deleting song:', err);
        }
      });
    }
  }

  // Helper methods for displaying song information
  getKeyTypeClass(song: Song): string {
    return song.is_minor ? 'badge bg-secondary' : 'badge bg-primary';
  }

  getKeyTypeLabel(song: Song): string {
    return song.is_minor ? 'Minor' : 'Major';
  }

  getTempoClass(category: string | undefined): string {
    if (!category) return 'badge bg-secondary';
    
    switch (category.toLowerCase()) {
      case 'slow': return 'badge bg-info';
      case 'medium': return 'badge bg-primary';
      case 'fast': return 'badge bg-danger';
      default: return 'badge bg-secondary';
    }
  }

  getOriginalClass(song: Song): string {
    return song.is_original ? 'badge bg-success' : 'badge bg-warning text-dark';
  }

  getOriginalLabel(song: Song): string {
    return song.is_original ? 'Original' : 'Cover';
  }

  getHitClass(song: Song): string {
    return song.is_hit ? 'badge bg-danger' : 'badge bg-secondary';
  }

  formatDuration(seconds: number | undefined): string {
    if (!seconds) return 'N/A';
    
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  }
}
