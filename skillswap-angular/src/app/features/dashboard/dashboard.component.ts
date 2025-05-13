import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { catchError, finalize, of } from 'rxjs';
import { EditProfileDialogComponent } from './edit-profile-dialog/edit-profile-dialog.component';
import { LoadingSpinnerComponent } from '../../shared/components/loading-spinner/loading-spinner.component';
import { UserService, ProfileResponse } from '../../core/services/user.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    MatButtonModule,
    MatCardModule,
    MatDialogModule,
    MatIconModule,
    MatSnackBarModule,
    LoadingSpinnerComponent
  ],
  template: `
    <div class="min-h-screen bg-gray-100">
      <div class="py-10">
        <header>
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 class="text-3xl font-bold leading-tight text-gray-900">Dashboard</h1>
          </div>
        </header>
        <main>
          <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <!-- Loading State -->
            <app-loading-spinner *ngIf="isLoading"></app-loading-spinner>

            <!-- Error State -->
            <div *ngIf="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
              <strong class="font-bold">Error!</strong>
              <span class="block sm:inline">{{ error }}</span>
            </div>

            <!-- Content -->
            <ng-container *ngIf="!isLoading && !error && profileData">
              <!-- Profile Section -->
              <div class="mt-8">
                <div class="bg-white shadow rounded-lg p-6">
                  <div class="flex items-center space-x-4">
                    <img [src]="getProfileImageUrl(profileData.user.profile_image)"
                         class="w-24 h-24 rounded-full object-cover"
                         alt="Profile picture">
                    <div class="flex-1">
                      <h2 class="text-2xl font-bold">{{ profileData.user.username }}</h2>
                      <p class="text-gray-600">{{ profileData.user.about || 'No bio yet' }}</p>
                      <p class="text-sm text-gray-500">Member since {{ profileData.user.created_at | date }}</p>
                      <p class="text-sm text-gray-500" *ngIf="profileData.user.phone">
                        <mat-icon class="align-middle text-gray-500">phone</mat-icon>
                        {{ profileData.user.phone }}
                      </p>
                    </div>
                    <button mat-raised-button
                            color="primary"
                            (click)="openEditProfileDialog()">
                      Edit Profile
                    </button>
                  </div>
                </div>
              </div>

              <!-- Skills Section -->
              <div class="mt-8">
                <h3 class="text-xl font-semibold mb-4">Your Skills</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <mat-card *ngFor="let skill of profileData.skills" class="!bg-white p-4">
                    <mat-card-content>
                      <h4 class="font-bold">{{ skill.name }}</h4>
                      <div class="flex items-center mt-2">
                        <div class="flex-1">
                          <div class="w-full bg-gray-200 rounded-full h-2.5">
                            <div class="bg-blue-600 h-2.5 rounded-full" 
                                 [style.width.%]="(skill.proficiency / 5) * 100">
                            </div>
                          </div>
                        </div>
                        <span class="ml-2 text-sm text-gray-600">{{ skill.proficiency }}/10</span>
                      </div>
                    </mat-card-content>
                  </mat-card>
                  <div *ngIf="!profileData.skills?.length" class="text-gray-500 text-center col-span-full py-4">
                    No skills added yet
                  </div>
                </div>
              </div>

              <!-- Reviews Section -->
              <div class="mt-8">
                <h3 class="text-xl font-semibold mb-4">Your Reviews</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <mat-card *ngFor="let review of profileData.reviews" class="!bg-white p-4">
                    <mat-card-content>
                      <div class="flex items-center mb-4">
                        <img *ngIf="review.reviewer_profile_image" 
                             [src]="getProfileImageUrl(review.reviewer_profile_image)"
                             class="w-10 h-10 rounded-full object-cover mr-3"
                             alt="Reviewer's photo">
                        <div *ngIf="!review.reviewer_profile_image"
                             class="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center text-gray-600 text-lg font-semibold mr-3">
                          {{ review.reviewer.charAt(0).toUpperCase() }}
                        </div>
                        <div>
                          <div class="flex text-yellow-400">
                            <mat-icon *ngFor="let star of [1,2,3,4,5]"
                                    [class.text-yellow-400]="star <= review.rating"
                                    [class.text-gray-300]="star > review.rating">
                              star
                            </mat-icon>
                          </div>
                          <p class="text-sm text-gray-600">
                            <span class="capitalize font-medium">{{ review.reviewer }}</span> reviewed you for <span class="capitalize font-medium">{{ review.skill_name }}</span>
                          </p>
                        </div>
                      </div>
                      <p class="text-gray-800 mt-2">{{ review.text }}</p>
                    </mat-card-content>
                  </mat-card>
                  <div *ngIf="!profileData.reviews?.length" class="text-gray-500 text-center col-span-full py-4">
                    No reviews yet
                  </div>
                </div>
              </div>

              <!-- Completed Swaps Section -->
              <div class="mt-8">
                <h3 class="text-xl font-semibold mb-4">Completed Swaps</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <mat-card *ngFor="let swap of profileData.completed_swaps" class="!bg-white p-4">
                    <mat-card-content>
                      <p><strong>Skill Offered:</strong> {{ swap.skill_offered || 'N/A' }}</p>
                      <p><strong>Skill Requested:</strong> {{ swap.skill_requested || 'N/A' }}</p>
                      <p><strong>Requesting User:</strong> {{ swap.user_requesting }}</p>
                      <p><strong>Requested User:</strong> {{ swap.user_requested }}</p>
                      <p><strong>Proposed Time:</strong> {{ swap.proposed_time | date:'medium' }}</p>
                      <p><strong>Completed At:</strong> {{ swap.completed_at | date:'medium' }}</p>
                    </mat-card-content>
                  </mat-card>
                  <div *ngIf="!profileData.completed_swaps?.length" class="text-gray-500 text-center col-span-full py-4">
                    No completed swaps yet
                  </div>
                </div>
              </div>
            </ng-container>
          </div>
        </main>
      </div>
    </div>
  `
})
export class DashboardComponent implements OnInit {
  profileData: ProfileResponse | null = null;
  isLoading = true;
  error: string | null = null;

