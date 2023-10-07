# Game Design Document for Avalon Sigma

## 1. Introduction

- **Concept**: A space exploration and logistics management game set in a half-broken ship at Alpha Centauri. Players wake up from cryo-sleep with a few crew members.
  
- **Objective**: Aim to reach a mythical space colony, "Avalon Sigma."

- **Target Audience**: Designed for players who enjoy a single-player experience without time pressures, allowing for thoughtful and strategic play.


## 2. Story and Setting

Player wakes up from cryo-sleep on FSS Adequate, together with a few crew members as refugees from Earth. Their aim is to reach a mythical space colony, "Avalon Sigma." 

Setting is deep-space and lonely. Player does most of interaction from bridge of the spaceship, checking reports and issuing commands.


## 3. Core Game Mechanics

- Managing and automating production
- Strategic resource allocation
- Upgrading ship capabilities
- Exploration and travel to different star systems
- Design blueprints for new components 

## 4. Technology and Architecture

### Tech Stack
- **Backend**: Django is used for the backend.
- **Frontend**: jQuery and Bootstrap are used for client-side interactions and styling.

### UI Components
- **DataTables**: DataTables for jQuery is used for most of the UI.

### MVC Architecture
- **Controller**: Holds all logic and flow.
- **View**: Responsible for routing requests and serving responses. When needed, transforms data for UI consumption.
- **Model**: Fetches data using Django ORM.

## 5. Art and Audio

- No audio for now, maybe later ambiental space-music (open source)
- Single visual: Bridge shows orbited body on big screen.
- Visual for celestial bodies varies by type (e.g. rocky planet) and size, to give some differentiation.

## 6. User Interface

### Overall Approach

- Office-like UI: Text and tables-based interface with almost no graphics.
- Ship's Bridge is the center. From the bridge player access all sections of a ship, and through them everything else.
- There is big visual of orbited body on the bridge.
- Bridge has alert feed: notifications of key alerts or status change.
- Some dashboards for statuses.
- Charts for production/consumption data.

### Tabs
- **Supplies and Cargo**: Tab for managing resources.
- **Ship Systems**: Tab for system efficiencies and statuses.
- **Admin/Debug**: Development tools, logs, export/import, etc

## 7. Models

### Ship 

Ship consists of ShipSystems, which consist of Components:
- **ShipSystem**: Logical groups of ship's sub-systems, organized by ship's high-level functions. E.g., Navigation, Engineering, etc.
- **SubSystem**: Collection of components that together provide single function within a ship's sytem. E.g. Atmosphere control subsystem within Life Support system.
- **Component**: Individual elements that consume and produce stuff (resources, parts, components). Assembled from Parts and possibly other Components
- **Part**: Smaller elements that are used to assemble Components (e.g., High-Conductivity Wiring, Vacuum-Tight Casing). Manufactured from Materials

Ship systems and their subsystems in the game:
- **Bridge**: MainComputer, ShipsLog
- **Navigation**: Communication, Sensors, Astrogation
- **Engineering**: Propulsion, Power, Manufacturing, Maintenance
- **Supplies and Cargo**: CargoBay
- **Provisions**: Hydroponics, FoodFarms
- **Life Support**: WaterReclamation, AtmosphereControl, Cryonics, Medical
- **Crew**: Personell

### Resources and Storage

Resource:
- Represent anything that can be stored, produced, consumed
- Each resource has StorageType, defining where it can be stored
- Resources in the game are: Air, Nutrients, Water, WasteWater, FuelCells, Energy, Hydrogen, Oxygen, Food

StorageType:
- Represent in what kind of StorageUnit resource can be stored
- Storage types in the game are: Air, GeneralCargo, SpecialCargo, Fluid, SpecialFluid, Energy

StorageUnit:
- Storage container for specific StorageType
- Can be installed in ship's subsystem as InstalledStorageUnit
- Storage units in the game: BatteryBank (for Energy), CargoHold (for general cargo), RegulatedCargoHold (for Food), FluidTank (for Water, WasteWater), PressurizedFluidTank (for Oxygen, Hydrogen), GeneralShipAir (for Air)
- RegulatedCargoHold, FluidTank and PressurizedFluidTank can store only single type of resource at one time
- CargoHold stores any number of resources at same time

InstalledStorageUnit:
- Specific storage unit installed into specific ship subsystem
- Subsystem can have multiple installed storage units of the same type

### Components


### Universe and Ship Location Models
- **Universe Model**: Describes the hierarchy of celestial bodies.
- **Ship Location Model**: Describes the ship's status and location.

### Bots and Shuttles in Resource Management
- **Bots**: Handle resource transport within the ship.
- **Shuttles**: Handle resource transport outside the ship.

### Resource Transaction Schema and Reporting
- **Resource Transaction Schema**: Describes how resource transactions are logged and reported.


## 8. Gameplay Mechanics
  

### Production Chains
- Food: Needs water, energy, and nutrients.
- Any production requires energy.

### Strategy and Planning
- Resource Scarcity: Planets and other locations offer limited resources.
- Planet vs Ship manufacturing: Limited but mobile manufacturing capabilities on the ship, vs extensive but stationary manufacturing options on planets.
- Upgradable Ship: Spend resources and manufacturing capacity to upgrade different aspects of the ship, from cargo space to manufacturing efficiency or defense capabilities.
- Exploration and Expansion: Player can explore new planets and systems to find resources or even a permanent settlement.

