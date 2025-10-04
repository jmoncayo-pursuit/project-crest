# Requirements Document: Project Crest (Hackathon MVP)

## Introduction

This document outlines the Minimum Viable Product (MVP) requirements for Project Crest, an AI-powered browser agent designed for the NYC AI Agents Hackathon. The goal is to create a compelling, functional demo that showcases the core idea and cleverly integrates the sponsor technologies. The focus is on achieving a working end-to-end loop, not on building a production-perfect, scalable system.

## Core Requirements

### Requirement 1: The End-to-End Functional Loop

**User Story:** As a user watching a YouTube video, I want the volume to automatically dip when a loud event is about to happen, so I have a comfortable and uninterrupted listening experience.

#### Acceptance Criteria

1. WHEN watching a YouTube video THEN the Chrome Extension SHALL successfully scrape live subtitle text (e.g., "[explosion]") in real-time
2. WHEN subtitle text is captured THEN the Extension SHALL send this text to a local Python Flask server
3. WHEN the Flask server receives text THEN it SHALL make a decision and send a `LOWER_VOLUME` command back to the extension
4. WHEN receiving the command THEN the Extension SHALL lower the volume of the HTML5 `<video>` element for a specified duration before restoring it

### Requirement 2: AI-Powered Decision Making

**User Story:** As a developer, I want to use AI to intelligently determine if a subtitle describes a loud noise, demonstrating a smart, context-aware agent.

#### Acceptance Criteria

1. WHEN making AI requests THEN the Flask server SHALL route all OpenAI API calls through the TrueFoundry AI Gateway using their base_url and API key
2. WHEN processing subtitle text THEN the server SHALL call OpenAI via the gateway asking for a simple "YES" or "NO" decision on whether it constitutes a loud event
3. WHEN running the server THEN it SHALL be orchestrated via the OpenHands agent framework
4. WHEN preprocessing is needed THEN the server SHOULD use Structify to clean subtitle text before sending to OpenAI (stretch goal)

### Requirement 3: "Production-Ready" Observability Demo

**User Story:** As a developer, I want to show the judges that this application is built with modern, observable principles, making it suitable for a real-world environment.

#### Acceptance Criteria

1. WHEN starting the Flask application THEN it SHALL be launched using `ddtrace-run` to automatically generate traces for every request
2. WHEN generating logs THEN the application SHALL output structured JSON logs with `DD_LOGS_INJECTION=true` to inject trace IDs
3. WHEN business events occur THEN the application SHALL send at least one custom metric to Datadog using `statsd` (e.g., `statsd.increment('crest.loud_event.detected')`)