import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Setlist } from '../../models/setlist.model';
import { SetlistService } from '../../services/setlist.service';

@Component({
  selector: 'app-setlist-view',
  templateUrl: './setlist-view.component.html',
  styleUrls: ['./setlist-view.component.scss']
})
export class SetlistViewComponent implements OnInit {
  setlist: Setlist | null = null;
  loading = true;
  error = '';
  
  constructor(
    private setlistService: SetlistService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      if (params['id']) {
        this.loadSetlist(+params['id']);
      } else {
        this.error = 'Setlist ID not provided';
        this.loading = false;
      }
    });
  }

  loadSetlist(id: number): void {
    this.loading = true;
    this.setlistService.getSetlist(id).subscribe({
      next: (setlist) => {
        this.setlist = setlist;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load setlist. Please try again later.';
        this.loading = false;
        console.error('Error loading setlist:', err);
      }
    });
  }

  deleteSetlist(): void {
    if (!this.setlist || !this.setlist.id) return;
    
    if (confirm('Are you sure you want to delete this setlist?')) {
      this.setlistService.deleteSetlist(this.setlist.id).subscribe({
        next: () => {
          this.router.navigate(['/songs']);
        },
        error: (err) => {
          this.error = 'Failed to delete setlist. Please try again later.';
          console.error('Error deleting setlist:', err);
        }
      });
    }
  }

  // Helper methods for displaying song information
  getKeyTypeClass(isMinor: boolean | undefined): string {
    return isMinor ? 'badge bg-secondary' : 'badge bg-primary';
  }

  getKeyTypeLabel(isMinor: boolean | undefined): string {
    return isMinor ? 'Minor' : 'Major';
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

  getOriginalClass(isOriginal: boolean | undefined): string {
    return isOriginal ? 'badge bg-success' : 'badge bg-warning text-dark';
  }

  getOriginalLabel(isOriginal: boolean | undefined): string {
    return isOriginal ? 'Original' : 'Cover';
  }

  formatDuration(seconds: number | undefined): string {
    if (!seconds) return 'N/A';
    
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  }

  formatTotalDuration(seconds: number | undefined): string {
    if (!seconds) return 'N/A';
    
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;
    
    if (hours > 0) {
      return `${hours}h ${minutes}m ${remainingSeconds}s`;
    } else {
      return `${minutes}m ${remainingSeconds}s`;
    }
  }

  // Print the setlist
  printSetlist(): void {
    window.print();
  }
}
