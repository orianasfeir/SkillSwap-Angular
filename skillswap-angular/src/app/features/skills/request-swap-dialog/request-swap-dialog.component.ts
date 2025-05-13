import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';

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
    MatSelectModule,
    MatDatepickerModule,
    MatNativeDateModule
  ],
  template: `
    <div class="p-6">
      <h2 class="text-2xl font-bold mb-4">Request Skill Swap</h2>
      <form [formGroup]="swapForm" (ngSubmit)="onSubmit()">
        <mat-form-field class="w-full mb-4">
          <mat-label>Your Skill to Offer</mat-label>
          <mat-select formControlName="offeredSkillId" required>
            <mat-option *ngFor="let skill of data.userSkills" [value]="skill.id">
              {{ skill.skill.name }}
            </mat-option>
          </mat-select>
          <mat-error *ngIf="swapForm.get('offeredSkillId')?.hasError('required')">
            Please select a skill to offer
          </mat-error>
        </mat-form-field>
        
        <mat-form-field class="w-full mb-4">
          <mat-label>Proposed Date</mat-label>
          <input matInput [matDatepicker]="picker" formControlName="proposedDate" required>
          <mat-datepicker-toggle matIconSuffix [for]="picker"></mat-datepicker-toggle>
          <mat-datepicker #picker></mat-datepicker>
          <mat-error *ngIf="swapForm.get('proposedDate')?.hasError('required')">
            Please select a proposed date
          </mat-error>
        </mat-form-field>
        
        <mat-form-field class="w-full mb-4">
          <mat-label>Message (Optional)</mat-label>
          <textarea matInput
                    formControlName="message"
                    rows="3"
                    placeholder="Add a message to your request..."></textarea>
        </mat-form-field>

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
      proposedDate: ['', Validators.required],
      message: ['', Validators.maxLength(500)]
    });
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