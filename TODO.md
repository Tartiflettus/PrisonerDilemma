- Change the functionality of the ECA into an object oriented approach

    - Change the rectangles of the canvas into a list of "Prisoner"
    - Each "Prisoner" can change its state instead of a global loop that checks all the rectangles
        - Prisoner has update function that calculates its payoff and updates its rectangle in the canvas
        - Global function that invokes the update function for each Prisoner
        - The Global function is called using the tk.after method

- Add variable width and height settings

- Add reset/init button(s)