### Crew Responsibilities
- **Captain**: Player. Responsible for overall decision-making.
- **Pilot**: Manages Navigation, responsible for steering and scans.
- **Chief Engineer**: Manages Engineering, responsible for repairs, power and drives.
- **Purser**: Manages Supplies and Cargo, responsible for resources and supplies.
- **Doc**: Manages Life Support, responsible for oxygen, food and water.

### Ship Sections
- **Bridge (Captain)**: Summary and status area.
- **Navigation (Pilot)**: Local system details and list of nearby stars.
- **Engineering (Chief)**: Ship modules, manufacturing, and blueprints.
- **Supplies and Cargo (Purser)**: Cargo and supplies management.
- **Life Support (Doc)**: Interpreting data and improving technologies.

### Customizable Blueprints

- Player can design new components by creating blueprints.
- Ship starts with initial set of blueprints for essential systems and components like mining drills, nanoassemblers, shuttles, drones, and bots.




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

### Key Points (continued)

- Specialized containers are strictly reserved for their designated resources.
- Intangible resources like "Air" will use the same storage mechanism as tangible resources.
- Energy and fluids have "magical" instantaneous flow and are either available or not.
- No concurrency in resource allocation; a random system gets the resources if not enough are available.
- MaxCapacity is a calculated value and will not be stored in the database.
- Transport mechanisms like bots and shuttles are outside the scope of this resource storage model for now.

### Assumptions and Limitations

- Specialized storage units cannot be used for general cargo.
- Energy, fluids, and special fluids each have their own separate storage types.
- Resource dependencies can be calculated from the components and don't need to be explicitly stored.

### Future Considerations

- A priority system for resource allocation may be implemented later for more depth in resource management.
- Transport mechanisms like bots and shuttles may require a separate design discussion.

### Implementation Steps

1. Maintain the reservation of specialized containers for specific resources.
2. Implement the same storage mechanism for both tangible and intangible resources.
3. Document the assumptions of "magical" instantaneous flow for energy and fluids.
4. Keep the initial design simple, with the option to optimize MaxCapacity calculations later.

## 19. Bots and Shuttles in Resource Management

### Bots

1. **Capacity**: Fixed amount X, upgradable for better bots.
2. **Transport Time**: 1 tick within a subsystem, 5 ticks within a system, 10 ticks within a ship.
3. **Resource Types**: Can carry any "itemized" resource, defined by storage types.
4. **Task Assignment**: Two methods: A. Component requests and B. Captain's orders.
5. **Resource Prioritization**: Bots are designed to be "stupid" for gameplay challenge.
6. **Concurrency**: Operate in ticks, take random requests from a list.
7. **Energy Requirement**: Require power, slow down when power is low.
8. **Bot Assignment**: Some bots are "free roaming," others are system-specific.

### Shuttles

1. **Capacity**: Depends on installed storage units.
2. **Transport Time**: X ticks depending on distance.
3. **Resource Types**: Depends on installed storage units.
4. **Task Assignment**: Manual and automatic, player-driven.
5. **Inter-ship Transfer**: Possible, based on route and wishlist.
6. **Docking Requirements**: To be determined.
7. **Energy Requirement**: Require fuel, possibly the same as the ship.

### General Considerations

1. **Pathfinding**: None, by design.
2. **Failures/Breakdowns**: Not yet implemented.
3. **Upgrades**: Bots can be upgraded, shuttles depend on blueprint.

### Additional Points

- **Transition**: Resources will magically appear in storage, tracked in a "ship's log."
- **UI/UX**: Office-like UI table for shuttles, no tracking for bots.
- **Load Balancing**: Random task selection for bots, manual assignment for shuttles.
- **Emergency Situations**: Captain can assign "priority requests" and allocate a percentage of bots.
- **StoredResource Junction Table**: To manage multiple types and units of storage for one resource.

## 20. Gameplay Constraints and Considerations

### Component Processing

- Components will be processed in a random order every tick.
- Components may require multiple ticks to complete a production cycle.
- If not enough inputs are available, the component reserves what it can but doesn't start the cycle.

### Resource Management

- Components will have a built-in buffer to reserve resources for up to two production cycles.
- If a component can't output its production due to lack of storage, it waits for the next cycle.

### Time Management

- Game time will be mapped to real time, with 1 real-life minute equating to 1 in-game hour.
- Component processing times will be defined in terms of in-game time.

### Status and Reporting

- Machines will have statuses like "Idle," "Running," "Paused for Input," etc.
- These statuses can be aggregated for a global view, potentially aiding in player decision-making.

### Buffering Considerations

- Energy will not be buffered; it is consumed as generated.
- Fluids will be buffered similarly to itemized resources.


## 21. Resource Transaction Schema and Reporting

### Resource Transaction Schema (Simplified)

- **Timestamp**: When the transaction occurred in "game time."
- **Resource Type**: The kind of resource involved (e.g., Energy, Oxygen).
- **Transaction Type**: The type of transaction (Produced or Consumed).
- **Amount**: The quantity of the resource involved.
- **System ID**: Identifier for the system involved (e.g., Power Plant).
- **Subsystem ID**: Identifier for the subsystem within the system (if applicable).
- **Location ID**: Identifier for where this resource is stored or where the transaction happened.

#### Example Log Line or Database Record (Simplified)
Timestamp | Resource_Type | Transaction_Type | Amount | System_ID | Subsystem_ID
1001 | Energy | Produce | 50 | 1 | 2
1002 | Oxygen | Consume | 10 | 1 | 3
