# Requirements Document: Chrome Extension Visual Feedback

## Introduction

This document outlines the requirements for enhancing Project Crest's Chrome extension with visual feedback features. The enhancement will provide users with clear visual indicators when the AI agent detects loud audio events and takes volume control actions, improving user awareness and trust in the system's intelligent behavior.

## Requirements

### Requirement 1: Extension Icon State Management

**User Story:** As a user, I want the Chrome extension icon to visually indicate when Crest is actively managing volume, so that I can see when the AI agent is working.

#### Acceptance Criteria

1. WHEN the extension is installed THEN it SHALL display a default icon in the Chrome toolbar
2. WHEN a loud audio event is detected THEN the extension icon SHALL change to an active state
3. WHEN the volume adjustment period ends THEN the extension icon SHALL return to the default state
4. WHEN icon changes occur THEN they SHALL be visible within 100ms of the triggering event

### Requirement 2: On-Screen Notification System

**User Story:** As a user, I want to see a subtle notification when Crest lowers the volume, so that I understand why the audio changed and trust the system's decisions.

#### Acceptance Criteria

1. WHEN volume is lowered due to detected loud content THEN the system SHALL display an on-screen notification
2. WHEN the notification appears THEN it SHALL be positioned in a non-intrusive location (top-right corner)
3. WHEN the notification is shown THEN it SHALL include clear messaging about the volume adjustment
4. WHEN the volume adjustment period ends THEN the notification SHALL fade out smoothly
5. WHEN multiple notifications would overlap THEN the system SHALL handle them gracefully without visual conflicts

### Requirement 3: Visual Asset Management

**User Story:** As a developer, I want properly organized visual assets for the extension, so that the icon states and notifications render correctly across different display contexts.

#### Acceptance Criteria

1. WHEN the extension is packaged THEN it SHALL include default and active icon variants
2. WHEN icons are displayed THEN they SHALL be 128x128 pixels for optimal Chrome extension compatibility
3. WHEN notification styles are applied THEN they SHALL use web-accessible resources properly configured in the manifest
4. WHEN visual assets are referenced THEN they SHALL use correct paths relative to the extension root

### Requirement 4: Notification Styling and UX

**User Story:** As a user, I want the visual notifications to be clear but not distracting, so that they enhance rather than interrupt my viewing experience.

#### Acceptance Criteria

1. WHEN notifications appear THEN they SHALL use semi-transparent dark background for readability
2. WHEN notifications are displayed THEN they SHALL use clear, readable white text
3. WHEN notifications animate THEN they SHALL use smooth opacity transitions (0.5s duration)
4. WHEN notifications are positioned THEN they SHALL have appropriate padding and border radius for modern UI aesthetics
5. WHEN notifications appear THEN they SHALL have the highest z-index to ensure visibility over YouTube content

### Requirement 5: Agent Control Panel Popup

**User Story:** As a user, I want to access an agent control panel through the extension popup, so that I can monitor Crest's status and activity.

#### Acceptance Criteria

1. WHEN clicking the extension icon THEN it SHALL open a popup interface showing agent status
2. WHEN the popup is displayed THEN it SHALL show current agent status (Active/Inactive)
3. WHEN the popup is open THEN it SHALL display a log container for monitoring events
4. WHEN no events have occurred THEN the log SHALL display "Waiting for events..." message
5. WHEN the popup interface loads THEN it SHALL be properly styled with consistent branding

### Requirement 6: Enhanced CSS Resource Management

**User Story:** As a developer, I want proper CSS resource injection for notifications, so that styling is applied correctly across different page contexts.

#### Acceptance Criteria

1. WHEN the content script loads THEN it SHALL inject the notification CSS dynamically
2. WHEN CSS is injected THEN it SHALL use chrome.runtime.getURL for proper resource access
3. WHEN notification styles are applied THEN they SHALL not conflict with YouTube's existing styles
4. WHEN the extension is updated THEN CSS resources SHALL be properly versioned and cached

### Requirement 7: Communication Flow Integration

**User Story:** As a system component, I want the visual feedback to integrate seamlessly with the existing Chrome extension communication flow, so that visual updates are triggered by the same AI decisions that control volume.

#### Acceptance Criteria

1. WHEN subtitle data triggers AI analysis THEN the service worker SHALL coordinate both volume control and visual feedback
2. WHEN the Flask server responds with LOWER_VOLUME action THEN the extension SHALL trigger both icon change and notification display
3. WHEN volume adjustment duration is specified THEN visual feedback SHALL respect the same timing
4. WHEN communication errors occur THEN visual feedback SHALL not be triggered inappropriately
5. WHEN the extension handles multiple tabs THEN visual feedback SHALL be tab-specific and not interfere across tabs

![grey icon](crest-active.png)
![green icon](crest-inactive.png)