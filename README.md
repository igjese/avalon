# FSS Adequate - Game Design Document

## 1. Introduction

- **Concept**: A space exploration and logistics management game set in a half-broken ship at Alpha Centauri. Players wake up from cryo-sleep with a few crew members.
- **Objective**: Flee from Earth, survive, and try to reach a mythical space colony, "Avalon Sigma."
- **Target Audience**: Designed for players who enjoy a single-player experience without time pressures, allowing for thoughtful and strategic play.


## 2. Story and Setting

Player wakes up from cryo-sleep as captain of FSS Adequate, with several crew members aboard. They are fleeing from Earth, trying to reach a mythical space colony, "Avalon Sigma." 

Setting is deep-space and lonely. Player does most of the interaction from bridge of the spaceship, checking reports and issuing commands.


## 3. Core Game Mechanics

- **Automate Production**: Set up systems to automatically create and manage resources, to scale up your own capabilities.
- **Resource Strategy**: Decide where to put your resources, to prioritize short- or long-term needs.
- **Ship Upgrades**: Design better parts and components to make your ship and other assets more effective.
- **Explore Star Systems**: Travel between star systems in search for resources and places suitable as base of operations.
- **Make Blueprints**: Design and build new components to create specialized hardware for specific situations.
- **No Dying**: Instead of dying, game employs emergency backup systems, which apply penalties instead until the crisis is resolved.

What wil NOT be implemented:
- Trade, Multiplayer

### Example: First Minutes of Gameplay

1. **Air supply is dwindling**: Player realizes the air supply is dwindling.
2. **Some components are broken**: Player checks life support status to identify 2 out of 3 OxyGeniuses are broken.
3. **We lack parts to fix them**: Player checks inventory for repair bots and parts, considering specific or generic "repair packs."
4. **Scan the system for the resources we need**: Player uses sensors to scan for needed resources, possibly needing to repair sensors first.
5. **Drones gather resources**: Player travels to resource location or use shuttles, to employ mining drones.
6. **Refine them into usable materials**: Player refines raw resources into usable materials.
7. **Manufacture repair parts**: Player uses production facilities to create repair parts or packs.
8. **Repair broken components**: Player allocates repair bots and parts to fix malfunctioning OxyGeniuses.


## 4. Implementation

### Tech Stack
- **Backend**: Django is used for the backend.
- **Frontend**: jQuery and Bootstrap are used for client-side interactions and styling.

### UI Components
- **Bootstrap Tabs** represent ship sections and sub-tabs display relevant info and data for each section.
- **Django Templates** populate the data in request/response cycle.
- **single js timer** updates "realtime" data every game tick.
- **DataTables** for jQuery are used for most of the complex data.
- **Highcharts** is used for charting

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

### View Model

- Instead of complex data transformations on the frontend, we'll have separate data model for presentation
- This View Model will be prepared by the View every time it needs to send data to the frontend
- Example: data for consumption/production charts, which needs to be aggregated first

## 5. Art and Audio

- No audio for now, maybe later: ambiental space-music, alert and feedback sounds
- Single visual: Bridge shows orbited body on big screen.
- Visual for celestial bodies varies by type (e.g. rocky planet) and size, to give some differentiation.

## 6. User Interface

### Overall Approach

- Office-like UI: Text and tables-based interface with almost no graphics.
- Ship's Bridge is the center. From the bridge player access all sections of a ship, and through them everything else.
- There is separate Debug page, with development and debugging tools, such as logs, imports/exports etc

### Tabs and Sub-Tabs
- **Bridge**: 
    - **Ship Status**: Critical resources, Maintenance alerts
    - **Ship Systems**: Shows components installed in each subsystem, along with which system it belongs to, plus how many are operational out of total installed number i.e. 3/5
- **Engineering**: Displays a list of maintenance requests. Each line item displays what part is needed and has toggle for "Priority repair".
- **Navigation**: Stars map, System map
- **Supplies and Cargo**:
    - **Current storage levels**: Displays for each resource quantity in storage plus max storage capacity. Shared capacity is indicated as e.g. "1000 (shared)"
    - **Production/Consumption**: Displays Production/Consumption charts (explained below)
