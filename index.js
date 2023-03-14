// Get all the headings in the document
const headings = document.querySelectorAll('h1, h2, h3');

// Loop through all the headings and create a table of contents
for (let i = 0; i < headings.length; i++) {
  // Get the text content of the heading
  const text = headings[i].textContent;

  // Create a list item for the heading in the table of contents
  const li = document.createElement('li');
  const a = document.createElement('a');
  a.textContent = text;
  a.href = '#' + headings[i].id;
  li.appendChild(a);

  // Add the list item to the table of contents
  document.getElementById('toc-list').appendChild(li);
}