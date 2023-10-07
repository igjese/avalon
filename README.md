# FSS Adequate - Game Design Document

## 1. Introduction

- **Concept**: A space exploration and logistics management game set in a half-broken ship at Alpha Centauri. Players wake up from cryo-sleep with a few crew members.
- **Objective**: Flee from Earth, survive, and try to reach a mythical space colony, "Avalon Sigma."
- **Target Audience**: Designed for players who enjoy a single-player experience without time pressures, allowing for thoughtful and strategic play.


## 2. Story and Setting

Player wakes up from cryo-sleep as captain of FSS Adequate, with several crew members aboard. They are fleeing from Earth, trying to reach a mythical space colony, "Avalon Sigma." 

Setting is deep-space and lonely. Player does most of the interaction from bridge of the spaceship, checking reports and issuing commands.


## 3. Core Game Mechanics

- **Automate Production**: Keep your ship's systems running smoothly by automating resource production.
- **Resource Strategy**: Decide where to put your resources for the best long-term gains.
- **Ship Upgrades**: Use resources to make your ship better, faster, and more efficient.
- **Explore Star Systems**: Hop between star systems to find new resources or a place to call home.
- **Make Blueprints**: Design and build new components to improve your ship's capabilities.

What wil NOT be implemented:
- Trade, Multiplayer

## 4. Implementation

### Tech Stack
- **Backend**: Django is used for the backend.
- **Frontend**: jQuery and Bootstrap are used for client-side interactions and styling.

### UI Components
- Most of the data is shown using Django templates, based on request/response.
- **DataTables**: DataTables for jQuery is used for most of the complex data.

### MVC Architecture
- **Controller** (ctrl.py): Holds all logic and flow.
- **View** (views.py): Responsible for routing requests and serving responses. When needed, transforms data for UI consumption.
- **Model** (models.py): Django ORM.

### Game Loop
- A single ajax timer advances game loop and fetches whole gamestate in regular intervals (ticks).
- Game tick is 10 seconds.

### Time Management

- Game time is mapped to real time, with 1 real-life minute equating to 1 in-game hour.
- Component processing times are defined in terms of in-game time.

### Debug Page
- The Debug Page is a separate interface for development and debugging purposes.
- It should freeze the game loop to allow for real-time analysis and adjustments.
- The page will have two main tabs: "Logs" and "Data."

Logs: 
- displays log entries in DataTable
- replaces the use of print commands for debugging

Data: 
- Database dump in JSON format displayed on-screen.
- "Copy to Clipboard" button to easily share or save the database state.
- Import/Export data

### Resource Tracking

- **Single Source of Truth**: Storage units serve as the single source of truth for resource quantities.
- **Aggregations**: total resource quantities are recalculated each tick, for easier processing

### Game State

- **World Object**: Introduce a `World` object to manage the game state.


## 5. Art and Audio

- No audio for now, maybe later: ambiental space-music, alert and feedback sounds
- Single visual: Bridge shows orbited body on big screen.
- Visual for celestial bodies varies by type (e.g. rocky planet) and size, to give some differentiation.

## 6. User Interface

### Overall Approach

- Office-like UI: Text and tables-based interface with almost no graphics.
- Ship's Bridge is the center. From the bridge player access all sections of a ship, and through them everything else.

### Tabs
- **Supplies and Cargo**: Tab for managing resources.
- **Ship Systems**: Tab for system efficiencies and statuses.
- **Admin/Debug**: Development tools, logs, export/import, etc
- **Navigation**: Stars map, System map
- **Bridge**: Alerts, Statuses, Visual of orbited body

#### Future Considerations
- Some dashboards for statuses.
- Charts for production/consumption data.

## 7. Database Models

Database Entities:
- **ShipSystem**: Logical containers for groups of sub-systems, organized by the ship's high-level functions.
- **SubSystem**: Collections of components that together provide a single function within a ship's system.
- **Component**: Specific pieces of hardware within a ShipSystem that consume and produce resources.
- **Resource**: Anything that can be stored, produced, or consumed.
- **StorageType**: Defines what kind of StorageUnit a resource can be stored in.
- **StorageUnit**: Containers for specific types of resources.
- **InstalledStorageUnit**: Specific storage units installed into specific ship subsystems.
- **StoredResource**: Specific resources assigned to be stored in specific installed storage units.
- **InstalledComponent**: Specific components installed into specific ship subsystems.
- **World Object**: Manages the overall game state.

