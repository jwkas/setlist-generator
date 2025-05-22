import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { SongService } from '../../services/song.service';

@Component({
  selector: 'app-csv-upload',
  templateUrl: './csv-upload.component.html',
  styleUrls: ['./csv-upload.component.scss']
})
export class CsvUploadComponent {
  selectedFile: File | null = null;
  uploading = false;
  error = '';
  success = '';
  
  constructor(
    private songService: SongService,
    private router: Router
  ) { }

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0] ?? null;
    
    // Reset messages
    this.error = '';
    this.success = '';
  }

  uploadFile(): void {
    if (!this.selectedFile) {
      this.error = 'Please select a CSV file to upload';
      return;
    }

    if (!this.selectedFile.name.endsWith('.csv')) {
      this.error = 'Only CSV files are supported';
      return;
    }

    this.uploading = true;
    this.error = '';
    this.success = '';

    this.songService.uploadSongs(this.selectedFile).subscribe({
      next: (response) => {
        this.uploading = false;
        this.success = response.message || 'Songs uploaded successfully';
        this.selectedFile = null;
        
        // Reset the file input
        const fileInput = document.getElementById('csvFile') as HTMLInputElement;
        if (fileInput) {
          fileInput.value = '';
        }
      },
      error: (err) => {
        this.uploading = false;
        this.error = 'Failed to upload songs. Please check your CSV file format and try again.';
        console.error('Error uploading songs:', err);
      }
    });
  }

  downloadSampleCsv(): void {
    // Create a link to download the sample CSV
    const link = document.createElement('a');
    link.href = '/assets/sample_songs.csv';
    link.download = 'sample_songs.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  navigateToSongList(): void {
    this.router.navigate(['/songs']);
  }
}
