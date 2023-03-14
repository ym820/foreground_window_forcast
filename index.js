// Get all the headings in the body
const body = document.getElementsByClassName("page-content")[0];
const headings = body.querySelectorAll('h1, h2, h3');
// Create a new unordered list to hold the table of contents
var tocList = document.createElement('ul');

// Keep track of the most recent parent list item so that you can nest list items properly
var parentListItem = tocList;


// Loop through each heading element and create a table of contents entry for it
headings.forEach(function(heading) {
    // Skip over any headings that have the 'notoc' class
    if (heading.classList.contains('notoc')) {
      return;
    }
    
    // Get the level of the heading (i.e. whether it is an h1, h2, h3, etc.)
    var level = parseInt(heading.tagName.charAt(1));
    
    // Create a new list item for the heading
    var listItem = document.createElement('li');
    
    // Create a link to the heading element
    var link = document.createElement('a');
    link.href = '#' + heading.id;
    link.innerText = heading.innerText;
    
    // Add the link to the list item
    listItem.appendChild(link);
    console.log(level, parentListItem.tagName.charAt(1), parentListItem.tagName.charAt(1))
    // Determine the nesting level of the list item and add it to the proper parent list item
    if (level > parentListItem.tagName.charAt(1)) {
      // If the level of the heading is greater than the level of the parent list item, create a new sublist
      var sublist = document.createElement('ul');
      parentListItem.lastChild.appendChild(sublist);
      console.log("Get a nested list")
      parentListItem = sublist;
    } else if (level < parentListItem.tagName.charAt(1)) {
      // If the level of the heading is less than the level of the parent list item, move back up to the appropriate level
      git while (level < parentListItem.tagName.charAt(1)) {
        parentListItem = parentListItem.parentElement.parentElement;
      }
    }
    
    // Add the list item to the parent list item
    parentListItem.appendChild(listItem);
  });
  
// Add the table of contents to the appropriate container on the page
document.getElementById('table-of-contents').appendChild(tocList);