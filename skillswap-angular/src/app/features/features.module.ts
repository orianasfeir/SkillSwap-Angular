import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { AuthGuard } from '../core/guards/auth.guard';

const routes: Routes = [
  {
    path: 'dashboard',
    loadChildren: () => import('./dashboard/dashboard.module').then(m => m.DashboardModule),
    canActivate: [AuthGuard]
  },
  {
    path: 'skills',
    loadChildren: () => import('./skills/skills.module').then(m => m.SkillsModule),
    canActivate: [AuthGuard]
  },
  {
    path: 'swaps',
    loadChildren: () => import('./swaps/swaps.module').then(m => m.SwapsModule),
    canActivate: [AuthGuard]
  },
  {
    path: 'reviews',
    loadChildren: () => import('./reviews/reviews.module').then(m => m.ReviewsModule),
    canActivate: [AuthGuard]
  },
  {
    path: '',
    redirectTo: 'dashboard',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [
    SharedModule,
    RouterModule.forChild(routes)
  ]
})
export class FeaturesModule { } 