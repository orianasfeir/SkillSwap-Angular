import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface SwapRequest {
  id?: number;
  offered_skill_id: number;
  target_user_id: number;
  target_skill_id: number;
  proposed_date: Date;
  message?: string;
  status?: 'pending' | 'accepted' | 'rejected' | 'completed';
  created_at?: string;
  updated_at?: string;
}

@Injectable({
  providedIn: 'root'
})
export class SwapService {
  private apiUrl = `${environment.apiUrl}`;

  constructor(private http: HttpClient) {}

  createSwapRequest(swapData: SwapRequest): Observable<SwapRequest> {
    return this.http.post<SwapRequest>(`${this.apiUrl}/swaps/`, {
      user_requested: swapData.target_user_id,
      skill_offered: swapData.offered_skill_id,
      skill_requested: swapData.target_skill_id,
      proposed_time: swapData.proposed_date
    });
  }

  getPendingSwapRequests(): Observable<SwapRequest[]> {
    return this.http.get<SwapRequest[]>(`${this.apiUrl}/swaps/pending/`);
  }

  getOngoingSwapRequests(): Observable<SwapRequest[]> {
    return this.http.get<SwapRequest[]>(`${this.apiUrl}/swaps/ongoing/`);
  }

  acceptSwapRequest(swapId: number): Observable<SwapRequest> {
    return this.http.post<SwapRequest>(`${this.apiUrl}/swaps/${swapId}/accept/`, {});
  }

  rejectSwapRequest(swapId: number): Observable<SwapRequest> {
    return this.http.post<SwapRequest>(`${this.apiUrl}/swaps/${swapId}/reject/`, {});
  }

  completeSwapRequest(swapId: number): Observable<SwapRequest> {
    return this.http.post<SwapRequest>(`${this.apiUrl}/swaps/${swapId}/complete/`, {});
  }
} 