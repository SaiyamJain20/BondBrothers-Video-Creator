# BondBrothers Video Creator
A web application that allows users to upload images and audio files, and combine them to create customized videos with transition effects.

## Features
### User Management
#### Account Creation: 
- Users can sign up with name, username, email, and password
#### Authentication: 
- Secure login/logout functionality with password hashing
#### Profile Management: 
- Users can view and edit their profile information and upload profile pictures
#### Admin Panel: 
- Administrative interface for user management and system overview

### Media Upload & Management
#### Image Upload:

- Drag-and-drop interface for image uploading
- Visual preview of uploaded images
- Support for multiple image formats (JPEG, PNG, WebP)

#### Audio Upload:

- Upload and manage audio files (MP3, WAV, AAC)
- Audio playback in the interface
- Use of preloaded and user-uploaded audio tracks

### Video Creation
#### Media Selection: 
- Choose images and audio to include in your video

#### Video Preview: 
- View the generated video directly in the browser

#### Download: 
- Save created videos to your device
#### Customizable Options:

- Adjust image duration (seconds per image)
- Select video resolution (360p, 720p, 1080p, 4K)
- Choose video quality (low, medium, high)
- Apply transition effects (fade in/out, cross fade)


### Organization Tools
#### Search & Sort: 
- Find media files by name, date, or file size
#### Filtering: 
- Filter your media based on various criteria
#### Bulk Actions: 
- Delete all images or audio files at once

## Technology Stack
- Backend: Python with Flask framework
- Database: PostgreSQL (using psycopg2)
- Video Processing: moviepy for video generation
- Frontend: HTML, CSS, JavaScript
- Media Handling: mutagen for audio metadata, Pillow for image processing

## Security Features
- Password hashing with Werkzeug
- JWT authentication
- Session management
- Database connection pooling for better performance

## Responsive Design
- Mobile-friendly interface
- Adaptive layout for different screen sizes
- Custom styling with CSS variables for consistent theming


The application provides a complete workflow from media upload to video creation, allowing users to easily create slideshow videos with background music and transition effects.