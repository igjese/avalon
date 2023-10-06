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

## 3. Architecture

### Tech Stack
- **Backend**: Django is used for the backend.
- **Frontend**: jQuery and Bootstrap are used for client-side interactions and styling.
  
### UI Components
- **DataTables**: DataTables for jQuery is used for most of the UI.

### MVC Architecture
- **Controller**: Holds all logic and flow.
- **View**: Responsible for routing requests and serving responses. When needed transforms data for UI consumption.
- **Model**: Fetches data using Django ORM.

---

## 4. Additional Features
- The game blends elements of logistics, resource management, and narrative choice into a compelling space exploration setting.
- Quasi-Random Interactions: The game includes quasi-random interactions that reveal the backstory and relationships between crew members. These interactions add a dynamic, unpredictable element to each playthrough, making the game more engaging and replayable.


---

## 5. Simplified Game Iteration

### UI Design
- Text and tables-based interface, no graphics.
- No trade interactions; the focus is on resource management and navigation.
- **Notifications**: Informative alerts for key events or status changes.

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

### Other Aspects

- **Assembly Lines**: Specialized manufacturing lines with dedicated bots.
- **Customizable Blueprints**: Allows players to design their own assembly lines with pre-defined settings.

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

## 8. Sensor Systems and Data Analysis

### Sensor Types
- **Astro-Body Sensor**: Detects planets, moons, asteroids, and other celestial bodies.
- **Resource Sensor**: Specifically designed to locate valuable minerals, elements, or other types of resources.
- **Life Form Sensor**: Detects biological entities.
- **Hazard Sensor**: Detects environmental dangers like radiation zones, black holes, or solar flares.

### Sensor Attributes
- **Range**: How far the sensor can scan.
- **Accuracy**: The likelihood that the data provided is correct.
- **Speed**: How quickly it generates new scans.
- **Power Consumption**: Higher-tier sensors might consume more power.

### Player Decisions
- **Sensor Management**: Deciding which sensors to run, considering their power consumption.
- **Data Interpretation**: Making educated guesses or taking risks based on sensor data.
- **Upgrade Planning**: When to invest in better sensors.

### Sensor-to-Analysis Chain
- **Raw Sensor Data**: Collected by various sensors.
- **Basic Analysis**: Run by the ship's basic computing facilities.
- **Advanced Analysis**: Requires specialized computing capabilities or algorithms.
- **Result Interpretation**: The player interprets the analyzed data.

### Upgrades
- **Sensors**: Better range, accuracy, speed, and lower power consumption.
- **Computing Hardware**: Faster processing speeds.
- **Software/Algorithms**: More efficient or specialized algorithms.
- **Data Storage**: Increased storage capabilities.

### Advanced Sensor Types
- **Spectral Sensors**: Used for identifying chemical compositions.
- **Radio Sensors**: Detect radio waves.
- **Gravitic Sensors**: Measure variations in gravitational fields.
- **Thermal Sensors**: For measuring heat signatures.

## 9. Game State and Real-Time Updates

### Single Timer Mechanism
- **Concept**: A single timer fetches all relevant data at regular intervals.
- **Advantages**: Reduces the number of timers and AJAX requests, optimizing the game as it grows in complexity.

### Game Loop Advancement
- **Concept**: The timer is not just fetching the game state; it actually advances the game loop.
