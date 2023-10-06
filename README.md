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

## 10. Resources and Systems

### Food, Water, and Oxygen

- **Food**: Consumed by the crew but can be produced in hydroponics facilities.
  - **Resource Dependencies**: Consumes water, energy, and potentially nutrients.
  - **Emergency Measures**: Rations can be reduced for a short time before causing health effects.
  
- **Water**: Consumed by the crew and used in hydroponics.
  - **Resource Dependencies**: Requires energy for purification and recycling.
  - **Emergency Measures**: Can be rationed more easily but with long-term consequences.
  
- **Oxygen**: Consumed by the crew.
  - **Resource Dependencies**: Requires energy, and potentially water if using electrolysis.
  - **Emergency Measures**: Can be rationed to an extent, but this has immediate health risks.

### New Systems and UI

- **Energy Stored**: A new resource, similar to food, water, and oxygen.
- **Crew as a System**: Consumes resources like food, water, and oxygen.
- **UI Tabs**: "Supplies and Cargo" for resources and "Ship Systems" for system efficiencies and statuses.
- **Power Plants**: Produces energy and consumes fuel.
- **Hydroponic Vats, Water Recyclers, Oxygen Generators**: Systems that produce essential resources.
- **Resource Consumption per Tick**: Game loop accounts for resource consumption and production.
- **Efficiency in Numbers**: Represented as a fraction (e.g., 5/7 machines working).

## 11. Systems and Components

### Ship Systems and Subsystems

- **ShipSystem**: An umbrella term for a specific system on the ship, such as "Power Generators," "Water Recycling," or "Hydroponics."
- **Component**: A specific piece of hardware or software within a ShipSystem that does the actual work. For example, "Hydrogen Fuel Cell," "Solar Panel," or "Water Filter."

### Crew as a System

- **Crew**: Considered as a "system" within the ship.
  - **Subsystems**: "Staff" and "Bots" (Bots not implemented yet).
  - **Components**: "Specialists" under "Staff" subsystem.
  
### Resource Consumption and Production

- **Staff**: Consumes 1 of each resource (Food, Water, Oxygen, maybe Energy) every tick.
- **Bots**: Consume 0 resources for now but could consume Energy in the future.

### Efficiency and Status

- **Crew Member Efficiency**: Depends on health, morale, and the quality of their equipment.

### Emergency Protocols

- **Power-Saving Mode**: Could reduce everyone's workload but also lower the ship's overall efficiency.

### Food Production System
- **Subsystem**: Hydroponic Vats
- **Component**: AgroVats2400
  - **Consumes**: Energy, Water, Nutrients
  - **Produces**: Food

#### AgroVats2400 Sub-components
- **UV Lights**: Consumes energy, necessary for plant growth.
- **Planting Boxes**: Holds the plants; doesn't consume or produce resources but might affect efficiency.
- **Nutrient Dispensers**: Consumes "Nutrients," necessary for plant growth.

### New Resources Introduced
- **Nutrients**: Consumed by Hydroponic Vats for food production.
  
### Design Decisions

#### Blueprint Designer
- Allows players to customize the AgroVats2400 component.
- Once a blueprint is designed, its inputs and outputs are fixed.

#### Resource Management
- Introduce "Nutrients" as a new resource for Hydroponic Vats.

### Updated Systems and Components

#### Galley and Provisions
- **Subsystem**: Astro-Farms
- **Component**: AgroGenesis 9000
  - **Inputs**: Energy, Water, Nutrients
  - **Outputs**: Food
  - **Description**: Employs cutting-edge hydroponics to cultivate food in a closed-loop system, minimizing waste and maximizing yield.

#### Environmental Control
- **Subsystem**: Liquid Reclamation Unit
- **Component**: AquaPurifier Mk IV
  - **Inputs**: Waste Water
  - **Outputs**: Water
  - **Description**: Converts waste water back into clean, usable water through a series of filtration and distillation processes.

#### Life Support Systems
- **Subsystem**: Atmosphere Control Unit
- **Component**: OxyGenius S-2
  - **Inputs**: Water, Energy
  - **Outputs**: Air, Waste Water
  - **Description**: Employs electrolysis to split water molecules into breathable air and waste byproducts.

- **Subsystem**: Air Circulation Unit
- **Component**: AeroMixer 5000
  - **Inputs**: Oxygen, Trace Gases (Nitrogen, Argon, etc.)
  - **Outputs**: Air
  - **Description**: Takes pure oxygen and combines it with trace gases to produce a breathable air mixture.

#### Engineering Bay
- **Subsystem**: Power Plant
- **Component**: FusionMaster Alpha
  - **Inputs**: Fuel Cells, Water
  - **Outputs**: Energy, Waste Water
  - **Description**: Utilizes fuel cells and a water-cooling system to generate a constant and reliable flow of energy.

### New Resources Introduced
- **Air**: Produced by the AeroMixer 5000 and consumed by the ship's crew.
- **Fuel Cells**: Used by the FusionMaster Alpha for energy production.

