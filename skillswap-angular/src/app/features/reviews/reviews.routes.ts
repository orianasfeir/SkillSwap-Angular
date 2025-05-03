import { Routes } from '@angular/router';

export const REVIEWS_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./reviews.component').then(m => m.ReviewsComponent)
  }
]; 