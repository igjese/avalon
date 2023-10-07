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

#### Universe and Ship Location Models
- **Universe Model**: Describes the hierarchy of celestial bodies.
- **Ship Location Model**: Describes the ship's (or e.g. mining facility) status and location.


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


### Future Considerations

#### Bots and Shuttles in Resource Management
- **Bots**: Handle resource transport within the ship.
- **Shuttles**: Handle resource transport outside the ship.

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

