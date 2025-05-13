import { Routes } from '@angular/router';

export const SKILLS_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./skills.component').then((m) => m.SkillsComponent),
  },
  {
    path: ':id',
    loadComponent: () =>
      import('./skill-detail/skill-detail.component').then((m) => m.SkillDetailComponent),
  },
];