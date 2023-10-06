# Game Design Document for Avalon Sigma

---

## 1. Introduction

### Concept
The game is a space exploration and logistics management experience set in a half-broken ship at Alpha Centauri. Players wake up from cryo-sleep with a few crew members and aim to reach a mythical space colony, "Avalon Sigma."

### Objective
The end goal may involve reaching a mythical space colony like "Avalon Sigma."

### Target Audience
The game is designed for players who enjoy a single-player experience without time pressures, allowing for more thoughtful and strategic play.

---

## 2. Gameplay Mechanics

### Resource Scarcity
- The game starts with limited resources, adding an immediate layer of challenge and urgency.

### Planet vs. Ship Manufacturing
- Limited but mobile manufacturing capabilities on the ship.
- Extensive but stationary manufacturing options on planets.
- Creates an interesting strategic trade-off for players.

### Upgradable Ship
- Upgrade different aspects of the ship, from cargo space to manufacturing efficiency or defense capabilities.

### Crew Management
- Unique skills and potential storylines for each crew member, including different section chiefs like Engineering.

### Decision Trees
- Key choices affect resource allocation and strategy, such as whether to explore potentially dangerous areas for valuable resources.

### Exploration and Expansion
- Players can explore new planets and systems to find resources or even a permanent settlement.

### Crisis Events
- Random events like natural disasters or space pirate attacks can occur, requiring immediate decisions.
- These events are not time-based to suit a more solitaire-like pace.

---

## 3. UI and Technical Aspects

### Tech Stack
- Backend: Django
- Frontend: jQuery and Bootstrap

### Interface
- UI envisioned as a series of tabs representing different sections of the ship, like Navigation, Engineering, and Manufacturing.

### Tables
- Display detailed information about inventory, crew status, and other logistical elements.

### Buttons
- Interactive buttons for issuing commands and performing various tasks.

### Progress Bars
- Display metrics like how much cargo or manufacturing space is left.

### Notifications
- Informative alerts for key events or status changes.

---

## 4. Additional Features
- The game blends elements of logistics, resource management, and narrative choice into a compelling space exploration setting.

---

## 5. Simplified Game Iteration

### UI Design
- Text and tables-based interface, no graphics.
- No trade interactions; the focus is on resource management and navigation.

### Crew Management
- Crew members are represented as numbers.
- No individual health or security metrics for crew members.

### Game Sections
- **Bridge**: Summary and status area.
- **Navigation**: Local system details and list of nearby stars.
- **Engineering**: Ship modules, manufacturing, and blueprints.
- **Quartermaster**: Cargo and supplies management.
- **Science**: Interpreting data and improving technologies.

### Immediate Questions
- Who is charting the system?
- Who is doing short and long-range scans?
- Who is responsible for sensors?
- Who will go "out" for tasks like installing mining equipment?

### Ship Composition
- To be determined based on the answers to the immediate questions.
