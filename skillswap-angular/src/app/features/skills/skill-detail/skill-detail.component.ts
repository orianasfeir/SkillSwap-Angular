import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { Observable } from 'rxjs';
import {
  SkillsService,
  SkillDetailResponse,
} from '../../../core/services/skills.service';
import { HttpClientModule } from '@angular/common/http'; // Import if not globally provided or if service needs it directly
import { MatIconModule } from '@angular/material/icon';
import { environment } from '../../../../environments/environment';

@Component({
  selector: 'app-skill-detail',
  standalone: true,
  imports: [CommonModule, RouterModule, HttpClientModule, MatIconModule], // HttpClientModule might not be needed if SkillsService is correctly provided
  template: `<div class="min-h-screen bg-gray-100">
    <div class="py-10">
      <header *ngIf="skillDetail$ | async as details">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold leading-tight text-gray-900">
            {{ details.skill.name }}
          </h1>
          <p class="mt-2 text-lg text-gray-600">
            {{ details.skill.description }}
          </p>
        </div>
      </header>
      <main>
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
          <div class="px-4 py-8 sm:px-0">
            <div *ngIf="skillDetail$ | async as details; else loading">
              <!-- Users Offering this Skill -->
              <h2 class="text-2xl font-semibold mb-4 text-gray-800">
                Users Offering This Skill
              </h2>
              <div
                *ngIf="details.users_offering.length > 0; else noUsers"
                class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
              >
                <div
                  *ngFor="let offering of details.users_offering"
                  class="bg-white shadow-lg rounded-lg p-6"
                >
                  <div class="flex items-center mb-4">
                    <img
                      *ngIf="offering.user.profile_image"
                      [src]="getImageUrl(offering.user.profile_image)"
                      alt="{{ offering.user.username }}"
                      class="w-12 h-12 rounded-full mr-4 object-cover"
                    />
                    <div
                      *ngIf="!offering.user.profile_image"
                      class="w-12 h-12 rounded-full mr-4 bg-gray-300 flex items-center justify-center text-gray-600 text-xl font-semibold"
                    >
                      {{ offering.user.username.charAt(0).toUpperCase() }}
                    </div>
                    <h3 class="text-xl font-semibold text-gray-900">
                      {{ offering.user.username }}
                    </h3>
                  </div>
                  <p class="text-gray-700">
                    Proficiency:
                    <span class="font-medium">{{
                      offering.proficiency_level
                    }}/10</span>
                  </p>

                  <div *ngIf="offering.qualifications.length > 0" class="mt-3">
                    <h4 class="text-md font-semibold text-gray-800">
                      Qualifications:
                    </h4>
                    <ul class="list-disc list-inside ml-4 text-gray-600">
                      <li *ngFor="let qual of offering.qualifications">
                        {{ qual.description }}
                        <span
                          *ngIf="qual.verified"
                          class="text-green-500 font-semibold"
                          >(Verified)</span
                        >
                      </li>
                    </ul>
                  </div>
                  <button
                    (click)="requestSwap(offering.user.id)"
                    class="mt-4 w-full px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50"
                  >
                    Request Swap
                  </button>
                </div>
              </div>
              <ng-template #noUsers>
                <p class="text-gray-600">
                  No other users are currently offering this skill.
                </p>
              </ng-template>

              <!-- Reviews for this Skill -->
              <h2 class="text-2xl font-semibold mt-10 mb-4 text-gray-800">
                Skill Reviews
              </h2>
              <div
                *ngIf="details.reviews.length > 0; else noReviews"
                class="space-y-6"
              >
                <div
                  *ngFor="let review of details.reviews"
                  class="bg-white shadow-lg rounded-lg p-6"
                >
                  <div class="flex gap-4 items-center mb-4">
                    <img
                      *ngIf="review.reviewer_profile_image"
                      [src]="getImageUrl(review.reviewer_profile_image)"
                      alt="{{ review.reviewer }}"
                      class="w-10 h-10 rounded-full object-cover"
                    />
                    <div
                      *ngIf="!review.reviewer_profile_image"
                      class="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center text-gray-600 text-lg font-semibold"
                    >
                      {{ review.reviewer.charAt(0).toUpperCase() }}
                    </div>
                    <div>
                      <h4 class="text-lg font-semibold text-gray-900">
                        {{ review.reviewer }}
                      </h4>
                      <div class="flex text-yellow-400">
                        <mat-icon *ngFor="let star of [1,2,3,4,5]"
                                [class.text-yellow-400]="star <= review.rating"
                                [class.text-gray-300]="star > review.rating">
                          star
                        </mat-icon>
                      </div>
                    </div>
                  </div>
                  <p class="text-gray-700 mt-2">{{ review.text }}</p>
                </div>
              </div>
              <ng-template #noReviews>
                <p class="text-gray-600">
                  There are no reviews for this skill yet.
                </p>
              </ng-template>
            </div>
            <ng-template #loading>
              <p class="text-center mt-8 text-gray-500">
                Loading skill details...
              </p>
            </ng-template>
          </div>
        </div>
      </main>
    </div>
  </div> `,
  // styleUrls: ['./skill-detail.component.css'] // If you have separate styles
})
export class SkillDetailComponent implements OnInit {
  skillDetail$!: Observable<SkillDetailResponse>;
  skillId!: number;

  constructor(
    private route: ActivatedRoute,
    private skillsService: SkillsService
  ) {}

  ngOnInit(): void {
    this.skillId = Number(this.route.snapshot.paramMap.get('id'));
    console.log('Skill ID:', this.skillId);
    if (this.skillId) {
      this.skillDetail$ = this.skillsService.getSkillDetails(this.skillId);
    }
  }

  getImageUrl(imagePath: string | null): string {
    if (!imagePath) return '';
    // If the image path already starts with http, return it as is
    if (imagePath.startsWith('http')) return imagePath;
    // Otherwise, prepend the images base URL
    return `${environment.imagesUrl}${imagePath}`;
  }

  requestSwap(userId: number): void {
    // Placeholder for swap request logic
    console.log(
      `Requesting swap with user ID: ${userId} for skill ID: ${this.skillId}`
    );
    // This could navigate to a new page, open a dialog, or make an API call.
    alert(
      `Swap request functionality for user ${userId} is not yet implemented.`
    );
  }
}
