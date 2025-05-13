import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SwapService } from '../../core/services/swap.service';
import { Observable } from 'rxjs';
import { HttpClientModule } from '@angular/common/http';

interface SwapResponse {
  id: number;
  user_requesting: { id: number; username: string };
  user_requested: { id: number; username: string };
  skill_offered: { id: number; name: string };
  skill_requested: { id: number; name: string };
  status: string;
  proposed_time: string;
  created_at: string;
  updated_at: string;
}

@Component({
  selector: 'app-swaps',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  template: `
    <div class="min-h-screen bg-gray-100">
      <div class="py-10">
        <header>
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 class="text-3xl font-bold leading-tight text-gray-900">
              Swaps
            </h1>
          </div>
        </header>
        <main>
          <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <div class="px-4 py-8 sm:px-0">
              <h2 class="text-2xl font-semibold mb-4">Incoming Requests</h2>
              <div *ngFor="let swap of incomingSwaps" class="bg-white shadow rounded p-4 mb-4">
                <p><strong>From:</strong> {{ swap.user_requesting.username }}</p>
                <p><strong>Skill Offered:</strong> {{ swap.skill_offered.name }}</p>
                <p><strong>Skill Requested:</strong> {{ swap.skill_requested.name }}</p>
                <button (click)="acceptSwap(swap.id)" class="bg-green-500 text-white px-4 py-2 rounded">Accept</button>
                <button (click)="rejectSwap(swap.id)" class="bg-red-500 text-white px-4 py-2 rounded ml-2">Reject</button>
              </div>

              <h2 class="text-2xl font-semibold mb-4">Outgoing Requests</h2>
              <div *ngFor="let swap of outgoingSwaps" class="bg-white shadow rounded p-4 mb-4">
                <p><strong>To:</strong> {{ swap.user_requested.username }}</p>
                <p><strong>Skill Offered:</strong> {{ swap.skill_offered.name }}</p>
                <p><strong>Skill Requested:</strong> {{ swap.skill_requested.name }}</p>
                <button (click)="cancelSwap(swap.id)" class="bg-yellow-500 text-white px-4 py-2 rounded">Cancel</button>
              </div>

              <h2 class="text-2xl font-semibold mb-4">Active Swaps</h2>
              <div *ngFor="let swap of activeSwaps" class="bg-white shadow rounded p-4 mb-4">
                <p><strong>With:</strong> {{ swap.user_requested.username }}</p>
                <p><strong>Skill Offered:</strong> {{ swap.skill_offered.name }}</p>
                <p><strong>Skill Requested:</strong> {{ swap.skill_requested.name }}</p>
                <button (click)="completeSwap(swap.id)" class="bg-blue-500 text-white px-4 py-2 rounded">Complete</button>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  `
})
export class SwapsComponent implements OnInit {
  incomingSwaps: SwapResponse[] = [];
  outgoingSwaps: SwapResponse[] = [];
  activeSwaps: SwapResponse[] = [];

  constructor(private swapService: SwapService) {}

  ngOnInit(): void {
    this.loadIncomingSwaps();
    this.loadOutgoingSwaps();
    this.loadActiveSwaps();
  }

  loadIncomingSwaps(): void {
    this.swapService.getIncomingSwaps().subscribe((response: { results: SwapResponse[] }) => {
      this.incomingSwaps = response.results;
    });
  }

  loadOutgoingSwaps(): void {
    this.swapService.getOutgoingSwaps().subscribe((response: { results: SwapResponse[] }) => {
      this.outgoingSwaps = response.results;
    });
  }

  loadActiveSwaps(): void {
    this.swapService.getActiveSwaps().subscribe((response: { results: SwapResponse[] }) => {
      this.activeSwaps = response.results;
    });
  }

  acceptSwap(swapId: number): void {
    this.swapService.acceptSwapRequest(swapId).subscribe(() => {
      this.loadIncomingSwaps();
      this.loadActiveSwaps();
    });
  }

  rejectSwap(swapId: number): void {
    this.swapService.rejectSwapRequest(swapId).subscribe(() => {
      this.loadIncomingSwaps();
    });
  }

  cancelSwap(swapId: number): void {
    this.swapService.cancelSwapRequest(swapId).subscribe(() => {
      this.loadOutgoingSwaps();
    });
  }

  completeSwap(swapId: number): void {
    this.swapService.completeSwapRequest(swapId).subscribe(() => {
      this.loadActiveSwaps();
    });
  }
}