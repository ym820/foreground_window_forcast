// Get all the headings in the body
const body = document.getElementsByClassName("page-content")[0];
const headings = body.querySelectorAll('h1, h2, h3');
console.log(headings)
// Create a new unordered list to hold the table of contents
var tocList = document.createElement('ul');

// Loop through each heading element and create a table of contents entry for it
headings.forEach(function(heading) {
    const listItem = document.createElement('li');
    // Create a link to the heading
    const link = document.createElement('a');
    link.setAttribute('href', `#${heading.id}`);
    link.textContent = heading.textContent;
    // Add the link to the list item
    listItem.appendChild(link);
    tocList.appendChild(link)
});
  
// Add the table of contents to the appropriate container on the page
document.getElementById('table-of-contents').appendChild(tocList);