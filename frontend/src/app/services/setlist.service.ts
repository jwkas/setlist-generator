import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Setlist } from '../models/setlist.model';

interface SetlistGenerationParams {
  target_duration?: number;
  name?: string;
  date?: string;
  venue?: string;
}

@Injectable({
  providedIn: 'root'
})
export class SetlistService {
  private apiUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) { }

  // Get all setlists
  getSetlists(): Observable<Setlist[]> {
    return this.http.get<Setlist[]>(`${this.apiUrl}/setlists`);
  }

  // Get a single setlist by ID
  getSetlist(id: number): Observable<Setlist> {
    return this.http.get<Setlist>(`${this.apiUrl}/setlists/${id}`);
  }

  // Create a new setlist manually
  createSetlist(setlist: Setlist): Observable<Setlist> {
    return this.http.post<Setlist>(`${this.apiUrl}/setlists`, setlist);
  }

  // Delete a setlist
  deleteSetlist(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/setlists/${id}`);
  }

  // Generate a setlist based on parameters
  generateSetlist(params: SetlistGenerationParams): Observable<Setlist> {
    return this.http.post<Setlist>(`${this.apiUrl}/generate-setlist`, params);
  }
}
