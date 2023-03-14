// Get all the headings in the document
const headings = (
    document
    .getElementsByClassName("page-content")
    .querySelectorAll('h1, h2, h3')
);

// Initialize variables to keep track of the current level and the parent element
var level = 0;
var lastLi = toc;

// Loop through all the headings and create a table of contents
for (let i = 0; i < headings.length; i++) {
    // Get the current heading level (e.g. 1 for <h1>, 2 for <h2>, etc.)
    var currentLevel = parseInt(headings[i].tagName.slice(1));

    // If the current level is higher than the previous level, create a new nested list
    if (currentLevel > level) {
        var newUl = document.createElement('ul');
        var newLi = document.createElement('li');
        newLi.appendChild(document.createTextNode(headings[i].textContent));
        newUl.appendChild(newLi);
        lastLi.appendChild(newUl);
        lastLi = newLi;
        level++;
    }

    // If the current level is lower than the previous level, move back up the list
    else if (currentLevel < level) {
        var diff = level - currentLevel;
        for (var j = 0; j < diff; j++) {
          lastLi = lastLi.parentNode.parentNode;
        }
        var newLi = document.createElement('li');
        newLi.appendChild(document.createTextNode(headings[i].textContent));
        lastLi.appendChild(newLi);
        lastLi = newLi;
        level--;
    }

    // If the current level is the same as the previous level, add a new list item
    else {
        var newLi = document.createElement('li');
        newLi.appendChild(document.createTextNode(headings[i].textContent));
        lastLi.parentNode.appendChild(newLi);
        lastLi = newLi;
    }

    // Add the list item to the table of contents
    document.getElementById('toc-list').appendChild(li);
}