Not implemented yet:
- **Part**: Smaller elements used to assemble Components.
- **ResourceTransaction**: Source for historical data for resource production and consumption.
- **Crew Members**: Characters with unique skills and responsibilities.
- **Bots**: Handle internal transport of resources.
- **Shuttles**: Handle resource transport outside the ship.


### Ship

Ship consists of ShipSystems, which consist of Components:
- **ShipSystem**: An umbrella term for a logical container for group of sub-systems, organized by ship's high-level functions. E.g., Navigation, Engineering, etc.
- **SubSystem**: Collection of components that together provide single function within a ship's sytem. E.g. Atmosphere control subsystem within Life Support system.
- **Component**: A specific piece of hardware within a ShipSystem that does the actual work. Consumes resources and produces resources or other Components. Assembled from Parts and other Components.
- **Part**: Smaller elements that are used to assemble Components. Manufactured from Resources and Parts.

Ship systems and their subsystems in the game:
- **Bridge**: MainComputer, ShipsLog
- **Navigation**: Communication, Sensors, Astrogation
- **Engineering**: Propulsion, Power, Manufacturing, Maintenance
- **Supplies and Cargo**: CargoBay
- **Provisions**: Hydroponics, FoodFarms
- **Life Support**: WaterReclamation, AtmosphereControl, Cryonics, Medical
- **Crew**: Personell

### Resources and Storage
In general:
- Specialized containers are strictly reserved for their designated resources.
- Intangible resources like "Air" will use the same storage mechanism as tangible resources.
- Energy and fluids have "magical" instantaneous flow and are either available or not.
- No concurrency in resource allocation; a random system gets the resources if not enough are available.
- MaxCapacity is a calculated value and will not be stored in the database.
- Specialized storage units cannot be used for general cargo.
- Energy, fluids, and special fluids each have their own separate storage types.

#### Models

Resource:
- Master list of all resources
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

StoredResource:
- Specific resource assigned to be stored specific installed storage unit
- Holds quantity information

### Components

Component:
- Consumes and produces resources
- Production and consumptions historical data is tracked in ResourceTransactions
- Can be installed in ship's subsystem as InstalledComponent
- Components in game are: AeroMixer, FusionMaster, OxyGenius, AquaPurifier, AgroGenesis, Specialist

InstalledComponent:
- Specific component installed into specific ship subsystem
- Quantity defines how many are installed there

ResourceTransaction:
- Source for historical data for charts etc
- Fields: timestamp, resource id, produced qty, consumed qty, system id, subsystem id

### Future Considerations

#### Universe

- **Hierarchy**: Universe > Star System > Stars > Planets > Moons
- Also: Artificial Structures, Ships (the Ship?), other celestial bodies
- Types of Stars: O-Type, B-Type, A-Type, F-Type, G-Type, K-Type, M-Type, Red Giant, White Dwarf, Neutron Star, Blue Giant
- Types of Planets: Rocky, Gas Giant, Ice Giant, Volcanic, Water World
- Types of Moons: Rocky, Icy, Volcanically Active, Iron
- Characteristics for planets and moons: Tidally Locked, Atmosphere-bearing

### Ship and Locations

- **Ship Status**: In transit, Docked, Landed, In orbit
- **Location**: Reference to a celestial body or coordinates


## 8. Gameplay Mechanics

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


### Production Chains

| Component    | SubSystem                | Produces           | Consumes                 |
|--------------|--------------------------|--------------------|--------------------------|
| AgroVats     | Hydroponic Vats          | Food               | Energy, Water, Nutrients |
| AquaPurifier | Liquid Reclamation Unit  | Water              | WasteWater               |
| OxyGenius    | Atmosphere Control Unit  | Air, WasteWater    | Water, Energy            |
| AeroMixer    | Air Circulation Unit     | Air                | Oxygen, Air              |
| FusionMaster | Power Plant              | Energy, WasteWater | Fuel Cells, Water        |


### Customizable Blueprints

- Player can design new components by creating blueprints.
- Ship starts with initial set of blueprints for essential systems and components like mining drills, nanoassemblers, shuttles, drones, and bots.


