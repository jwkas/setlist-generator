import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { SongListComponent } from './components/song-list/song-list.component';
import { SongFormComponent } from './components/song-form/song-form.component';
import { SetlistGeneratorComponent } from './components/setlist-generator/setlist-generator.component';
import { SetlistViewComponent } from './components/setlist-view/setlist-view.component';
import { CsvUploadComponent } from './components/csv-upload/csv-upload.component';
import { NavbarComponent } from './components/navbar/navbar.component';

const routes: Routes = [
  { path: '', redirectTo: '/songs', pathMatch: 'full' },
  { path: 'songs', component: SongListComponent },
  { path: 'songs/add', component: SongFormComponent },
  { path: 'songs/edit/:id', component: SongFormComponent },
  { path: 'songs/upload', component: CsvUploadComponent },
  { path: 'generate', component: SetlistGeneratorComponent },
  { path: 'setlists/:id', component: SetlistViewComponent },
  { path: '**', redirectTo: '/songs' }
];

@NgModule({
  declarations: [
    AppComponent,
    SongListComponent,
    SongFormComponent,
    SetlistGeneratorComponent,
    SetlistViewComponent,
    CsvUploadComponent,
    NavbarComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule.forRoot(routes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
