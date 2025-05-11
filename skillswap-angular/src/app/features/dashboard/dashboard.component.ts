import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { catchError, finalize, forkJoin, of } from 'rxjs';
import { EditProfileDialogComponent } from './edit-profile-dialog/edit-profile-dialog.component';
import { LoadingSpinnerComponent } from '../../shared/components/loading-spinner/loading-spinner.component';
import { UserService, UserProfile, Skill, Review, SwapRequest } from '../../core/services/user.service';

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
            <ng-container *ngIf="!isLoading && !error">
              <!-- Profile Section -->
              <div class="mt-8">
                <div class="bg-white shadow rounded-lg p-6">
                  <div class="flex items-center space-x-4">
                    <img [src]="userProfile.profile_image || 'assets/default-avatar.png'"
                         class="w-24 h-24 rounded-full object-cover"
                         alt="Profile picture">
                    <div class="flex-1">
                      <h2 class="text-2xl font-bold">{{ userProfile.username }}</h2>
                      <p class="text-gray-600">{{ userProfile.bio || 'No bio yet' }}</p>
                      <p class="text-sm text-gray-500">Member since {{ userProfile.date_joined | date }}</p>
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
                  <mat-card *ngFor="let skill of userSkills" class="p-4">
                    <mat-card-content>
                      <h4 class="font-bold">{{ skill.name }}</h4>
                      <p class="text-gray-600">Proficiency: {{ skill.proficiency }}/5</p>
                      <p class="text-gray-600">Category: {{ skill.category }}</p>
                    </mat-card-content>
                  </mat-card>
                  <div *ngIf="userSkills.length === 0" class="text-gray-500 text-center col-span-full py-4">
                    No skills added yet
                  </div>
                </div>
              </div>

              <!-- Reviews Section -->
              <div class="mt-8">
                <h3 class="text-xl font-semibold mb-4">Your Reviews</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <mat-card *ngFor="let review of userReviews" class="p-4">
                    <mat-card-content>
                      <div class="flex items-center mb-2">
                        <div class="flex text-yellow-400">
                          <mat-icon *ngFor="let star of [1,2,3,4,5]"
                                   [class.text-yellow-400]="star <= review.rating"
                                   [class.text-gray-300]="star > review.rating">
                            star
                          </mat-icon>
                        </div>
                        <span class="ml-2 text-gray-600">{{ review.created_at | date }}</span>
                      </div>
                      <p class="text-gray-800">{{ review.text }}</p>
                      <div class="flex items-center mt-2">
                        <img [src]="review.reviewer.profile_image || 'assets/default-avatar.png'"
                             class="w-6 h-6 rounded-full mr-2"
                             alt="Reviewer">
                        <p class="text-gray-600">- {{ review.reviewer.username }}</p>
                      </div>
                    </mat-card-content>
                  </mat-card>
                  <div *ngIf="userReviews.length === 0" class="text-gray-500 text-center col-span-full py-4">
                    No reviews yet
                  </div>
                </div>
              </div>

              <!-- Swap Requests Section -->
              <div class="mt-8 grid grid-cols-1 md:grid-cols-2 gap-8">
                <!-- Pending Requests -->
                <div>
                  <h3 class="text-xl font-semibold mb-4">Pending Requests</h3>
                  <div class="space-y-4">
                    <mat-card *ngFor="let request of pendingRequests" class="p-4">
                      <mat-card-content>
                        <div class="flex justify-between items-start">
                          <div>
                            <p class="font-semibold">Offering: {{ request.skill_offered.name }}</p>
                            <p class="text-gray-600">Requesting: {{ request.skill_requested.name }}</p>
                            <p class="text-sm text-gray-500">{{ request.created_at | date }}</p>
                            <p class="text-sm text-gray-500">
                              From: {{ request.user_requesting.username }}
                            </p>
                          </div>
                          <span class="px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm">
                            Pending
                          </span>
                        </div>
                      </mat-card-content>
                    </mat-card>
                    <div *ngIf="pendingRequests.length === 0" class="text-gray-500 text-center py-4">
                      No pending requests
                    </div>
                  </div>
                </div>

                <!-- Ongoing Requests -->
                <div>
                  <h3 class="text-xl font-semibold mb-4">Ongoing Requests</h3>
                  <div class="space-y-4">
                    <mat-card *ngFor="let request of ongoingRequests" class="p-4">
                      <mat-card-content>
                        <div class="flex justify-between items-start">
                          <div>
                            <p class="font-semibold">Offering: {{ request.skill_offered.name }}</p>
                            <p class="text-gray-600">Requesting: {{ request.skill_requested.name }}</p>
                            <p class="text-sm text-gray-500">{{ request.created_at | date }}</p>
                            <p class="text-sm text-gray-500">
                              With: {{ request.user_requesting.username === userProfile.username ? 
                                     request.user_requested.username : 
                                     request.user_requesting.username }}
                            </p>
                          </div>
                          <span class="px-2 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                            Ongoing
                          </span>
                        </div>
                      </mat-card-content>
                    </mat-card>
                    <div *ngIf="ongoingRequests.length === 0" class="text-gray-500 text-center py-4">
                      No ongoing requests
                    </div>
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
  userProfile: UserProfile = {
    id: 0,
    username: '',
    email: '',
    profile_image: null,
    bio: '',
    date_joined: ''
  };
  userSkills: Skill[] = [];
  userReviews: Review[] = [];
  pendingRequests: SwapRequest[] = [];
  ongoingRequests: SwapRequest[] = [];
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

    forkJoin({
      profile: this.userService.getUserProfile(),
      skills: this.userService.getUserSkills(),
      reviews: this.userService.getUserReviews(),
      pendingRequests: this.userService.getPendingSwapRequests(),
      ongoingRequests: this.userService.getOngoingSwapRequests()
    }).pipe(
      catchError(error => {
        this.error = 'Failed to load dashboard data. Please try again later.';
        console.error('Dashboard data loading error:', error);
        return of({
          profile: this.userProfile,
          skills: [],
          reviews: [],
          pendingRequests: [],
          ongoingRequests: []
        });
      }),
      finalize(() => {
        this.isLoading = false;
      })
    ).subscribe(data => {
      this.userProfile = data.profile;
      this.userSkills = data.skills;
      this.userReviews = data.reviews;
      this.pendingRequests = data.pendingRequests;
      this.ongoingRequests = data.ongoingRequests;
    });
  }

  openEditProfileDialog(): void {
    const dialogRef = this.dialog.open(EditProfileDialogComponent, {
      width: '500px',
      data: {
        bio: this.userProfile.bio,
        profilePicture: this.userProfile.profile_image
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.userService.updateUserProfile(result).pipe(
          catchError(error => {
            this.snackBar.open('Failed to update profile. Please try again.', 'Close', {
              duration: 5000
            });
            console.error('Profile update error:', error);
            return of(this.userProfile);
          })
        ).subscribe(updatedProfile => {
          this.userProfile = updatedProfile;
          this.snackBar.open('Profile updated successfully', 'Close', {
            duration: 3000
          });
        });
      }
    });
  }
} 