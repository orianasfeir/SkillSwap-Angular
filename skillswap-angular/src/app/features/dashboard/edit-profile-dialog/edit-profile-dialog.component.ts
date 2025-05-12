import { Component, Inject, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

@Component({
  selector: 'app-edit-profile-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule
  ],
  template: `
    <div class="p-6">
      <h2 class="text-2xl font-bold mb-4">Edit Profile</h2>
      <form [formGroup]="profileForm" (ngSubmit)="onSubmit()">
        <div class="mb-4">
          <div class="flex items-center justify-center mb-4">
            <div class="relative">
              <img [src]="previewImage || (profileForm.get('profile_image')?.value ? baseUrl + '/' + profileForm.get('profile_image')?.value : 'assets/default-avatar.png')"
                   class="w-32 h-32 rounded-full object-cover"
                   alt="Profile picture">
              <button type="button"
                      class="absolute bottom-0 right-0 bg-blue-500 text-white rounded-full p-2 hover:bg-blue-600"
                      (click)="openFileInput()">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </button>
            </div>
          </div>
          <input type="file"
                 accept="image/*"
                 class="hidden"
                 #fileInput
                 (change)="onFileSelected($event)">
        </div>

        <mat-form-field class="w-full mb-4">
          <mat-label>Bio</mat-label>
          <textarea matInput
                    formControlName="about"
                    rows="4"
                    placeholder="Tell us about yourself..."></textarea>
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
                  [disabled]="profileForm.invalid">
            Save Changes
          </button>
        </div>
      </form>
    </div>
  `
})
export class EditProfileDialogComponent {
  @ViewChild('fileInput') fileInput!: ElementRef;
  profileForm: FormGroup;
  baseUrl = 'http://localhost:8000'; // Replace with your actual base URL
  previewImage: string | ArrayBuffer | null = null; // To store the preview image URL

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<EditProfileDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { about: string; profile_image: string },
  ) {
    this.profileForm = this.fb.group({
      about: [data.about || '', [Validators.maxLength(500)]],
      profile_image: [data.profile_image || '']
    });
  }

  // Updated to send the profilePicture as a File object instead of a base64 string.
  onFileSelected(event: Event): void {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (file) {
      this.profileForm.patchValue({
        profile_image: file // Update the form control with the file
      });

      // Use FileReader to generate a preview URL
      const reader = new FileReader();
      reader.onload = () => {
        this.previewImage = reader.result; // Set the preview image URL
      };
      reader.readAsDataURL(file);
    }
  }

  openFileInput(): void {
    this.fileInput.nativeElement.click();
  }

  onSubmit(): void {
    if (this.profileForm.valid) {
      const formData = { ...this.profileForm.value };
      this.dialogRef.close(formData);
    }
  }

  onCancel(): void {
    this.dialogRef.close();
  }
}