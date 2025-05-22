import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Song } from '../../models/song.model';
import { SongService } from '../../services/song.service';

@Component({
  selector: 'app-song-form',
  templateUrl: './song-form.component.html',
  styleUrls: ['./song-form.component.scss']
})
export class SongFormComponent implements OnInit {
  songForm!: FormGroup;
  isEditMode = false;
  songId?: number;
  loading = false;
  submitting = false;
  error = '';
  
  tempoCategories = ['slow', 'medium', 'fast'];
  intensityLevels = ['low', 'medium', 'high'];
  
  constructor(
    private fb: FormBuilder,
    private songService: SongService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.initForm();
    
    // Check if we're in edit mode
    this.route.params.subscribe((params: { [key: string]: string }) => {
      if (params['id']) {
        this.isEditMode = true;
        this.songId = +params['id'];
        this.loadSong(this.songId);
      }
    });
  }

  initForm(): void {
    this.songForm = this.fb.group({
      title: ['', [Validators.required]],
      artist: ['', [Validators.required]],
      tempo: [null, [Validators.min(1)]],
      tempo_category: [''],
      intensity: [''],
      lead_vocalist: [''],
      key: [''],
      is_minor: [false],
      is_original: [true],
      is_hit: [false],
      duration: [null, [Validators.min(1)]]
    });
  }

  loadSong(id: number): void {
    this.loading = true;
    this.songService.getSong(id).subscribe({
      next: (song: Song) => {
        this.songForm.patchValue(song);
        this.loading = false;
      },
      error: (err: any) => {
        this.error = 'Failed to load song. Please try again later.';
        this.loading = false;
        console.error('Error loading song:', err);
      }
    });
  }

  onSubmit(): void {
    if (this.songForm.invalid) {
      // Mark all fields as touched to trigger validation messages
      Object.keys(this.songForm.controls).forEach(key => {
        this.songForm.get(key)?.markAsTouched();
      });
      return;
    }

    const songData: Song = this.songForm.value;
    this.submitting = true;

    if (this.isEditMode && this.songId) {
      // Update existing song
      this.songService.updateSong(this.songId, songData).subscribe({
        next: () => {
          this.router.navigate(['/songs']);
        },
        error: (err: any) => {
          this.error = 'Failed to update song. Please try again.';
          this.submitting = false;
          console.error('Error updating song:', err);
        }
      });
    } else {
      // Create new song
      this.songService.createSong(songData).subscribe({
        next: () => {
          this.router.navigate(['/songs']);
        },
        error: (err: any) => {
          this.error = 'Failed to create song. Please try again.';
          this.submitting = false;
          console.error('Error creating song:', err);
        }
      });
    }
  }

  // Helper method to convert duration from minutes:seconds to seconds
  convertDurationToSeconds(minutes: number, seconds: number): number {
    return (minutes * 60) + seconds;
  }

  // Helper method to extract minutes and seconds from duration in seconds
  extractDurationComponents(durationInSeconds?: number): { minutes: number, seconds: number } {
    if (!durationInSeconds) {
      return { minutes: 0, seconds: 0 };
    }
    
    const minutes = Math.floor(durationInSeconds / 60);
    const seconds = durationInSeconds % 60;
    
    return { minutes, seconds };
  }
}