### Design Decisions
- Renamed "Fuel" to "Fuel Cells."
- Introduced "Air" as a new resource.
- Updated component names to be more thematic (navy and/or SF).

## 12. Debug Page

### Overview
- The Debug Page is a separate interface for development and debugging purposes.
- It should freeze the game loop to allow for real-time analysis and adjustments.
- The page will have two main tabs: "Logs" and "Data."

### Logs Tab
- **Purpose**: To display logs for debugging.
- **Features**: 
  - Real-time log display.
  - Replaces the use of print commands for debugging.
  
### Data Tab
- **Purpose**: To display and manipulate game data.
- **Features**: 
  - Database dump in JSON format displayed on-screen.
  - "Copy to Clipboard" button to easily share or save the database state.

### Design Decisions
- The Debug Page will be accessible only in development builds to prevent end-users from accessing it.
- It will have the capability to freeze the game loop for in-depth analysis.

## 13. Model

StorageType - type of Storage required by a resource (Cargo, SpecialCargo, Fluid, SpecialFluid, Air, Energy, etc)

## 14. Resource Tracking

- **Single Source of Truth**: Storage units will serve as the single source of truth for resource quantities.
- **Resource Table**: The `Resource` table will no longer have a `quantity` field. Resource quantities will be calculated dynamically based on storage units.
- **Game Tick**: At each game tick, resource quantities will be recalculated based on the `currently_stored` values in each storage unit.

## 15. World State

- **World Object**: Introduce a `World` object to manage the game state.
- **Locations**: The `World` object will manage various locations, starting with the ship.
- **Database**: All entities managed by the `World` object will be stored in the database.

Future consideration:
- The `World` object can be extended to manage other locations like planets, space stations, and more.

## 16. Universe and Ship Location Models

### Universe Model

- **Hierarchy**: Universe > Star System > Stars > Planets > Moons, also: Artificial Structures, Ship
- **Types of Stars**: O-Type, B-Type, A-Type, F-Type, G-Type, K-Type, M-Type, Red Giant, White Dwarf, Neutron Star, Blue Giant
- **Types of Planets**: Rocky, Gas Giant, Ice Giant, Volcanic, Water World
- **Types of Moons**: Rocky, Icy, Volcanically Active, Iron
- **Characteristics**: Tidally Locked, Atmosphere-bearing

### Ship Location Model

- **Status**: In transit, Docked, Landed, In orbit
- **Location**: Reference to a celestial body or coordinates
- **Consideration**: Radial coordinates for more granularity

### Admin Panel

- **Data Dump Button**: Expand into a full-fledged admin panel
- **Features**: Data import/export, entity management, real-time analytics

### Drawing Maps

- **Navigation Tab**: Feature star maps for interactive exploration
- **Purpose**: Planning routes, marking notable locations, strategic gameplay

### Bridge UI

- **Alerts and Statuses**: Central hub for game alerts
- **Visuals**: Change per orbited body for a dynamic experience

## 17. Current Milestones

### In Progress

#### Storage Model
- Finalizing how resources are stored and managed in various storage units.

#### Location Model
- Deciding how to model locations such as planets, moons, and star systems, and how to track the ship's current location.

#### Admin Panel
- Starting with basic features like export/import functionality.
- Incorporating logs that are already in place.

### Upcoming Milestones

#### Logistic Bots
- Implementing bots that handle the transferring, stocking, and management of resources.

#### Celestial Hierarchy
- Setting up a model to describe the hierarchy of celestial bodies like stars, planets, moons, etc.
- Creating basic rules for procedurally generating these celestial bodies.

#### Navigation
- Adding a star map and a system map, potentially with some interactive features for route planning or exploration.

#### Bridge
- Building a central dashboard for alerts, statuses, and visuals based on the ship's current location.

## 18. Storage Model Revisions

### Storage Types and Units

- **Resource**: Master list of all resources, linked to `StorageType` via a foreign key.
- **StorageType**: Types of storage possible (e.g., tanks, crates).
- **StorageUnit**: Actual storage units, linked to `StorageType`.
- **InstalledStorageUnit**: Storage units installed on the ship, linked to `StorageUnit`.

### General Cargo Hold

- **GeneralCargoHold**: A new table to represent a generic storage area.
- **GeneralCargoResource**: A junction table between `GeneralCargoHold` and `Resource` to manage multiple types of resources in a single cargo hold.

### Relationships

- 1:N relationship between `GeneralCargoHold` and `Resource` through `GeneralCargoResource`.

### Logic Changes

- **Specific Cargo**: Resources are stored in specialized storage units (`InstalledStorageUnit`), each linked to a specific `StorageType`.
- **General Cargo**: Resources not stored in specialized units go into `GeneralCargoHold`, managed through `GeneralCargoResource`.
- The model allows for multiple types of resources in each `GeneralCargoHold`, each with its own quantity.

