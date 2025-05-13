import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { map } from 'rxjs/operators';

export interface Skill {
  id: number;
  name: string;
  description: string;
  created_at: string;
  is_featured: boolean;
}

export interface Qualification {
  id: number;
  description: string;
  verified: boolean;
}

export interface UserSkill {
  id: number;
  proficiency_level: number;
  qualifications: Qualification[];
  skill: Skill; // Nested Skill object
}

export interface UserProfile {
  id: number;
  username: string;
  profile_image: string | null;
}

export interface UserOfferingSkill {
  user: UserProfile;
  proficiency_level: string;
  qualifications: Qualification[];
}

export interface SkillReview {
  id: number;
  text: string;
  rating: number;
  reviewer: string; // username
  reviewer_profile_image: string | null;
  user_reviewed: string; // username of the person being reviewed
  skill_name: string;
}

export interface SkillDetailResponse {
  skill: Skill;
  user_has_skill: boolean; // Whether the current logged-in user has this skill
  users_offering: UserOfferingSkill[];
  reviews: SkillReview[];
}

@Injectable({
  providedIn: 'root',
})
export class SkillsService {
  private apiUrl = `${environment.apiUrl}/`;

  constructor(private http: HttpClient) {}

  getSkills(): Observable<Skill[]> {
    return this.http
      .get<{ results: Skill[] }>(`${this.apiUrl}skills`)
      .pipe(map((response) => response.results));
  }

  addUserSkill(skillData: {
    skill_id: number;
    proficiency_level: number;
    qualification_description?: string;
  }): Observable<any> {
    return this.http.post(`${this.apiUrl}user-skills/`, skillData);
  }

  getUserSkills(): Observable<UserSkill[]> {
    return this.http
      .get<{ results: UserSkill[] }>(`${this.apiUrl}user-skills/`)
      .pipe(
        map((response) => response.results) // Extract the array from the response
      );
  }

  deleteUserSkill(userSkillId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}user-skills/${userSkillId}/`);
  }

  editUserSkill(
    userSkillId: number,
    proficiencyLevel: number,
    qualificationDescription?: string
  ): Observable<UserSkill> {
    const updateData: any = {
      proficiency_level: proficiencyLevel
    };
    
    if (qualificationDescription) {
      updateData.qualification_description = qualificationDescription;
    }
    
    return this.http.patch<UserSkill>(
      `${this.apiUrl}user-skills/${userSkillId}/`,
      updateData
    );
  }

  getSkillDetails(skillId: number): Observable<SkillDetailResponse> {
    return this.http.get<SkillDetailResponse>(
      `${this.apiUrl}skills/${skillId}/`
    );
  }
}
