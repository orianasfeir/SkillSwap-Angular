import { Routes } from '@angular/router';

export const SWAPS_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./swaps.component').then(m => m.SwapsComponent)
  }
]; 