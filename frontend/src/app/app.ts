import { Component, inject, OnDestroy, OnInit, signal } from '@angular/core';
import { TextEntry } from './interfaces/text-entry';
import { Ocr } from './services/ocr';
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-root',
  imports: [],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit, OnDestroy {
  texts = signal<TextEntry[]>([]);
  selectedText = signal<TextEntry | undefined>(undefined);
  latestText = signal<TextEntry | undefined>(undefined);

  ocrService = inject(Ocr);
  
  pollingInterval: number = 0;

  async pollLastestText(): Promise<void> {
    const data = await firstValueFrom(this.ocrService.getLatest());    

    if (this.latestText() === undefined) {
      this.latestText.set(data);
      return;
    }

    if (data.id === this.latestText()!.id)
      return;

    this.texts.update(entries => [...entries, data]);
    this.latestText.set(data);
    this.selectedText.set(data);
  }

  ngOnInit(): void {
    this.pollingInterval = setInterval(() => {
      this.pollLastestText();
    }, 500);
  }

  ngOnDestroy(): void {
    clearInterval(this.pollingInterval);
  }

  selectText(id: number): void {
    const text = this.texts().find(text => text.id === id);

    if (!text) return;

    this.selectedText.set(text);
  }  

  updateText(e: Event, id?: number,): void {
    if (!id) return;

    const text = this.texts().find(text => text.id === id);

    if (!text) return;
    
    text.text = (e.target as HTMLTextAreaElement)?.value;
  }
}