- **Reference**: displays all the game info player needs about game systems and mechanics
    - **Components**: For each available component: how it functions, what does it consume and produce.
    - **Storage Types**: Game storage types, and explanation for each.

### Production/Consumption Charts

- Three interactive charts provide resources overview over time:
  - Resource Quantity
  - Resource Production
- Highcharts is used on frontend
- Data source is view model, passed through game state (which we poll every 10 seconds anyway).
- **User Interaction**: 
  - Timeframe Selection: Ability to change focus (minute/hour/day).
  - Resource Toggling: Option to toggle display of specific resources (out-of-box with Highcharts)
  

#### Future Considerations
- Some dashboards for statuses.

## 7. Gameplay Mechanics

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

### Emergency Backups (Bridge Subsystem)

- Those activate when otherwise the crew would die (no dying in this game).
- BUT while active, the penalties apply.

Emergency Neural Command Interface (ENCI):
- **Status**: Standby/[Percentage]
- **Penalties**: Player can issue commands only when full, then it slowly fills again.
- **In-Game**: Activates a neural link so captain can issue commands even while in ELS stasis field. Issuing a command depletes it, then it slowly fills again.

Emergency Life Support (ELS):
- **Status**: Standby/Active
- **Activation**: Auto-activates itself and ENCI at low air, water, or food levels.
- **In-Game**: Generates a stasis field to reduce metabolic rates and resource consumption.

Emergency Power Core (EPC):
- **Status**: Idle/Standby/Active
- **Power Output**: [X] units/tick indefinitely.
- **In-Game**: Utilizes a compact fusion reactor for minimal, indefinite energy output.

### Bridge Dashboards

#### Critical Resources
- Primary mechanism for the player to recognize unfolding emergencies.
- Displays the quantity of critical resources: Air, Water, Food, and Energy. 
- They are color coded Green/Yellow/Red (and blinking) per defined thresholds

| Resource | Green    | Yellow  | Red    | % of What          |
|----------|----------|---------|--------|--------------------|
| Air      | 99-100%  | 51-98%  | 0-50%  | breathable air     |
| Water    | 81-100%  | 51-80%  | 0-50%  | defined quantity   |
| Food     | 81-100%  | 51-80%  | 0-50%  | defined quantity   |
| Energy   | 81-100%  | 51-80%  | 0-50%  | battery bank level |

#### Maintenance Alerts

- Shows number of maintenance requests
- Green means no requests
- Yellow: requests exist, all required parts are available
- Red: requests exist, some required parts are not available


### Production Chains

| Component    | SubSystem                | Produces           | Consumes                 | Byproduct  |
|--------------|--------------------------|--------------------|--------------------------|------------|
| AgroVats     | Hydroponic Vats          | Food               | Energy, Water, Nutrients | -          |
| AquaPurifier | Liquid Reclamation Unit  | Water              | WasteWater               | -          |
| OxyGenius    | Atmosphere Control Unit  | Air                | Water, Energy            | WasteWater |
| AeroMixer    | Air Circulation Unit     | Air                | Oxygen, Air              | -          |
| FusionMaster | Power Plant              | Energy             | Fuel Cells, Water        | WasteWater |


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

### Logistic Bots

Bots handle internal transport of resources.

