import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Observable } from 'rxjs';
import { SkillsService, Skill } from '../../core/services/skills.service';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { AddSkillDialogComponent } from './add-skill-dialog/add-skill-dialog.component';

@Component({
  selector: 'app-skills',
  standalone: true,
  imports: [CommonModule, HttpClientModule, ReactiveFormsModule],
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
            <div class="px-4 py-8 sm:px-0">
              <h2 class="text-2xl font-semibold mb-4">Your Skills</h2>
              <div *ngIf="userSkills$ | async as userSkills; else loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div *ngFor="let skill of userSkills" class="border rounded-lg p-4 bg-white shadow">
                  <h2 class="text-xl font-semibold">{{ skill.name }}</h2>
                  <p class="text-gray-600">{{ skill.description }}</p>
                </div>
              </div>

              <h2 class="text-2xl font-semibold mt-8 mb-4">All Skills</h2>
              <div *ngIf="skills$ | async as skills; else loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div *ngFor="let skill of skills" class="border rounded-lg p-4 bg-white shadow">
                  <h2 class="text-xl font-semibold">{{ skill.name }}</h2>
                  <p class="text-gray-600">{{ skill.description }}</p>
                  <button (click)="openAddSkillDialog(skill.id)" class="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">
                    Add
                  </button>
                </div>
              </div>
              <ng-template #loading>
                <p class="text-center mt-8 text-gray-500">Loading...</p>
              </ng-template>
            </div>
          </div>
        </main>
      </div>
    </div>
  `
})
export class SkillsComponent implements OnInit {
  skills$!: Observable<Skill[]>;
  userSkills$!: Observable<Skill[]>;

  constructor(private skillsService: SkillsService, private fb: FormBuilder, private dialog: MatDialog) {}

  ngOnInit(): void {
    this.skills$ = this.skillsService.getSkills();
    this.userSkills$ = this.skillsService.getUserSkills();
  }

  openAddSkillDialog(skillId: number): void {
    const dialogRef = this.dialog.open(AddSkillDialogComponent, {
      width: '400px',
      data: { skillId }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.skillsService.addUserSkill(result).subscribe(() => {
          console.log('Skill added successfully');
          this.userSkills$ = this.skillsService.getUserSkills(); // Refresh user skills
        });
      }
    });
  }
}