import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface UserProfile {
  id: number;
  username: string;
  email: string;
  profile_image: string | null;
  bio: string;
  date_joined: string;
}

export interface Skill {
  id: number;
  name: string;
  proficiency: number;
  category: string;
}

export interface Review {
  id: number;
  text: string;
  rating: number;
  reviewer: {
    id: number;
    username: string;
    profile_image: string | null;
  };
  created_at: string;
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

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = `${environment.apiUrl}`;

  constructor(private http: HttpClient) {}

  // Profile Section
  getUserProfile(): Observable<UserProfile> {
    return this.http.get<UserProfile>(`${this.apiUrl}/users/profile/`);
  }

  updateUserProfile(profile: Partial<UserProfile>): Observable<UserProfile> {
    return this.http.patch<UserProfile>(`${this.apiUrl}/users/profile/`, profile);
  }

  // Skills Section
  getUserSkills(): Observable<Skill[]> {
    return this.http.get<Skill[]>(`${this.apiUrl}/user-skills/`);
  }

  // Reviews Section
  getUserReviews(): Observable<Review[]> {
    return this.http.get<Review[]>(`${this.apiUrl}/reviews/`);
  }

  // Swap Requests Section
  getPendingSwapRequests(): Observable<SwapRequest[]> {
    return this.http.get<SwapRequest[]>(`${this.apiUrl}/swap-requests/pending/`);
  }

  getOngoingSwapRequests(): Observable<SwapRequest[]> {
    return this.http.get<SwapRequest[]>(`${this.apiUrl}/swap-requests/ongoing/`);
  }
} 