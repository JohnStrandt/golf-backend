let searchForm = document.getElementById("searchForm");
let pageLinks = document.getElementsByClassName("page-link");

if (searchForm) {
  for (let i = 0; i < pageLinks.length; i++) {
    pageLinks[i].addEventListener("click", (e) => {
      e.preventDefault();

      // data attribute
      let page = e.currentTarget.dataset.page;
      console.log("Page: ", page);

      // add hidden search input to form
      searchForm.innerHTML += `<input value=${page} name="page" hidden />`;

      searchForm.submit();
    });
  }
}

// const toggle_vis = () => {
//   var x = document.getElementById("toggler");
//   if (x.style.display === "none") {
//     x.style.display = "grid";
//   } else {
//     x.style.display = "none";
//   }
// }

// let tags = document.getElementsByClassName("project-tag");

// Array.from(tags).forEach((tag) => {
//   tag.addEventListener("click", (e) => {
//     let tagId = e.target.dataset.tag;
//     let projectId = e.target.dataset.project;

//     console.log(tagId);

//     fetch("http://127.0.0.1:8000/api/remove-tag/", {
//       method: "DELETE",
//       headers: {
//         "Content-Type": "application/json"
//       },
//       body: JSON.stringify({ project: projectId, tag: tagId })
//     })
//       .then((response) => response.json())
//       .then((data) => {
//         e.target.remove();
//       });
//   });
// });
