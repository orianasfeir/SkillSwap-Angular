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

@Injectable({
  providedIn: 'root'
})
export class SkillsService {
  private apiUrl = `${environment.apiUrl}/skills/`;

  constructor(private http: HttpClient) {}

  getSkills(): Observable<Skill[]> {
    return this.http.get<{ results: Skill[] }>(this.apiUrl).pipe(
      map(response => response.results)
    );
  }

  addUserSkill(skillData: { skill_id: number; proficiency_level: number }): Observable<any> {
    return this.http.post(`${this.apiUrl}user-skills/`, skillData);
  }

  getUserSkills(): Observable<Skill[]> {
    return this.http.get<Skill[]>(`${this.apiUrl}user-skills/`);
  }
}