// Get all the headings in the body
const body = document.getElementsByClassName("page-content")[0];
const headings = body.querySelectorAll('h1, h2, h3');
console.log(headings)
// Create a new unordered list to hold the table of contents
var tocList = document.createElement('ul');

// Keep track of the previous level of heading to determine nesting
let prevLevel = 1;
let currLevel = 1;
// let prevListItem = tocList;
let currentList = null;

// Loop through each heading element and create a table of contents entry for it
headings.forEach(function(heading) {
    // Get the current heading level
    currLevel = parseInt(heading.tagName[1]);
    console.log(heading.tagName, heading.tagName[1])
    // Create a new list item for the heading
    const listItem = document.createElement('li');

    // Create a link to the heading
    const link = document.createElement('a');
    link.setAttribute('href', `#${heading.id}`);
    link.textContent = heading.textContent;

    // Determine the nesting level based on the difference between the current and previous heading level
    const levelDiff = currLevel - prevLevel;
    console.log(currLevel, prevLevel, levelDiff)
    // if (levelDiff > 0) {
    if (currLevel > prevLevel) {
        // If the current level is deeper than the previous level, create a new nested list
        const nestedList = document.createElement('ul');
        console.log("creating nested list");
        listItem.appendChild(nestedList);
        prevListItem = nestedList;
    } else if (levelDiff < 0) {
        // If the current level is shallower than the previous level, go up the tree to the appropriate parent list
        let i = 0;
        console.log("going up the tree");
        for (let u = headingLevel; u < levelDiff; u++) {
            prevListItem = prevListItem.parentNode;
        }
    }
    // Add the link to the list item
    // listItem.appendChild(link);

    // Add the list item to the appropriate list
    prevListItem.appendChild(link);

    // Update the previous level and list item for the next iteration
    prevLevel = currLevel;
});
  
// Add the table of contents to the appropriate container on the page
document.getElementById('table-of-contents').appendChild(tocList);