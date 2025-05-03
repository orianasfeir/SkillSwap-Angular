import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-skills',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="min-h-screen bg-gray-100">
      <div class="py-10">
        <header>
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 class="text-3xl font-bold leading-tight text-gray-900">
              Skills
            </h1>
          </div>
        </header>
        <main>
          <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <!-- Skills content will go here -->
            <div class="px-4 py-8 sm:px-0">
              <div class="border-4 border-dashed border-gray-200 rounded-lg h-96">
                <p class="text-center mt-8 text-gray-500">Skills content coming soon...</p>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  `
})
export class SkillsComponent {} 