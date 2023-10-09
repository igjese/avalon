# Tasks and Issues We Don't Want to Tackle Immediately

## Issues
- Energy should output every tick 
- Components might have to be individual, because this way if a subsystem has 100 components, they would all have production cycles simultaneously

## Tasks
- Component should finish the cycle nevermind output capacity is available or not, BUT output slowly as much it can and start NEXT cycle only when it got rid of all produced resources => among other things that would solve energy levels dropping while production capacity being more than enough but no capacity for output
- Components should be processed in random order (to avoid fast components monopolizing all the resources and starving slow components)