1. **Capacity**: Fixed amount X, upgradable for better bots.
2. **Transport Time**: 1 tick within a subsystem, 5 ticks within a system, 10 ticks within a ship.
3. **Resource Types**: Can carry any "itemized" resource, defined by storage types.
4. **Task Assignment**: Two methods: A. Component requests and B. Captain's orders.
5. **Resource Prioritization**: Bots are designed to be "stupid" for gameplay challenge.
6. **Concurrency**: Operate in ticks, take random requests from a list.
7. **Energy Requirement**: Require power, slow down when power is low.
8. **Bot Assignment**: Some bots are "free roaming," others are system-specific.
- They are components, so can break down themselves, but not the last one (so we don't get into a deadlock)

### Shuttles

Shuttles handle resource transport outside the ship.

1. **Capacity**: Depends on installed storage units.
2. **Transport Time**: X ticks depending on distance.
3. **Resource Types**: Depends on installed storage units.
4. **Task Assignment**: Manual and automatic, player-driven.
5. **Inter-ship Transfer**: Possible, based on route and wishlist.
6. **Docking Requirements**: To be determined.
7. **Energy Requirement**: Require fuel, possibly the same as the ship.

### Drones

- Similar to bots but bigger and specialized for specific tasks like e.g. repairs or mining.
- Types:
    - Mining Drone
    - Repair Drone
    
### Repairs

- When a component breaks down:
    - It immediately adds a maintenance request for repair drones.
    - It also indicates which "simple part" is needed for repair, and number of ticks needed for repair 
    - These "simple parts" are limited to the ones used to manufacture the component or its subcomponents. 
    - Needed part and repair time are random (part from valid options, repair time 1-10)
- "Wear and tear" occasionally causes a random component to break.
- The captain can prioritize maintenance requests.

#### Simple Parts

- There are "simple parts" commonly used in manufacturing various components. 
- These are the only parts that will be required for repairs. 
- Examples include: Electronics Controller, Hydraulic Pump, Power Converter, Cooling Unit, etc

#### Repair Drones

- Repair drones randomly select a maintenance request to fulfill, but only if the required part is available. They chose from prioritized requests first
- Travel time: same as for Logistic Bots
- They are components, so can break down themselves, but not the last one (so we don't get into a deadlock)
- Require power, slow down when power is low.

### Future Considerations

### Sensors

Sensors are additional components planned for future implementation. They will assist in various tasks like resource discovery and hazard detection.

- **Types**: Astro-Body, Resource, Life Form, Hazard, etc.
- **Attributes**: Range, Accuracy, Speed, Power Consumption.
- **Upgrades**: Improved sensors, faster computing hardware, specialized algorithms, and increased data storage.
- **Advanced Types**: Spectral, Radio, Gravitic, Thermal.
- **Data Analysis**: From raw sensor data to player interpretation, various levels of data analysis will be available. This analysis process may itself function as a "production chain" within the game.

## 8. Database Models

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
- **ResourceHistory**: Each tick stores aggregated resource quantity, production and consumption.

Not implemented yet:
- **World Object**: Manages the overall game state.
- **Part**: Smaller elements used to assemble Components.
- **Bots**: Handle internal transport of resources.
- **Shuttles**: Handle resource transport outside the ship.


### Ship

Ship consists of ShipSystems, which consist of Components:
- **ShipSystem**: An umbrella term for a logical container for group of sub-systems, organized by ship's high-level functions. E.g., Navigation, Engineering, etc.
- **SubSystem**: Collection of components that together provide single function within a ship's sytem. E.g. Atmosphere control subsystem within Life Support system.
- **Component**: A specific piece of hardware within a ShipSystem that does the actual work. Consumes resources and produces resources or other Components. Assembled from Parts and other Components.
- **Part**: Smaller elements that are used to assemble Components. Manufactured from Resources and Parts.

Ship systems and their subsystems in the game:
- **Bridge**: MainComputer, ShipsLog, EmergencyBackups
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

ResourceHistory:
- Source for historical data (for charts etc) for resource quantity, production, consumption over time
- each record represents aggregated data for single tick
- Fields: tick, quantity_data, production_data, consumption_data
- data fields are JSON dictionaries 

### Future Considerations

#### Universe

- **Hierarchy**: Universe > Star System > Stars > Planets > Moons
- Also: Artificial Structures, Ships (the Ship?), other celestial bodies
- Types of Stars: O-Type, B-Type, A-Type, F-Type, G-Type, K-Type, M-Type, Red Giant, White Dwarf, Neutron Star, Blue Giant
- Types of Planets: Rocky, Gas Giant, Ice Giant, Volcanic, Water World
- Types of Moons: Rocky, Icy, Volcanically Active, Iron
- Characteristics for planets and moons: Tidally Locked, Atmosphere-bearing, Waterless

### Ship and Locations

- **Ship Status**: In transit, Docked, Landed, In orbit
- **Location**: Reference to a celestial body or coordinates


