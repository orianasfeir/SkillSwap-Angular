import { Routes } from '@angular/router';

export const SKILLS_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./skills.component').then(m => m.SkillsComponent)
  }
]; 