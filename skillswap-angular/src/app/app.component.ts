import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from './shared/components/header/header.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, HeaderComponent],
  template: `
    <app-header></app-header>
    <main class="container mx-auto py-4">
      <router-outlet />
    </main>
  `,
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'skillswap-angular';
}