### Resource Management

Approach:
- Components will be processed in a random order every tick.
- Components request resources
- Fluids and Energy are instantly available
- Itemized resources are delivered by bots

Notes:
- Components may require multiple ticks to complete a production cycle.
- If not enough resources are available, the component uses built-in buffer to store what it can but doesn't start the cycle.
- If a component can't output its production due to lack of storage, it waits for the next cycle.
- Machines will have statuses like "Idle," "Running," "Waiting for Resources," "Waiting for Storage", etc.
- Energy will not be buffered; it is consumed as generated.
- Fluids will be buffered similarly to itemized resources.
- Fluids and energy flow magically and are instantly transported if available
- Bots pick random requests for itemized resources
- Loading/Unloading: Resources will magically appear in storage, tracked in a "ship's log."
- Load Balancing: Random task selection for bots, manual assignment for shuttles.
- Emergency Situations: Captain can assign "priority requests" and allocate a percentage of bots.

### Efficiency
- Efficiency for sub-systems is represented as a fraction (e.g., 5/7) how many machines are operational out of total installed machines.

### Crew as a System

- Crew is onsidered as a "system" within the ship.
- Subsystems are "Personell" and "Bots".
- Actual people are Components of type "Specialist", as mechanism for them to consume resources.

#### Celestial Hierarchy
- Setting up a model to describe the hierarchy of celestial bodies like stars, planets, moons, etc.
- Creating basic rules for procedurally generating these celestial bodies.

### Bots

Bots handle internal transport of resources.

1. **Capacity**: Fixed amount X, upgradable for better bots.
2. **Transport Time**: 1 tick within a subsystem, 5 ticks within a system, 10 ticks within a ship.
3. **Resource Types**: Can carry any "itemized" resource, defined by storage types.
4. **Task Assignment**: Two methods: A. Component requests and B. Captain's orders.
5. **Resource Prioritization**: Bots are designed to be "stupid" for gameplay challenge.
6. **Concurrency**: Operate in ticks, take random requests from a list.
7. **Energy Requirement**: Require power, slow down when power is low.
8. **Bot Assignment**: Some bots are "free roaming," others are system-specific.

### Shuttles

Shuttles handle resource transport outside the ship.

1. **Capacity**: Depends on installed storage units.
2. **Transport Time**: X ticks depending on distance.
3. **Resource Types**: Depends on installed storage units.
4. **Task Assignment**: Manual and automatic, player-driven.
5. **Inter-ship Transfer**: Possible, based on route and wishlist.
6. **Docking Requirements**: To be determined.
7. **Energy Requirement**: Require fuel, possibly the same as the ship.


### Future Considerations

#### Logistics
- **Drones**: Mining drones.
- **Shuttles**: 

### Sensors
Sensor Types
- **Astro-Body Sensor**: Detects planets, moons, asteroids, and other celestial bodies.
- **Resource Sensor**: Specifically designed to locate valuable minerals, elements, or other types of resources.
- **Life Form Sensor**: Detects biological entities.
- **Hazard Sensor**: Detects environmental dangers like radiation zones, black holes, or solar flares.

Sensor Attributes
- **Range**: How far the sensor can scan.
- **Accuracy**: The likelihood that the data provided is correct.
- **Speed**: How quickly it generates new scans.
- **Power Consumption**: Higher-tier sensors might consume more power.

Sensor-to-Analysis Chain
- **Raw Sensor Data**: Collected by various sensors.
- **Basic Analysis**: Run by the ship's basic computing facilities.
- **Advanced Analysis**: Requires specialized computing capabilities or algorithms.
- **Result Interpretation**: The player interprets the analyzed data.

Upgrades
- **Sensors**: Better range, accuracy, speed, and lower power consumption.
- **Computing Hardware**: Faster processing speeds.
- **Software/Algorithms**: More efficient or specialized algorithms.
- **Data Storage**: Increased storage capabilities.

Advanced Sensor Types
- **Spectral Sensors**: Used for identifying chemical compositions.
- **Radio Sensors**: Detect radio waves.
- **Gravitic Sensors**: Measure variations in gravitational fields.
- **Thermal Sensors**: For measuring heat signatures.

