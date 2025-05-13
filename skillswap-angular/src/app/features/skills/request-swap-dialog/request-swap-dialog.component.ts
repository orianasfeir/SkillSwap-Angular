import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';

@Component({
  selector: 'app-request-swap-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule
  ],
  template: `
    <div class="p-6">
      <h2 class="text-2xl font-bold mb-4">Request Skill Swap</h2>
      <form [formGroup]="swapForm" (ngSubmit)="onSubmit()">
        <mat-form-field class="w-full mb-4">
          <mat-label>Your Skill to Offer</mat-label>
          <mat-select formControlName="offeredSkillId" required>
            <mat-option *ngFor="let skill of data.userSkills" [value]="skill.skill.id">
              {{ skill.skill.name }}
            </mat-option>
          </mat-select>
          <mat-error *ngIf="swapForm.get('offeredSkillId')?.hasError('required')">
            Please select a skill to offer
          </mat-error>
        </mat-form-field>
        
        <div class="mb-4">
          <label for="proposedDate" class="block text-sm font-medium text-gray-700 mb-1">Proposed Date</label>
          <input 
            type="date" 
            id="proposedDate" 
            formControlName="proposedDate"
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
            required
          >
          <div *ngIf="swapForm.get('proposedDate')?.invalid && swapForm.get('proposedDate')?.touched" class="text-red-500 text-sm mt-1">
            Please select a proposed date
          </div>
        </div>

        <div class="flex justify-end gap-2">
          <button mat-button
                  type="button"
                  (click)="onCancel()">
            Cancel
          </button>
          <button mat-raised-button
                  color="primary"
                  type="submit"
                  [disabled]="swapForm.invalid">
            Send Request
          </button>
        </div>
      </form>
    </div>
  `
})
export class RequestSwapDialogComponent {
  swapForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<RequestSwapDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { 
      userSkills: any[],
      targetUserId: number,
      targetSkillId: number
    },
  ) {
    this.swapForm = this.fb.group({
      offeredSkillId: ['', Validators.required],
      proposedDate: [this.formatDate(new Date()), Validators.required]
    });
  }

  formatDate(date: Date): string {
    const d = new Date(date);
    let month = '' + (d.getMonth() + 1);
    let day = '' + d.getDate();
    const year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    return [year, month, day].join('-');
  }

  onSubmit(): void {
    if (this.swapForm.valid) {
      const formData = {
        ...this.swapForm.value,
        targetUserId: this.data.targetUserId,
        targetSkillId: this.data.targetSkillId
      };
      this.dialogRef.close(formData);
    }
  }

  onCancel(): void {
    this.dialogRef.close();
  }
}