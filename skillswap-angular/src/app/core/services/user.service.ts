import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { map } from 'rxjs/operators';

export interface UserProfile {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  phone: string;
  profile_image: string | null;
  about: string;
  created_at: string;
  updated_at: string;
  profile: {
    avatar: string;
    bio: string | null;
    location: string | null;
    rating: number | null;
    created_at: string;
    updated_at: string;
  };
  qualifications: any[];
}

export interface Skill {
  id: number;
  name: string;
  proficiency: number;
}

export interface UserSkill {
  id: number;
  proficiency_level: number;
  qualifications: any[]; // Adjust type if needed
  skill: Skill; // Nested Skill object
}

export interface Review {
  id: number;
  text: string;
  rating: number;
  reviewer: string;
}

export interface SwapRequest {
  id: number;
  user_requesting: {
    id: number;
    username: string;
    profile_image: string | null;
  };
  user_requested: {
    id: number;
    username: string;
    profile_image: string | null;
  };
  skill_offered: {
    id: number;
    name: string;
  };
  skill_requested: {
    id: number;
    name: string;
  };
  status: 'pending' | 'accepted' | 'rejected' | 'completed';
  proposed_time: string | null;
  created_at: string;
  updated_at: string;
}

export interface ProfileResponse {
  user: UserProfile;
  skills: Skill[];
  reviews: Review[];
  completed_swaps: any[];
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = `${environment.apiUrl}`;

  constructor(private http: HttpClient) {}

  // Profile Section
  getUserProfile(): Observable<ProfileResponse> {
    return this.http.get<ProfileResponse>(`${this.apiUrl}/users/profile/`);
  }

  updateUserProfile(profile: Partial<UserProfile>): Observable<UserProfile> {
    return this.http.patch<UserProfile>(`${this.apiUrl}/users/profile/`, profile);
  }

  // Skills Section
  getUserSkills(): Observable<UserSkill[]> {
    console.log('fetet aal service front')
    return this.http.get<{ results: UserSkill[] }>(`${this.apiUrl}/user-skills/`).pipe(
      map(response => response.results) // Extract the array from the response
    );
  }

  // Reviews Section
  getUserReviews(): Observable<Review[]> {
    return this.http.get<Review[]>(`${this.apiUrl}/reviews/`);
  }

  // Swap Requests Section
  getPendingSwapRequests(): Observable<SwapRequest[]> {
    return this.http.get<SwapRequest[]>(`${this.apiUrl}/swaps/pending/`);
  }

  getOngoingSwapRequests(): Observable<SwapRequest[]> {
    return this.http.get<SwapRequest[]>(`${this.apiUrl}/swaps/ongoing/`);
  }
} 