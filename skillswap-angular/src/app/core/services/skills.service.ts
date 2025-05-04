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

export interface UserSkill {
  id: number;
  proficiency_level: number;
  qualifications: any[]; // Adjust type if needed
  skill: Skill; // Nested Skill object
}

@Injectable({
  providedIn: 'root'
})
export class SkillsService {
  private apiUrl = `${environment.apiUrl}/`;

  constructor(private http: HttpClient) {}

  getSkills(): Observable<Skill[]> {
    return this.http.get<{ results: Skill[] }>(`${this.apiUrl}skills`).pipe(
      map(response => response.results)
    );
  }

  addUserSkill(skillData: { skill_id: number; proficiency_level: number }): Observable<any> {
    return this.http.post(`${this.apiUrl}user-skills/`, skillData);
  }

  getUserSkills(): Observable<UserSkill[]> {
    return this.http.get<{ results: UserSkill[] }>(`${this.apiUrl}user-skills/`).pipe(
      map(response => response.results) // Extract the array from the response
    );
  }

  deleteUserSkill(userSkillId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}user-skills/${userSkillId}/`);
  }

  editUserSkill(userSkillId: number, proficiencyLevel: number): Observable<UserSkill> {
    return this.http.patch<UserSkill>(`${this.apiUrl}user-skills/${userSkillId}/`, {
      proficiency_level: proficiencyLevel
    });
  }
}