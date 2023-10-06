


# 13. constraints and considerations

there are several gameplay considerations we need to implement, let me list them now:
- all ship's components are being "processed" every tick, we'll make it be in random order (at the moment it's sequential)
- most components will not finish one production cycle in single tick, so we'll need to keep track of progress or ticks
- if not enough inputs are available, component takes whatever it can but doesn't start, just keeps it for the next try
- when component is finished, it outputs what it produced up to available storage capacity, if it can't output everything it waits for next cycle to retry to get rid of it

since it sounds a lot to me, I would keep this commit simple, so implement any non-essential logic (like checking whether available inputs are greater than 0) for very next step

what do you think?
ChatGPT
You're right; adding these gameplay considerations will make your simulation more complex but also more realistic and engaging. Let's break it down.

Random Order Processing: Simple enough to implement by randomizing the list of installed components before iterating over them.

Tracking Progress: You'll need to add an additional field to the InstalledComponent model to keep track of progress or ticks required for completion.

Partial Inputs: Here you could gather the resources, but not actually start the processing until you have all required resources.

Output Constraints: This could be tricky. You'd need to add some logic to check the available storage capacity for the produced resource.

Let's start with a simplified approach. The complexity will mostly come from ensuring all conditions are met before changing the state of resources or the component's progress.

don't check for ship
- we don't have multiple ships/supersystems yet
- we don't have that layer implemented yet (all systems and subsystems are just there, not part of a ship)
- installed cargo unit doesn't link to ship even indirectly, it links to subsystem, which links to system, which doesn't link to anything (yet)






ChatGPT
Fantastic! I'm glad to hear that the code is working for you. Now, let's discuss the next steps for implementing the gameplay constraints you mentioned. Here's a quick summary of the constraints for reference:

All ship's components should be processed in a random order each tick.
Most components will not finish one production cycle in a single tick; you'll need to keep track of progress or ticks.
If not enough inputs are available, the component takes whatever it can but doesn't start and keeps it for the next try.
When a component finishes, it outputs what it produced up to the available storage capacity. If it can't output everything, it waits for the next cycle to retry.
Proposed Solutions:
Random Order Processing: To randomize the order of component processing, you can simply shuffle the list of components before iterating over them.

Tracking Progress: One way to track the progress of each component is to have a progress or ticks attribute for each installed component in the database. This would be incremented each time the component processes.

Handling Input Constraints: This would involve checking the availability of inputs before consumption and production occur. If not enough resources are available, the component can simply hold its consumption but not start its production.

Handling Output Constraints: Similar to input constraints, you'll need to check whether there is enough storage available before actually producing resources. If not, the component holds its output until the next cycle.

Would you like to dive deeper into each of these constraints? We can go through each one step-by-step and discuss possible implementations.




User
let's discuss tracking progress in little more detail

what would be intuitive for player is that "machine X takes 2 minutes to produce Y" - so we will need "game time". how do we decide what single tick represents?

since we could decide for technical or UX reasons to change ticks frequency, it might make sense to start from fundamentals: how many minutes in real time represent how many hours in game time. For example one minute RL could be one hour in-game (that translates one hour of actual playing into advancing game by roughly 2.5 days, which sounds about right.

If we keep this ratio defined and our target, then calculating tick from game time is simple. 

Which means we could keep definitions (for components, etc) in game-time: again the same example, machine X in 2 minutes produces Y.

Would that make sense?  Are there other considerations? How do other games do it? W 
ChatGPT
Tracking Progress: Game Time vs. Real Time
The concept of game time vs. real time is common in many simulation and strategy games. There are a couple of factors that typically drive the decision of how to set up this relationship:

Gameplay Pacing: How quickly do you want the game to progress? If a lot is supposed to happen in a short amount of in-game time, then you would need a faster ratio of game time to real time.

User Experience: If some activities take "days" in-game but only minutes in real life, this has to be communicated clearly to the player to set the right expectations.

Game Balance: Some tasks might be easy to perform and should be quick, but others should be more difficult and take more time, both in-game and in real life.

Technical Constraints: If each "tick" in the game involves complex calculations, you may be limited in how fast you can actually process these ticks.

Your Proposed Approach
Your idea to map 1 real-life minute to 1 in-game hour seems to be a good starting point and offers a clear and easy-to-understand mapping. In terms of maintaining this mapping when adjusting the tick frequency, here are a couple of methods:

Static Game Time: Keep the game time to real-time ratio fixed. This way, you can adjust the tick rate while maintaining a consistent game time experience. For example, if one tick is supposed to represent 10 minutes of game time, then whether your tick happens every 10 seconds or every minute in real life, you know that each tick advances the game by 10 minutes.

Dynamic Adjustment: Alternatively, you could allow for some "time dilation" features where the game time can be sped up or slowed down, either due to gameplay mechanics or player choice.

How Other Games Do It
Fixed Ratios: Many games use a fixed ratio of game time to real-time that best suits their gameplay mechanics and pacing. This is often not adjustable by the player.

Variable Speeds: Some games allow the player to adjust the speed at which time passes in-game, often with limitations to prevent breaking game balance.

Event-Driven: In some games, time only advances when certain actions are taken, rather than on a fixed tick. This gives the player more control but can make game balancing more challenging.

Conclusion
Given these considerations, your proposed approach of keeping a fixed ratio and defining all component times in terms of in-game time seems like a sound strategy. It simplifies many calculations and makes it easy to adjust the tick rate if needed without affecting game balance. It's also more intuitive for the player. Would you like to proceed with implementing this or discuss further?




User
let's discuss a bit how to implement input/output constraints
ChatGPT
Certainly! When we talk about input/output constraints in the context of your simulation, it sounds like we need to consider a few things:

Component Processing Time: How long a component takes in in-game time to consume inputs and produce outputs. This needs to be tracked across multiple ticks if the component's operation takes longer than one tick.

Resource Availability: If enough inputs are not available, the component should not start its operation and should instead wait for the next tick to see if enough inputs are available.

Output Capacity: A component can produce resources only up to the available storage capacity. If it can't offload its produced resources, it should wait for the next cycle to retry.

Here are some thoughts on how to implement each of these:

Component Processing Time
Each component could have an additional field or attribute that keeps track of its "progress" or "time until completion".
Each tick, if the component is "working", you decrement this counter.
When the counter reaches zero, you produce the output and reset the counter based on the original component definition.
Resource Availability
Before a component starts its cycle, check if the required resources are available.
If they are, decrement the resources and start the component's cycle. Otherwise, wait for the next tick.
Output Capacity
When a component finishes its cycle, first check if there is enough capacity in the storage to hold the produced resources.
If there is, add the resources to storage and continue. Otherwise, wait for the next tick to try again.


i would like to comment on this:
"1. Before a component starts its cycle, check if the required resources are available.
2. If they are, decrement the resources and start the component's cycle. Otherwise, wait for the next tick."

there might be components that produce small things very fast (think "nails" or something) and others that need huge amount of same resource to do something with it (think "tank chassis") - so if there is not enough resources for everyone, mass-producers of small stuff will continue producing every cycle, while big consumers could never get their turn.

what I'm proposing is that each machine (they are picked randomly anyway) takes as much resources as it can (up to a limit, let's say 2 production cycles, but we could simply start with just what's needed for single cycle) , never minding whether it can start actual production or not

what do you think?
ChatGPT
Your proposal makes sense and adds a layer of complexity to the resource management aspect of the game. It also seems more realistic in terms of how resources might be allocated in a situation where multiple components are competing for the same resources.

In the scenario you described, each machine/component would essentially "reserve" resources for itself until it has enough to begin a cycle. This approach would indeed prevent smaller, faster-producing components from monopolizing all the available resources, giving the larger, slower components a fair chance to accumulate what they need.

roach?




User
i think of it as a inherent buffer, each machine has built in - could you change the naming so it's clear from the code
ChatGPT
Certainly! A built-in buffer makes the concept very clear. Here's the updated code snippet, with revised naming to emphasize the built-in buffer for each installed component:



User
yes, that's good

and what about output constraints? to me it sounds trivial to check, but haven't really put thought into it
ChatGPT
The output constraints can be handled in a straightforward manner, especially if we already have a buffering system for inputs. The idea is to produce outputs only if there is enough space in the corresponding storage. If not, the component would need to wait until space is available.

Here's a simplified example that focuses just on output constraints:



User
ok, now few overall considerations:

do we buffer energy? (probably not)

do we bufer fluids? (probably yes, in the same way as the "itemized" stuff)

machines will need some kind of status, that can be reported (e.g. bridge could see aggregated statuses of everything) or even kept history of (player will need some kind of data to base his decisions from, either production charts, or utilization charts, or both)
ChatGPT
Buffering Considerations:
Energy:
Generally, in games and simulations, energy isn't buffered in the same way as other resources. Energy is typically consumed instantaneously as it is generated, so it often doesn't make sense to "store" it beyond what specialized energy storage components (e.g., batteries) can hold.

Fluids:
Fluids can be buffered similarly to itemized resources, especially if they are considered as "bulk" resources that are stored in tanks or similar containers. The simulation logic for fluids can essentially be the same as that for solid resources.

Machine Status and Reporting:
Status Reporting: Each machine can have a status attribute that could take values like "Idle", "Running", "Paused for Input", "Paused for Output", "Paused for Energy", etc. This status could be used both for individual machine reporting and for aggregated views.

# 14. historical data

Historical Data: You can also keep track of machine utilization, production rates, and other relevant metrics over time. This historical data can then be displayed in various formats, such as charts or logs, to help players make informed decisions.

You might want to create specialized classes or data structures to hold this historical data. The granularity of the data would depend on how detailed you want the history to be and how much computational resources you're willing to allocate for this feature.

Would you like to discuss these topics in more detail?




User
about historical data:

machines change over time, get installed/uninstalled, their quantity changes, etc - might not make sense to keep history data for machines

what doesn't change are resources - maybe we simply keep track of production/consumption data similar to as factorio does

also, systems and subsystems will be pretty much fixed 
ChatGPT
Keeping track of resources over time makes a lot of sense, especially if machines are frequently changed. Tracking resource utilization, production, and consumption can provide useful insights for players without adding unnecessary complexity related to tracking each machine's historical data. It's simpler to implement and likely more useful for gameplay.

Resource-Based Metrics:
Production Rate: This could be the rate at which each resource is being produced per tick or over a longer time period (e.g., 5 minutes, 1 hour in-game time).

Consumption Rate: Similarly, track how fast each resource is being consumed. This can help players identify potential bottlenecks or overproduction.

Net Gain/Loss: This could be an aggregated metric that takes into account both production and consumption to give a net figure. If this number is negative, it indicates the player is consuming more than producing, which is critical information.

Resource Availability: Track the average and peak availability of each resource over time. This helps the player understand how close they are to running out or overflowing storage for a particular resource.

System/Subsystem Metrics:
Given that systems and subsystems are relatively fixed:

Utilization Rate: For each system or subsystem, you could keep track of the percentage of time it's actively processing vs idle. This could be used to identify inefficiencies at a higher level.

System Status: Like machine status, each system/subsystem can have an aggregated status that summarizes the statuses of its component machines.

Reporting:
Charts: Utilize time-series charts to depict these metrics over time.

Alarms/Notifications: Based on these metrics, generate alarms or notifications if certain thresholds are crossed (e.g., low resource availability, high consumption rate, etc.)

Snapshots: Periodically save the state of these metrics to provide a "historical snapshot" that players can refer to.

Would these approaches fit within your vision for the game?




User
also, we might not care how much Kryptonite is available in Kryptonite mines, but we might care a lot how much of it is available in Superman Suppression system on the ship - never mind bad example, but we probably want to track production/consumption (and thus net gain/loss) by location, system, subsystem.. correct?
ChatGPT
Absolutely, location-specific tracking could add a layer of strategic depth and realism to the game. Knowing where resources are being used or produced most heavily can inform a lot of decisions.

Here's how you could break it down:

Location-Specific Metrics
System/Subsystem Resource Metrics:

Track production, consumption, and net gain/loss for each system and subsystem.
For example: The "Power Plant" system might produce 'Energy', whereas the "Life Support" subsystem might consume 'Oxygen' and 'Energy'.
Global Metrics:

These would still exist and provide an overall snapshot, but the system/subsystem metrics can feed into this for a comprehensive view.
Storage Location:

Knowing where resources are stored can be crucial for logistical reasons. For example, it wouldn't be efficient to produce food in one part of the ship but store it far away from where it's consumed.
Resource Transit:

If resources have to move from one part of the ship to another, tracking how long this takes and the efficiency of the process could add another layer of complexity.
Priority Metrics:

Some systems or subsystems may be more critical than others. Having a "priority" metric that indicates which systems should get resources first in times of scarcity can add another layer of strategy.
How to Implement:
Tagging Resources:

When a resource is produced, it can be tagged with its system of origin. This would allow you to track how much of each resource is being produced where.
Database Schema:

Each resource entry could include a field for its location, making it easy to query location-specific stats.
Reporting:

These new metrics can feed into whatever reporting mechanisms you're already planning, whether that's charts, logs, or alerts.
Would this sort of location-specific tracking align with your vision for the game?




User
let's think about it in "records" terms, like in database, or logs - what do we need in each record/line item?
ChatGPT
Sure, if you're thinking in terms of database records or log lines, each entry would need to capture a variety of fields to provide a comprehensive picture of resource transactions in the game. Here's what a basic schema could look like:

Resource Transaction Schema
Timestamp:

When the transaction occurred. This would be in "game time."
Resource Type:

What kind of resource is being produced or consumed (e.g., Energy, Oxygen, Food).
Transaction Type:

Whether the resource was produced or consumed.
Amount:

The quantity of the resource produced or consumed.
System ID:

Which system the resource is linked to (e.g., Power Plant, Life Support).
Subsystem ID:

Which subsystem within the system (if applicable).
Component ID:

Specific component within the subsystem that was involved (if applicable).
Location ID:

Where this resource is stored or where the transaction happened. Could be specific to a sector of the ship or a specific storage unit.
Priority Level:

Optional. If certain systems or subsystems have set priorities, log that here.
Status:

Current status of the component, system, or subsystem involved in the transaction (e.g., Operational, Malfunctioning, Inactive).
Buffer Status:

The amount of buffered input and output resources for the component (if applicable).
Example Log Line or Database Record
Timestamp	Resource_Type	Transaction_Type	Amount	System_ID	Subsystem_ID	Component_ID	Location_ID	Priority_Level	Status	Buffer_Status
1001	Energy	Produce	50	1	2	5	2	High	Operational	0/10
1002	Oxygen	Consume	10	1	3	6	3	Low	Operational	3/0
This schema could be tailored to your specific needs but should offer a comprehensive snapshot for every resource transaction in the game. Would this work for you?




User
I like the example record format, could you repeat but without components nor buffer since components are volatile
ChatGPT
Certainly! If you're not including components and their buffer status, the schema could be simplified like this:

Resource Transaction Schema (Simplified)
Timestamp:

When the transaction occurred. This would be in "game time."
Resource Type:

What kind of resource is being produced or consumed (e.g., Energy, Oxygen, Food).
Transaction Type:

Whether the resource was produced or consumed.
Amount:

The quantity of the resource produced or consumed.
System ID:

Which system the resource is linked to (e.g., Power Plant, Life Support).
Subsystem ID:

Which subsystem within the system (if applicable).
Location ID:

Where this resource is stored or where the transaction happened. Could be specific to a sector of the ship or a specific storage unit.
Priority Level:

Optional. If certain systems or subsystems have set priorities, log that here.
Status:

Current status of the system or subsystem involved in the transaction (e.g., Operational, Malfunctioning, Inactive).
Example Log Line or Database Record (Simplified)
Timestamp	Resource_Type	Transaction_Type	Amount	System_ID	Subsystem_ID	Location_ID	Priority_Level	Status
1001	Energy	Produce	50	1	2	2	High	Operational
1002	Oxygen	Consume	10	1	3	3	Low	Operational
This simplified schema still gives you a snapshot of resource transactions but omits the more volatile details associated with specific components and their buffer states. Would this be more aligned with your requirements?




User
remove priority and status, they are not directly related to the resource transaction

list the fields as before but in one line each (plus table example as before)

and then give few examples of charts/report we can produce from such schema
ChatGPT
Resource Transaction Schema (Further Simplified)
Timestamp: When the transaction occurred in "game time."
Resource Type: The kind of resource involved (e.g., Energy, Oxygen).
Transaction Type: The type of transaction (Produced or Consumed).
Amount: The quantity of the resource involved.
System ID: Identifier for the system involved (e.g., Power Plant).
Subsystem ID: Identifier for the subsystem within the system (if applicable).
Location ID: Identifier for where this resource is stored or where the transaction happened.
Example Log Line or Database Record (Further Simplified)
Timestamp	Resource_Type	Transaction_Type	Amount	System_ID	Subsystem_ID	Location_ID
1001	Energy	Produce	50	1	2	2
1002	Oxygen	Consume	10	1	3	3
Potential Reports/Charts:
Resource Production Over Time: Line chart displaying production rates for each resource type.

Resource Consumption Over Time: Similar to production but for consumption rates.

Resource Surplus/Deficit: A chart showing the net surplus or deficit for each resource type.

System-Specific Resource Usage: Bar chart or pie chart breaking down resource usage or production by system.

Subsystem-Specific Resource Usage: Similar to the system-specific chart but for subsystems.

Location-Specific Resource Inventory: Stacked bar or pie chart showing the amount of each resource type stored at different locations.

Resource Availability Heatmap: Heatmap showing where each resource is most and least abundant.

Resource Transaction Timeline: A Gantt chart or similar showing all transactions in a given time period, color-coded by type of transaction (production or consumption).

Global Resource Flow: Sankey diagram showing how resources move between different systems, subsystems, and locations.

Critical Resource Points: A table highlighting moments where resource levels reached critically low or high points, which might require player attention.

