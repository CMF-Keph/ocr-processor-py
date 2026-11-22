import { Component, inject, OnDestroy, OnInit, signal } from '@angular/core';
import { TextEntry } from './interfaces/text-entry';
import { Ocr } from './services/ocr';
import { firstValueFrom } from 'rxjs';
import { NgClass } from '../../node_modules/@angular/common/types/_common_module-chunk';

@Component({
  selector: 'app-root',
  imports: [],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit, OnDestroy {
  texts = signal<TextEntry[]>([]);
  latestText = signal<TextEntry | undefined>(undefined);

  ocrService = inject(Ocr);
  
  pollingInterval: number = 0;

  async pollLastestText(): Promise<void> {
    const data = await firstValueFrom(this.ocrService.getLatest());

    console.log(data);

    if (this.latestText() === undefined) {
      this.latestText.set(data);
      return;
    }

    if (data.id === this.latestText()!.id)
      return;

    this.texts.update(entries => [...entries, this.latestText()!]);
    this.latestText.set(data);
  }

  ngOnInit(): void {
    this.pollingInterval = setInterval(() => {
      this.pollLastestText();
    }, 500);
  }

  ngOnDestroy(): void {
    clearInterval(this.pollingInterval);
  }
}

