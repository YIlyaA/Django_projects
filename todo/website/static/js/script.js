// document.addEventListener("DOMContentLoaded", function () {
//   const addItemButton = document.getElementById("add-item");
//   const newFieldsContainer = document.getElementById("new-fields-container");

//   addItemButton.addEventListener("click", function (event) {
//     event.preventDefault(); // Prevent form submission

//     // Create a new input field and save button
//     const newDiv = document.createElement("div");
//     newDiv.className = "todo-body";
    
//     const newInput = document.createElement("input");
//     newInput.type = "text";
//     newInput.name = "description";
//     newInput.className = "todo-input";
//     newInput.placeholder = "Enter another item";

//     const saveButton = document.createElement("button");
//     saveButton.type = "submit";
//     saveButton.className = "save-button";
//     saveButton.textContent = "Save";

//     // Append the new input and button to the new div
//     newDiv.appendChild(newInput);
//     newDiv.appendChild(saveButton);

//     // Add the new div to the container
//     newFieldsContainer.appendChild(newDiv);
//   });
// });
