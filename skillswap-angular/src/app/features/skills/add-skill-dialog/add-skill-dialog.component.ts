import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-add-skill-dialog',
  standalone: true,
  imports: [CommonModule, MatFormFieldModule, MatInputModule, MatButtonModule, MatDialogModule, ReactiveFormsModule],
  template: `
    <h1 mat-dialog-title>Add Skill</h1>
    <div mat-dialog-content>
      <form [formGroup]="form">
        <mat-form-field appearance="fill" class="w-full">
          <mat-label>Proficiency Level</mat-label>
          <input matInput type="number" formControlName="proficiency_level" min="1" max="10">
          <mat-error *ngIf="form.get('proficiency_level')?.hasError('required')">
            Proficiency level is required
          </mat-error>
          <mat-error *ngIf="form.get('proficiency_level')?.hasError('min') || form.get('proficiency_level')?.hasError('max')">
            Proficiency level must be between 1 and 10
          </mat-error>
        </mat-form-field>
      </form>
    </div>
    <div mat-dialog-actions>
      <button mat-button (click)="onCancel()">Cancel</button>
      <button mat-button [disabled]="form.invalid" (click)="onSubmit()">Add</button>
    </div>
  `
})
export class AddSkillDialogComponent {
  form: FormGroup;

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<AddSkillDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { skillId: number }
  ) {
    this.form = this.fb.group({
      skill_id: [data.skillId, Validators.required],
      proficiency_level: ['', [Validators.required, Validators.min(1), Validators.max(10)]]
    });
  }

  onCancel(): void {
    this.dialogRef.close();
  }

  onSubmit(): void {
    if (this.form.valid) {
      this.dialogRef.close(this.form.value);
    }
  }
}