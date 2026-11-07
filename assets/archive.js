const form = document.querySelector("#archive-filters");
const results = document.querySelector("#results");
const entries = Array.from(document.querySelectorAll("[data-entry]"), (element) => ({
  element,
  tags: JSON.parse(element.dataset.tags),
  year: element.dataset.year,
  searchable: element.textContent.toLowerCase(),
}));
const query = new URLSearchParams(window.location.search);
const { q, topic, year } = form.elements;
q.value = query.get("q") || "";
topic.value = query.get("topic") || "";
year.value = query.get("year") || "";
if (topic.selectedIndex < 0) topic.selectedIndex = 0;
if (year.selectedIndex < 0) year.selectedIndex = 0;

function filter() {
  const search = q.value.trim().toLowerCase();
  let count = 0;
  for (const entry of entries) {
    const match = (!topic.value || entry.tags.includes(topic.value))
      && (!year.value || entry.year === year.value)
      && entry.searchable.includes(search);
    entry.element.hidden = !match;
    if (match) count += 1;
  }
  results.textContent = count === 1 ? "1 post" : `${count} posts`;
}

form.addEventListener("input", filter);
form.addEventListener("submit", (event) => event.preventDefault());
form.hidden = false;
filter();
