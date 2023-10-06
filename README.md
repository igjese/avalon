# Game Design Document for Avalon Sigma

## 1. Introduction

### Concept
The game is a space exploration and logistics management experience set in a half-broken ship at Alpha Centauri. Players wake up from cryo-sleep with a few crew members and aim to reach a mythical space colony, "Avalon Sigma."

### Objective
The end goal may involve reaching a mythical space colony like "Avalon Sigma."

### Target Audience
The game is designed for players who enjoy a single-player experience without time pressures, allowing for more thoughtful and strategic play.

### Ship Construction and Logistics Hierarchy
- **Ship Systems**: High-level assemblies that serve major functions on the ship (e.g., IonTek Drive, Vortex Power Core).
  - Assembled from Sub-Systems
- **Sub-Systems**: Variants or modular upgrades within a System (e.g., IonTek Drive, Plasma Drive within Propulsion).
  - Assembled from Components
- **Components**: Individual elements that combine to form a Sub-System (e.g., Thrust Coils, Ion Chamber).
  - Assembled from Parts and possibly other Components
- **Parts**: Smaller elements that are used to assemble Components (e.g., High-Conductivity Wiring, Vacuum-Tight Casing).
  - Manufactured from Materials
- **Materials**: Substances that are directly used to create Parts (e.g., Copper, Titanium).
  - Gathered, Mined, or Refined from Raw Materials
- **Raw Materials**: Natural substances found on celestial bodies (e.g., Copper Ore, Iron Ore).
  - Found on Planets, Moons, and Asteroids

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

### Crew Roles and Responsibilities
- Captain (Player): Responsible for overall decision-making.
- Pilot: Manages the Navigation section, responsible for steering the ship and making short-range scans.
- Chief Engineer (or simply Chief): Manages the Engineering section, responsible for repairs, upgrades, and power management.
- Purser: Manages the "Supplies and Cargo" section, responsible for keeping track of all resources and supplies.
- Doc: Manages the Life Support section, initially responsible for maintaining oxygen levels, water recycling, and food production. Could later be expanded to cover science, healthcare, etc.

### Other Mechanics

- **Throughput-Sensitive Systems**: Consideration for systems sensitive to the rate of material throughput.
- **Workflow Management Sub-System**: Manages the rate at which materials move through the manufacturing process.
- **Foundational Blueprints**: Initial set of blueprints for essential systems and components like mining drills, nanoassemblers, shuttles, drones, and bots.

---

## 3. UI and Technical Aspects

### Tech Stack
- Backend: Django
- Frontend: jQuery and Bootstrap

### Interface
- UI envisioned as a series of tabs representing different sections of the ship, like Navigation, Engineering, and Manufacturing.

Tabs/Ship sections:
- Bridge: Managed by the Captain, displays current location, ship status, and available crew members.
- Navigation: Managed by the Pilot, shows detailed information about the current star system and options for setting a course to other star systems.
- Engineering: Managed by the Chief, shows information about ship modules, power management, and available blueprints for upgrades or repairs.
- Supplies and Cargo: Managed by the Purser, shows your current supplies including food, water, and other essential and non-essential supplies.
- Life Support: Managed by Doc, shows the status of life-support systems like oxygen levels, water recycling, and food production.
- 
### UI elements
Tables:
- Display detailed information about inventory, crew status, and other logistical elements.

Buttons:
- Interactive buttons for issuing commands and performing various tasks.

Progress Bars:
- Display metrics like how much cargo or manufacturing space is left.

Notifications:
- Informative alerts for key events or status changes.

### Other Aspects

- **Assembly Lines**: Specialized manufacturing lines with dedicated bots.
- **Customizable Blueprints**: Allows players to design their own assembly lines with pre-defined settings.

---

## 4. Additional Features
- The game blends elements of logistics, resource management, and narrative choice into a compelling space exploration setting.
- Quasi-Random Interactions: The game includes quasi-random interactions that reveal the backstory and relationships between crew members. These interactions add a dynamic, unpredictable element to each playthrough, making the game more engaging and replayable.


---

## 5. Simplified Game Iteration

### UI Design
- Text and tables-based interface, no graphics.
- No trade interactions; the focus is on resource management and navigation.

### Crew Management
- Crew members now have specific roles: Captain, Pilot, Chief Engineer (Chief), Purser, and Doc.
- Each role comes with specific responsibilities and manages different sections of the ship.
- No individual health or security metrics for crew members.

### Game Sections
- **Bridge (Captain)**: Summary and status area.
- **Navigation (Pilot)**: Local system details and list of nearby stars.
- **Engineering (Chief)**: Ship modules, manufacturing, and blueprints.
- **Supplies and Cargo (Purser)**: Cargo and supplies management.
- **Life Support (Doc)**: Interpreting data and improving technologies.

### Immediate Questions
- Who is charting the system? (Pilot)
- Who is doing short and long-range scans? (Pilot)
- Who is responsible for sensors? (Pilot)
- Who will go "out" for tasks like installing mining equipment? (To be determined)

### Ship Composition
- Hull, Engines, Fuel Tanks, Storage/Cargo Area, Manufacturing Bay, Crew Quarters, Life Support Systems, Navigation Systems, Power Generators, Sensor Arrays.

## 6. Ship Blueprint with Fictional Component Names

### Bridge (Managed by Captain)
- **AstroCom Interface**: Main computer interface for managing ship operations.
- **Holosphere**: 3D holographic display for situational awareness.
- **StarLog**: Archive system to record ship logs and data.

### Navigation (Managed by Pilot)
- **PulsarNav System**: Advanced navigation system utilizing pulsar mapping.
- **SkySight Sensor Suite**: A combination of radar, lidar, and other sensors.
- **QuantCom Array**: Short-range and long-range communication system.

### Engineering (Managed by Chief)
- **IonTek Drive**: Main ion drive for system travel.
- **Vortex Power Core**: Main power generator.
- **NanoFix Drones**: Drones for internal and external repairs.
- **StellarFusion Backup Generators**: Backup power units.
- **CraftMaster 3000**: Manufacturing unit for making new components, repairs, etc.

### Supplies and Cargo (Managed by Purser)
- **StarHold Cargo Bays**: Main cargo holds.
- **NutriPod Food Storage**: Temperature and environment-controlled food storage.
- **TradeMate Interface**: Inventory management system.
- **AquaPurifier Max**: Advanced water purification and filtration system.

### Life Support and Cryo (Managed by Doc)
- **BioSphere Hydroponics**: Food growing system.
- **OxyGen Plus**: Main oxygen generation and regulation system.
- **MediVault**: Medical supplies storage and emergency treatment unit.
- **DeepSleep Cryo Pods**: Cryogenic sleeping pods.
- **VitalGuard Emergency Systems**: Backup life support utilities.

## 7. Minute-to-Minute Gameplay Challenges

- **Resource Management**: Challenges related to resource depletion alerts, resource surplus, and resource conversion.
- **Logistics**: Challenges related to queue management, load balancing, and transport issues.