  constructor(
    private userService: UserService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadDashboardData();
  }

  loadDashboardData(): void {
    this.isLoading = true;
    this.error = null;

    this.userService.getUserProfile().pipe(
      catchError(error => {
        this.error = 'Failed to load dashboard data. Please try again later.';
        console.error('Dashboard data loading error:', error);
        return of(null);
      }),
      finalize(() => {
        this.isLoading = false;
      })
    ).subscribe(data => {
      if (data) {
        this.profileData = data;
      }
    });
  }

  openEditProfileDialog(): void {
    if (!this.profileData) return;

    const dialogRef = this.dialog.open(EditProfileDialogComponent, {
      width: '500px',
      data: {
        about: this.profileData.user.about,
        profile_image: this.profileData.user.profile_image
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result && this.profileData) {
        this.userService.updateUserProfile(result).pipe(
          catchError(error => {
            this.snackBar.open('Failed to update profile. Please try again.', 'Close', {
              duration: 5000
            });
            console.error('Profile update error:', error);
            return of(this.profileData?.user || null);
          })
        ).subscribe(updatedProfile => {
          if (this.profileData && updatedProfile) {
            // Preserve username and created_at fields
            updatedProfile.username = this.profileData.user.username;
            updatedProfile.created_at = this.profileData.user.created_at;

            this.profileData.user = updatedProfile;
            this.snackBar.open('Profile updated successfully', 'Close', {
              duration: 3000
            });
          }
        });
      }
    });
  }

  getProfileImageUrl(imagePath: string | null): string {
    return imagePath ? `${this.userService.baseUrl}/${imagePath}` : 'assets/default-avatar.png';
  }
}