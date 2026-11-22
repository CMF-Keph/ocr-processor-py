import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { TextEntry } from '../interfaces/text-entry';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class Ocr {
  private baseUrl = "http://127.0.0.1:8000/api"
  private httpClient = inject(HttpClient);

  getLatest(): Observable<TextEntry> {
    return this.httpClient.get<TextEntry>(`${this.baseUrl}/texts/latest`);  
  } 
}
