
## 10. Resources and Systems


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
