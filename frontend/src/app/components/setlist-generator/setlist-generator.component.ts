import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { SetlistService } from '../../services/setlist.service';

@Component({
  selector: 'app-setlist-generator',
  templateUrl: './setlist-generator.component.html',
  styleUrls: ['./setlist-generator.component.scss']
})
export class SetlistGeneratorComponent implements OnInit {
  generatorForm!: FormGroup;
  generating = false;
  error = '';
  
  constructor(
    private fb: FormBuilder,
    private setlistService: SetlistService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.initForm();
  }

  initForm(): void {
    const today = new Date().toISOString().split('T')[0];
    
    this.generatorForm = this.fb.group({
      name: ['', [Validators.required]],
      date: [today],
      venue: [''],
      target_duration: [3600, [Validators.required, Validators.min(600)]] // Minimum 10 minutes (600 seconds)
    });
  }

  onSubmit(): void {
    if (this.generatorForm.invalid) {
      // Mark all fields as touched to trigger validation messages
      Object.keys(this.generatorForm.controls).forEach(key => {
        this.generatorForm.get(key)?.markAsTouched();
      });
      return;
    }

    this.generating = true;
    this.error = '';

    this.setlistService.generateSetlist(this.generatorForm.value).subscribe({
      next: (setlist) => {
        this.generating = false;
        // Navigate to the setlist view page
        this.router.navigate(['/setlists', setlist.id]);
      },
      error: (err) => {
        this.generating = false;
        this.error = err.error?.error || 'Failed to generate setlist. Please try again later.';
        console.error('Error generating setlist:', err);
      }
    });
  }

  // Helper method to convert duration from hours and minutes to seconds
  convertDurationToSeconds(hours: number | string, minutes: number | string): number {
    const hoursNum = typeof hours === 'string' ? parseInt(hours, 10) : hours;
    const minutesNum = typeof minutes === 'string' ? parseInt(minutes, 10) : minutes;
    return (hoursNum * 3600) + (minutesNum * 60);
  }

  // Helper method to extract hours and minutes from duration in seconds
  extractDurationComponents(durationInSeconds: number): { hours: number, minutes: number } {
    const hours = Math.floor(durationInSeconds / 3600);
    const minutes = Math.floor((durationInSeconds % 3600) / 60);
    
    return { hours, minutes };
  }

  // Update the form when hours/minutes inputs change
  updateDuration(hours: number | string, minutes: number | string): void {
    const hoursNum = typeof hours === 'string' ? parseInt(hours, 10) || 0 : hours;
    const minutesNum = typeof minutes === 'string' ? parseInt(minutes, 10) || 0 : minutes;
    const totalSeconds = this.convertDurationToSeconds(hoursNum, minutesNum);
    this.generatorForm.patchValue({ target_duration: totalSeconds });
  }
}
